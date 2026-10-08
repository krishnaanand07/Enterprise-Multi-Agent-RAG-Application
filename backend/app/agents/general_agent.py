from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import AgentState
from app.services.llm_service import llm_service


class GeneralAgent:
    """General QA Node for questions not requiring specific documents."""

    GENERAL_PROMPT = """You are a helpful, professional Enterprise AI Assistant.
Answer the user's question accurately and helpfully.

Question: {query}
Answer:"""

    @classmethod
    async def process(cls, state: AgentState) -> AgentState:
        query = state["query"]
        try:
            llm = llm_service.get_llm(temperature=0.7)
            prompt = ChatPromptTemplate.from_template(cls.GENERAL_PROMPT)
            chain = prompt | llm
            res = await chain.ainvoke({"query": query})

            state["response"] = str(res.content).strip()
            state["sources"] = []
            state["agent_used"] = "General Agent"
        except Exception as e:
            state["response"] = f"Error generating response: {str(e)}"
            state["sources"] = []
            state["agent_used"] = "General Agent"

        return state
