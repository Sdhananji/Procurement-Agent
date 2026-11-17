from langgraph.graph import StateGraph, START, END

from app.graph.state import ProcurementState
from app.graph.nodes import (
    intake_node, stock_check_node, compare_node, explain_node,
)


def after_intake(state: ProcurementState) -> str:
    return "end" if state.get("needs_clarification") else "stock_check"


def after_stock(state: ProcurementState) -> str:
    return "compare" if state["quantity_to_order"] > 0 else "end"


def after_compare(state: ProcurementState) -> str:
    return "end" if state.get("needs_human_review") else "explain"


def build_graph():
    graph = StateGraph(ProcurementState)

    graph.add_node("intake", intake_node)
    graph.add_node("stock_check", stock_check_node)
    graph.add_node("compare", compare_node)
    graph.add_node("explain", explain_node)

    graph.add_edge(START, "intake")
    graph.add_conditional_edges(
        "intake", after_intake, {"stock_check": "stock_check", "end": END}
    )
    graph.add_conditional_edges(
        "stock_check", after_stock, {"compare": "compare", "end": END}
    )
    graph.add_conditional_edges(
        "compare", after_compare, {"explain": "explain", "end": END}
    )
    graph.add_edge("explain", END)

    return graph.compile()