# app/models.py
from typing import Dict, Any
from pydantic import BaseModel


class GraphCreateRequest(BaseModel):
    graph_id: str
    start_node: str
    nodes: Dict[str, str]     # node_name -> tool_name
    edges: Dict[str, Any]     # node_name -> next node OR branch object


class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]
