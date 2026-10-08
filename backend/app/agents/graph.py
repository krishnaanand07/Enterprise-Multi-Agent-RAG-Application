import time
from typing import Optional
from langgraph.graph import StateGraph, END

from app.agents.state import AgentState
from app.agents.supervisor import SupervisorAgent
from app.agents.rag_agent import RAGAgent
from app.agents.data_agent import DataAgent
from app.agents.general_agent import GeneralAgent


def route_decision(state: AgentState) -> str:
    route = state.get("route", "GENERAL")
    if route == "DOCUMENT":
        return "rag_agent"
    elif route == "DATA":
        return "data_agent"
    else:
        return "general_agent"


def build_agent_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("supervisor", SupervisorAgent.route)
    workflow.add_node("rag_agent", RAGAgent.process)
    workflow.add_node("data_agent", DataAgent.process)
    workflow.add_node("general_agent", GeneralAgent.process)

    workflow.set_entry_point("supervisor")

    workflow.add_conditional_edges(
        "supervisor",
        route_decision,
        {
            "rag_agent": "rag_agent",
            "data_agent": "data_agent",
            "general_agent": "general_agent",
        }
    )

    workflow.add_edge("rag_agent", END)
    workflow.add_edge("data_agent", END)
    workflow.add_edge("general_agent", END)

    return workflow.compile()


agent_graph = build_agent_graph()


async def run_agent_workflow(
    query: str, 
    user_id: str, 
    conversation_id: str, 
    selected_document_id: Optional[str] = None
) -> AgentState:
    start_time = time.time()

    initial_state: AgentState = {
        "query": query,
        "user_id": user_id,
        "conversation_id": conversation_id,
        "selected_document_id": selected_document_id,
        "route": None,
        "response": None,
        "sources": [],
        "agent_used": None,
        "metrics": None
    }

    final_state = await agent_graph.ainvoke(initial_state)

    duration_ms = round((time.time() - start_time) * 1000, 2)
    sources_count = len(final_state.get("sources") or [])

    final_state["metrics"] = {
        "response_time_ms": duration_ms,
        "sources_count": sources_count,
        "agent_selected": final_state.get("agent_used", "General Agent"),
        "route": final_state.get("route", "GENERAL")
    }

    return final_state
