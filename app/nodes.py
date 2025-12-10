# app/nodes.py
from typing import Dict, Any, List

from app.registry import register_tool

State = Dict[str, Any]


@register_tool("extract_functions")
def extract_functions(state: State) -> State:
    """
    Extract function names from Python code.
    Very simple parsing: detects lines starting with 'def '.
    """
    code: str = state.get("code", "")
    functions: List[str] = []

    for line in code.splitlines():
        line = line.strip()
        if line.startswith("def "):
            # Example: def add(a, b):
            fn_name = line.split("(")[0].replace("def ", "").strip()
            functions.append(fn_name)

    state["functions"] = functions
    state.setdefault("quality_score", 0.0)
    return state


@register_tool("check_complexity")
def check_complexity(state: State) -> State:
    """
    Naive cyclomatic complexity based on keywords.
    """
    code: str = state.get("code", "")
    complexity = (
        code.count("if ") +
        code.count("for ") +
        code.count("while ") +
        code.count("elif ") +
        code.count("and ") +
        code.count("or ")
    )
    state["complexity"] = complexity
    return state


@register_tool("detect_issues")
def detect_issues(state: State) -> State:
    """
    Basic issue detection:
    - Tabs mixed with spaces
    - Long file
    - TODO comments
    """
    code = state.get("code", "")
    issues = 0
    suggestions = []

    if "\t" in code:
        issues += 1
        suggestions.append("Avoid mixing tabs and spaces.")

    if len(code.splitlines()) > 50:
        issues += 1
        suggestions.append("File is too long — consider splitting.")

    if "TODO" in code:
        issues += 1
        suggestions.append("Resolve TODO comments.")

    state["issues"] = issues
    state["suggestions"] = suggestions
    return state


@register_tool("suggest_improvements")
def suggest_improvements(state: State) -> State:
    """
    Improves quality score based on issues and complexity.
    """
    quality = state.get("quality_score", 0.0)
    issues = state.get("issues", 0)
    complexity = state.get("complexity", 0)

    improvement = 0.3
    if issues > 0 or complexity > 10:
        improvement = 0.2

    state["quality_score"] = min(1.0, quality + improvement)

    state.setdefault("suggestions", [])
    if issues > 0:
        state["suggestions"].append("Fix formatting and TODOs.")
    if complexity > 10:
        state["suggestions"].append("Refactor to reduce complexity.")

    return state


@register_tool("final_review")
def final_review(state: State) -> State:
    """
    Final check — assigns status based on threshold.
    """
    score = state.get("quality_score", 0.0)
    threshold = state.get("threshold", 0.8)

    if score >= threshold:
        state["status"] = "approved"
    else:
        state["status"] = "needs_improvement"

    return state
