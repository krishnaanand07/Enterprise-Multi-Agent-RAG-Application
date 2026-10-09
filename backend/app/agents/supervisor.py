from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import AgentState
from app.services.llm_service import llm_service


class SupervisorAgent:
    """Classifies user input into: 'DOCUMENT', 'DATA', or 'GENERAL'."""

    SUPERVISOR_PROMPT = """You are the Supervisor Router for an Enterprise AI Assistant.
Analyze the user's input query and determine the appropriate routing category:

1. 'DOCUMENT': Choose for standard factual questions, document searches, policy questions, project details, budgets, SLAs, guidelines, text summaries, or questions about uploaded enterprise documents (PDF, DOCX, TXT, manuals, reports, contracts).
2. 'DATA': Choose ONLY if the user explicitly asks to analyze, query, calculate, or summarize an uploaded CSV file, spreadsheet, or tabular dataset (e.g., "analyze my uploaded CSV", "calculate average revenue in the CSV dataset", "filter rows where column X > Y").
3. 'GENERAL': Choose for general conversational greetings, general knowledge questions, general coding/writing tasks, or statements that do NOT reference enterprise documents or tabular CSV datasets.

CRITICAL INSTRUCTIONS:
- Questions asking for document facts, project budgets, policy targets, SLA metrics, or report details (even if numerical, such as "total budget" or "acknowledgement target") MUST be routed to 'DOCUMENT'.
- Do NOT route to 'DATA' unless the query explicitly requests CSV/spreadsheet/tabular dataset operations.

Return ONLY one of the following exact single words in uppercase: DOCUMENT, DATA, or GENERAL.
Do not add punctuation or additional text.

User Query: {query}
Route:"""

    @classmethod
    async def route(cls, state: AgentState) -> AgentState:
        query = state["query"]
        try:
            llm = llm_service.get_llm(temperature=0.0)
            prompt = ChatPromptTemplate.from_template(cls.SUPERVISOR_PROMPT)
            chain = prompt | llm
            res = await chain.ainvoke({"query": query})

            raw_route = str(res.content).strip().upper()
            if "DATA" in raw_route or "CSV" in raw_route:
                # Require explicit CSV/dataset indicator keywords before routing to DATA agent
                query_lower = query.lower()
                csv_keywords = ["csv", "dataset", "spreadsheet", "tabular", "dataframe", "data file", "table"]
                if any(kw in query_lower for kw in csv_keywords):
                    selected_route = "DATA"
                else:
                    selected_route = "DOCUMENT"
            elif "GENERAL" in raw_route:
                selected_route = "GENERAL"
            else:
                selected_route = "DOCUMENT"

            state["route"] = selected_route
        except Exception:
            state["route"] = "DOCUMENT"  # Safe default fallback

        return state
