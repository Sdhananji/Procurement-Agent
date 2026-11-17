from app.graph.nodes import intake_node, stock_check_node

requests = [
    "I need 500 pairs of Men's Black School Shoes for Colombo",
    "20 Men's Leather Formal Shoes for Colombo",
    "200 Women's Canvas Sneakers for Kandy",
    "I need some shoes",
]

for text in requests:
    print("\nREQUEST:", text)
    state = {"request_text": text}
    state.update(intake_node(state))
    if state.get("needs_clarification"):
        print("  -> asks:", state["message"])
        continue
    state.update(stock_check_node(state))
    print("  ->", state["message"])