from app.graph.builder import build_graph

app = build_graph()

for text in [
    "I need 500 pairs of Men's Black School Shoes for Colombo",
    "I need some shoes",
]:
    result = app.invoke({"request_text": text})
    print("\nREQUEST:", text)
    print("MESSAGE:", result["message"])
    print("STATE KEYS:", sorted(result.keys()))