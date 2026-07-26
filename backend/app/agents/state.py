"""
LangGraph State definitions.
"""
from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    """The state passed between all nodes in the graph."""
    user_id: str
    question: str
    chat_history: List[Dict[str, str]]
    
    # Internal routing and context
    next_agent: Optional[str]
    retrieved_documents: List[Dict[str, Any]]
    sql_query: Optional[str]
    sql_result: Optional[str]
    
    # Final Output
    final_answer: Optional[str]
    citations: List[Dict[str, Any]]
    chart_data: Optional[Dict[str, Any]]
