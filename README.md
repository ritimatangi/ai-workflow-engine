 AI Workflow Engine (FastAPI + Python)

This project is a simple workflow (graph) engine built using Python and FastAPI.  
It was created as part of the **AI Engineering Internship Assignment**.

The engine supports:
- Nodes (Python functions)
- Shared state passing between nodes
- Graph edges (defining which step runs next)
- Looping until a condition is met
- Basic branching
- Running a workflow through FastAPI APIs

---
 Features

 Node Registry
Each node is registered with a name so the engine can run the function dynamically.

 Graph Execution
Nodes are executed based on a directed graph that defines:
- start node  
- next node  
- end node  
- looping logic  

 FastAPI Endpoints
The system exposes three APIs:

 POST /graph/create
Create a workflow graph.

 POST /graph/run
Run a graph with an initial state.

 GET /graph/state/{run_id}
Get the latest state of a particular run.

---

 Example Workflow Implemented

A simple Code Review Workflow:

1. Extract functions  
2. Calculate complexity  
3. Detect issues  
4. Suggest improvements  
5. Loop until `quality_score ≥ 90`  

This shows how state flows and changes across steps.

---

 Running the Project

 Install dependencies:
```bash
pip install -r requirements.txt
### Run the FastAPI Server

After installing dependencies, start the backend server using:

```bash
uvicorn app.main:app --reload
This will start the API at:

arduino
Copy code
http://localhost:8000
Open API Documentation (Swagger UI)
You can test all APIs using the automatically generated docs:

👉 http://localhost:8000/docs

This page shows the endpoints:

POST /graph/create

POST /graph/run

GET /graph/state/{run_id}

These APIs allow you to create, run, and inspect your workflow engine.

yaml
Copy code

---

# 📌 Where to paste?

1. Open your README.md  
2. Scroll to the bottom (after `pip install -r requirements.txt`)  
3. Paste the above block  
4. Click **Commit changes**

---

# 🎉 After this, your README is complete and looks exactly like what companies expect.

If you want, I can check your README after you paste it.
