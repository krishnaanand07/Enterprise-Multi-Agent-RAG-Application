"""
Supervisor Agent. Routes queries and manages the LangGraph state machine.
"""
from loguru import logger
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage

from app.agents.state import AgentState
from app.agents.rag_agent import rag_agent
from app.agents.sql_agent import sql_agent
from app.services.langchain_llm import get_llm

class SupervisorAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.0)
        self.graph = self._build_graph()
        
    async def route_query_node(self, state: AgentState) -> dict:
        """Decides which agent should handle the query."""
        logger.info(f"Supervisor evaluating query: {state['question']}")
        
        system_prompt = (
            "You are an enterprise AI routing supervisor. Analyze the user's question and decide where to direct it.\n"
            "- If the question asks about general document concepts, reading uploaded PDF/DOCX content, or textual research summaries, return 'RAG'.\n"
            "- If the question asks about data charts, plotting, visualization, graphs (bar chart, pie chart, line graph), table statistics, comparisons, counts, distributions, metrics, or SQL database records, return 'SQL'.\n"
            "Return ONLY the word 'RAG' or 'SQL'."
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=state['question'])
        ]
        
        response = await self.llm.ainvoke(messages)
        decision = response.content.strip().upper()
        
        if decision not in ["RAG", "SQL"]:
            decision = "RAG" # Default fallback
            
        logger.info(f"Supervisor routing to: {decision}")
        return {"next_agent": decision}
        
    def _route_condition(self, state: AgentState) -> str:
        """Conditional edge routing function."""
        return state.get("next_agent", "RAG")

    def _build_graph(self):
        """Builds the LangGraph computational graph."""
        workflow = StateGraph(AgentState)
        
        # Add Nodes
        workflow.add_node("supervisor", self.route_query_node)
        
        # RAG Nodes
        workflow.add_node("rag_retrieve", rag_agent.retrieve_node)
        workflow.add_node("rag_generate", rag_agent.generate_node)
        
        # SQL Nodes
        workflow.add_node("sql_generate_query", sql_agent.generate_query_node)
        workflow.add_node("sql_execute_format", sql_agent.execute_and_format_node)
        
        # Define Edges
        workflow.set_entry_point("supervisor")
        
        # Conditional routing from supervisor
        workflow.add_conditional_edges(
            "supervisor",
            self._route_condition,
            {
                "RAG": "rag_retrieve",
                "SQL": "sql_generate_query"
            }
        )
        
        # RAG Path
        workflow.add_edge("rag_retrieve", "rag_generate")
        workflow.add_edge("rag_generate", END)
        
        # SQL Path
        workflow.add_edge("sql_generate_query", "sql_execute_format")
        workflow.add_edge("sql_execute_format", END)
        
        # Compile graph
        return workflow.compile()
        
    async def process_query(self, query: str, user_id: str) -> dict:
        """Entry point for the API to call the graph."""
        initial_state = {
            "user_id": user_id,
            "question": query,
            "chat_history": [],
            "next_agent": None,
            "retrieved_documents": [],
            "sql_query": None,
            "sql_result": None,
            "final_answer": None,
            "citations": [],
            "chart_data": None
        }
        
        # Execute the graph
        final_state = await self.graph.ainvoke(initial_state)
        
        return {
            "answer": final_state.get("final_answer"),
            "agent_used": final_state.get("next_agent"),
            "citations": final_state.get("citations", []),
            "chart_data": final_state.get("chart_data", None)
        }

supervisor = SupervisorAgent()
