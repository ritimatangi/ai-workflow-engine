from fastapi import FastAPI, HTTPException

from app.graph_engine import GraphEngine
from app.models import GraphCreateRequest, GraphRunRequest
from app.workflows.code_review import get_code_review_graph_definition

import app.nodes   # ✅ THIS REGISTERS ALL TOOLS (VERY IMPORTANT)

app = FastAPI(title="AI Workflow Engine")

engine = GraphEngine()

# Load default workflow
start_node, nodes, edges = get_code_review_graph_definition()
engine.create_graph(
    graph_id="code_review",
    start_node=start_node,
    nodes=nodes,
    edges=edges,
)


@app.post("/graph/create")
def create_graph(payload: GraphCreateRequest):
    engine.create_graph(
        graph_id=payload.graph_id,
        start_node=payload.start_node,
        nodes=payload.nodes,
        edges=payload.edges,
    )
    return {"graph_id": payload.graph_id}


@app.post("/graph/run")
def run_graph(payload: GraphRunRequest):
    if payload.graph_id not in engine.graphs:
        raise HTTPException(status_code=404, detail="Graph not found")

    run_id, final_state, log, finished = engine.run_graph(
        graph_id=payload.graph_id,
        initial_state=payload.initial_state,
    )
    return {
        "run_id": run_id,
        "finished": finished,
        "final_state": final_state,
        "log": log,
    }


@app.get("/graph/state/{run_id}")
def get_graph_state(run_id: str):
    run = engine.get_run_state(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run
