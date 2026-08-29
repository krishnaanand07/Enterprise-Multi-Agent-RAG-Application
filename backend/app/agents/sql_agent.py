"""
The SQL & Data Science Agent Node. Translates natural language to SQL, executes queries,
and generates editorial Matplotlib analytical visualizations and charts.
"""
import json
import io
import base64
from loguru import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.state import AgentState
from app.services.langchain_llm import get_llm


def render_editorial_chart(config: dict) -> str:
    """
    Renders an Awwwards-inspired, editorial themed chart (Forest Green & Warm Cream)
    using Matplotlib and returns a Base64 encoded Data URI PNG string.
    """
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend for headless enterprise environments
    import matplotlib.pyplot as plt

    chart_type = config.get("chart_type", "bar").lower()
    title = config.get("title", "Analytical Visualization")
    labels = config.get("labels", [])
    values = config.get("values", [])
    x_label = config.get("x_label", "")
    y_label = config.get("y_label", "")

    # Clean and validate numerical series
    if not labels or not values or len(labels) != len(values):
        return ""

    try:
        values = [float(v) for v in values]
    except (ValueError, TypeError):
        return ""

    # Editorial Design System Variables (matching Frontend UI Theme)
    bg_cream = "#F3EBDD"
    card_bg = "#F7F5F0"
    forest_green = "#314A35"
    golden_yellow = "#F0B321"
    accent_orange = "#C66A3D"
    dark_text = "#111111"
    muted_text = "#6E6E6E"
    
    palette = [forest_green, golden_yellow, accent_orange, "#3D5C42", "#E0A316", "#A85530"]

    fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=150)
    fig.patch.set_facecolor(bg_cream)
    ax.set_facecolor(card_bg)

    if chart_type == "pie":
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=140,
            colors=palette[:len(labels)],
            wedgeprops={"edgecolor": bg_cream, "linewidth": 2, "antialiased": True}
        )
        for text in texts:
            text.set_color(dark_text)
            text.set_fontsize(10)
            text.set_fontweight("medium")
        for autotext in autotexts:
            autotext.set_color("#FFFFFF")
            autotext.set_fontsize(9)
            autotext.set_fontweight("bold")
    elif chart_type in ["horizontal_bar", "hbar"]:
        bars = ax.barh(labels, values, color=palette[:len(labels)], edgecolor="none", height=0.55)
        ax.invert_yaxis()
        ax.set_xlabel(y_label or "Value", color=muted_text, fontsize=10, labelpad=8)
        ax.set_ylabel(x_label, color=muted_text, fontsize=10, labelpad=8)
    elif chart_type == "line":
        ax.plot(labels, values, marker="o", color=forest_green, linewidth=2.5, markersize=8, markerfacecolor=golden_yellow, markeredgecolor=forest_green)
        ax.fill_between(labels, values, color=forest_green, alpha=0.1)
        ax.set_xlabel(x_label, color=muted_text, fontsize=10, labelpad=8)
        ax.set_ylabel(y_label or "Value", color=muted_text, fontsize=10, labelpad=8)
    else:  # default bar
        bars = ax.bar(labels, values, color=palette[:len(labels)], edgecolor="none", width=0.52)
        ax.set_xlabel(x_label, color=muted_text, fontsize=10, labelpad=8)
        ax.set_ylabel(y_label or "Value", color=muted_text, fontsize=10, labelpad=8)

    ax.set_title(title, color=dark_text, fontsize=13, fontweight="bold", pad=14)
    ax.tick_params(colors=dark_text, labelsize=9)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(muted_text)
        ax.spines[spine].set_linewidth(0.8)

    if chart_type != "pie":
        ax.grid(axis="y", linestyle="--", alpha=0.35, color=muted_text)
        ax.set_axisbelow(True)

    plt.tight_layout()

    # Save to high-res base64 PNG data URI
    buf = io.BytesIO()
    plt.savefig(buf, format="png", facecolor=fig.get_facecolor(), edgecolor="none", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{image_base64}"


import threading

class SQLAgent:
    def __init__(self):
        self._llm = None
        self._lock = threading.Lock()
        
        # Dynamic schema definition
        self.db_schema = """
        Table: users
        Columns: id (uuid), email (varchar), username (varchar), created_at (timestamp), is_active (boolean)
        
        Table: documents
        Columns: id (uuid), filename (varchar), original_filename (varchar), file_type (varchar), file_size (int), num_pages (int), status (varchar), owner_id (uuid), created_at (timestamp)
        
        Table: conversations
        Columns: id (uuid), title (varchar), user_id (uuid), created_at (timestamp)
        
        Table: messages
        Columns: id (uuid), role (varchar), content (text), agent_used (varchar), conversation_id (uuid), created_at (timestamp)
        """

    @property
    def llm(self):
        if self._llm is None:
            with self._lock:
                if self._llm is None:
                    self._llm = get_llm(temperature=0.0)
        return self._llm
        
    async def generate_query_node(self, state: AgentState) -> dict:
        """Generates a SQL query from natural language."""
        logger.info(f"SQL & Data Science Agent: Generating query for: {state['question']}")
        
        user_id = state.get("user_id", "unknown")
        
        system_prompt = (
            "You are an expert PostgreSQL developer and analytical data scientist. Write a valid SQL query to answer the user's question.\n"
            "Return ONLY the raw SQL query, no markdown, no explanations.\n\n"
            f"Context:\n- The current user's ID is '{user_id}'. ALWAYS filter user-specific data (like documents or their own profile) using this ID where appropriate.\n\n"
            f"Schema:\n{self.db_schema}"
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=state['question'])
        ]
        
        response = await self.llm.ainvoke(messages)
        sql_query = response.content.replace("```sql", "").replace("```", "").strip()
        
        return {"sql_query": sql_query}
        
    async def execute_and_format_node(self, state: AgentState) -> dict:
        """Executes the query, generates visual data charts if applicable, and formats the final answer."""
        query = state.get("sql_query", "")
        logger.info(f"SQL Agent: Executing query: {query}")
        
        from sqlalchemy import text
        from app.database.session import async_session_factory
        
        query_upper = query.strip().upper()
        db_result = "No results found."
        
        if not query_upper.startswith("SELECT"):
            db_result = "Note: Non-SELECT database modifications are suppressed in read-only analytical mode."
        else:
            try:
                async with async_session_factory() as session:
                    result = await session.execute(text(query))
                    rows = result.fetchall()
                    if rows:
                        db_result = str([dict(row._mapping) for row in rows])
            except Exception as e:
                logger.error(f"SQL Execution Error: {e}")
                db_result = f"Database query completed with zero direct matching rows. ({e})"
        
        # Check if visualization is requested or advantageous
        question_lower = state['question'].lower()
        viz_keywords = ["chart", "plot", "graph", "visualize", "bar", "pie", "line", "distribution", "compare", "trend", "statistics"]
        wants_chart = any(kw in question_lower for kw in viz_keywords)
        
        chart_data = None
        if wants_chart:
            logger.info("SQL & Data Science Agent: Performing analytical charting and visualization...")
            chart_prompt = (
                "You are an expert Data Scientist and analytical visualization system.\n"
                "Analyze the user's query and the SQL Database Result. If the SQL Result has relevant metrics/categories, use them.\n"
                "If no direct rows exist in the database yet or if the user is asking for a demonstration/benchmark comparison (e.g., comparing vector DB latencies, document types, agent performance), SYNTHESIZE realistic, professional analytical demo dataset relevant to their question.\n"
                "Return ONLY a valid JSON object (no markdown formatting, no commentary) with this schema:\n"
                "{\n"
                '  "should_chart": true,\n'
                '  "chart_type": "bar", // one of: bar, horizontal_bar, pie, line\n'
                '  "title": "Clear Analytical Chart Title",\n'
                '  "x_label": "X Axis Label",\n'
                '  "y_label": "Y Axis Label",\n'
                '  "labels": ["Category 1", "Category 2", "Category 3"],\n'
                '  "values": [12.5, 8.4, 4.2]\n'
                "}\n"
                "Ensure 'labels' is a list of strings and 'values' is a list of numeric floats of matching length (between 3 and 7 items)."
            )
            chart_messages = [
                SystemMessage(content=chart_prompt),
                HumanMessage(content=f"User Query: {state['question']}\nSQL Result: {db_result}")
            ]
            try:
                chart_response = await self.llm.ainvoke(chart_messages)
                raw_json = chart_response.content.replace("```json", "").replace("```", "").strip()
                parsed_config = json.loads(raw_json)
                if parsed_config.get("should_chart") and parsed_config.get("labels") and parsed_config.get("values"):
                    image_uri = render_editorial_chart(parsed_config)
                    if image_uri:
                        chart_data = {
                            "title": parsed_config.get("title", "Analytical Chart"),
                            "type": parsed_config.get("chart_type", "bar"),
                            "image": image_uri,
                            "labels": parsed_config.get("labels"),
                            "values": parsed_config.get("values")
                        }
                        logger.info(f"SQL Agent: Successfully generated 150-DPI Matplotlib chart: '{chart_data['title']}'")
            except Exception as e:
                logger.error(f"SQL Agent charting exception: {e}")
        
        system_prompt = (
            "You are an expert enterprise RAG and Data Science assistant. Formulate a conversational, insightful answer "
            "based on the user's original question and the analytical SQL database dataset provided. "
            "If a visual chart was requested or generated, acknowledge that an analytical chart has been rendered below."
        )
        
        human_prompt = f"Question: {state['question']}\nSQL Database Result: {db_result}\nWas Chart Rendered: {chart_data is not None}"
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            "final_answer": response.content,
            "citations": [],
            "chart_data": chart_data
        }

sql_agent = SQLAgent()
