from app.engine.registry import registry
import ast
import radon.complexity as radon_cc
import random

THRESHOLD = 7

async def extract_functions(state):
    code = state.data.get("code", "")
    parsed = ast.parse(code)
    functions = [node.name for node in ast.walk(parsed) if isinstance(node, ast.FunctionDef)]
    state.data["functions"] = functions
    return {"next": "check_complexity"}

async def check_complexity(state):
    code = state.data.get("code", "")
    blocks = radon_cc.cc_visit(code)
    complexity_scores = {b.name: b.complexity for b in blocks}
    state.data["complexity"] = complexity_scores
    return {"next": "detect_issues"}

async def detect_issues(state):
    issues = []
    for function, score in state.data.get("complexity", {}).items():
        if score > 10:
            issues.append(f"Function '{function}' is too complex.")
    state.data["issues"] = issues
    return {"next": "suggest_improvements"}

async def suggest_improvements(state):
    issues = state.data.get("issues", [])
    suggestions = []
    for issue in issues:
        suggestions.append("Consider breaking the function into smaller components.")
    current_score = state.data.get("quality_score", 0)
    new_score = current_score + random.randint(1, 3)
    state.data["quality_score"] = new_score
    if new_score >= THRESHOLD:
        return "STOP"
    return {"next": "extract"}

def get_code_review_workflow():
    nodes = {
        "extract": extract_functions,
        "check_complexity": check_complexity,
        "detect_issues": detect_issues,
        "suggest_improvements": suggest_improvements,
    }
    edges = {
        "extract": "check_complexity",
        "check_complexity": "detect_issues",
        "detect_issues": "suggest_improvements",
        "suggest_improvements": "extract",
    }
    return nodes, edges, "extract"
