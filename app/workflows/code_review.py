# app/workflows/code_review.py

def get_code_review_graph_definition():
    """
    Returns (start_node, nodes, edges) for the Code Review workflow.

    Nodes:
      extract -> complexity -> issues -> quality_gate
      quality_gate:
          if quality_score >= threshold -> END
          else -> improve -> quality_gate (loop)
    """

    # Node name → tool name
    nodes = {
        "extract": "extract_functions",
        "complexity": "check_complexity",
        "issues": "detect_issues",
        "improve": "suggest_improvements",
        "quality_gate": "final_review"
    }

    # Workflow edges
    edges = {
        "extract": "complexity",
        "complexity": "issues",
        "issues": "quality_gate",

        "quality_gate": {    # branching (looping)
            "type": "branch",
            "condition_key": "quality_score",
            "operator": ">=",
            "value": 0.8,
            "true_next": "END",
            "false_next": "improve"
        },

        "improve": "quality_gate"
    }

    start_node = "extract"
    return start_node, nodes, edges
