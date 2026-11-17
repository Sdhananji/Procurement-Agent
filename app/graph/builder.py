from langgraph.graph import StateGraph, START, END

from app.graph.state import ProcurementState
from app.graph.nodes import intake_node, stock_check_node


def after_intake(state: ProcurementState) -> str:
    return "end" if state.get("needs_clarification") else "stock_check"


def build_graph():
    graph = StateGraph(ProcurementState)

    graph.add_node("intake", intake_node)
    graph.add_node("stock_check", stock_check_node)

    graph.add_edge(START, "intake")
    graph.add_conditional_edges(
        "intake", after_intake, {"stock_check": "stock_check", "end": END}
    )
    graph.add_edge("stock_check", END)

    return graph.compile()