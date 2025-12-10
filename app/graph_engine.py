# app/graph_engine.py
from typing import Dict, Any, List, Optional
import uuid

from app.registry import get_tool


class GraphEngine:
    def __init__(self):
        # Stores graphs: graph_id -> {start_node, nodes, edges}
        self.graphs: Dict[str, Dict[str, Any]] = {}
        # Stores runs: run_id -> {graph_id, state, log, finished}
        self.runs: Dict[str, Dict[str, Any]] = {}

    def create_graph(
        self,
        graph_id: str,
        start_node: str,
        nodes: Dict[str, str],
        edges: Dict[str, Any],
    ) -> str:
        """Register a new graph (workflow)."""
        self.graphs[graph_id] = {
            "start_node": start_node,
            "nodes": nodes,
            "edges": edges,
        }
        return graph_id

    def _evaluate_branch(self, edge: Dict[str, Any], state: Dict[str, Any]) -> Optional[str]:
        """
        Branching logic.

        Example edge format:
        {
            "type": "branch",
            "condition_key": "quality_score",
            "operator": ">=",
            "value": 0.8,
            "true_next": "END",
            "false_next": "improve"
        }
        """
        key = edge["condition_key"]
        op = edge["operator"]
        value = edge["value"]
        current_val = state.get(key)

        if op == ">=":
            result = current_val >= value
        elif op == ">":
            result = current_val > value
        elif op == "<=":
            result = current_val <= value
        elif op == "<":
            result = current_val < value
        elif op == "==":
            result = current_val == value
        elif op == "!=":
            result = current_val != value
        else:
            raise ValueError(f"Unsupported operator: {op}")

        next_node = edge["true_next"] if result else edge["false_next"]
        return None if next_node == "END" else next_node

    def run_graph(
        self,
        graph_id: str,
        initial_state: Dict[str, Any],
        max_steps: int = 100,
    ):
        """
        Execute a graph workflow from start to finish.
        """
        if graph_id not in self.graphs:
            raise KeyError(f"Graph '{graph_id}' not found")

        run_id = str(uuid.uuid4())
        graph = self.graphs[graph_id]

        nodes = graph["nodes"]
        edges = graph["edges"]
        current = graph["start_node"]
        state = dict(initial_state)
        log: List[str] = []

        steps = 0
        while current is not None and steps < max_steps:
            steps += 1

            if current not in nodes:
                raise KeyError(f"Node '{current}' not found in graph '{graph_id}'")

            tool_name = nodes[current]
            tool_fn = get_tool(tool_name)

            log.append(f"Running node '{current}' (tool='{tool_name}')")
            state = tool_fn(state)

            edge = edges.get(current)
            if edge is None:
                current = None
                break

            if isinstance(edge, str):
                current = None if edge == "END" else edge

            elif isinstance(edge, Dict) and edge.get("type") == "branch":
                current = self._evaluate_branch(edge, state)

            else:
                raise ValueError(f"Invalid edge format: {edge}")

        finished = current is None

        self.runs[run_id] = {
            "graph_id": graph_id,
            "state": state,
            "log": log,
            "finished": finished,
        }

        return run_id, state, log, finished

    def get_run_state(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Return stored state & log for a previous workflow run."""
        return self.runs.get(run_id)
