from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import AgentState
from app.services.llm_service import llm_service


class SupervisorAgent:
    """Classifies user input into: 'DOCUMENT', 'DATA', or 'GENERAL'."""

    SUPERVISOR_PROMPT = """You are the Supervisor Router for an Enterprise AI Assistant.
Analyze the user's input query and determine the appropriate routing category:

1. 'DOCUMENT': Choose if the query asks about uploaded enterprise documents, policies, pdfs, reports, or text files.
2. 'DATA': Choose if the query asks for numerical, statistical, structured aggregation, or analytical queries over tabular CSV data.
3. 'GENERAL': Choose if the query is a general question, greeting, coding task, or statement that does NOT require external enterprise documents.

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
            if "DOCUMENT" in raw_route or "RAG" in raw_route:
                selected_route = "DOCUMENT"
            elif "DATA" in raw_route or "CSV" in raw_route:
                selected_route = "DATA"
            else:
                selected_route = "GENERAL"

            state["route"] = selected_route
        except Exception:
            state["route"] = "DOCUMENT"  # Safe default fallback

        return state
