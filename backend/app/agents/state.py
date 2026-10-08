from typing import TypedDict, List, Dict, Any, Optional


class AgentState(TypedDict):
    query: str
    user_id: str
    conversation_id: str
    selected_document_id: Optional[str]     # Optional doc filter for Document-Scoped Chat
    route: Optional[str]                   # "DOCUMENT", "DATA", "GENERAL"
    response: Optional[str]                # Final answer string
    sources: Optional[List[Dict[str, Any]]] # Array of citation objects
    agent_used: Optional[str]
    metrics: Optional[Dict[str, Any]]      # Observability metrics (latency_ms, sources_count, etc.)
