from app.graph.builder import build_graph

app = build_graph()

requests = [
    "I need 500 pairs of Men's Black School Shoes for Colombo",
    "200 Women's Canvas Sneakers for Kandy",
    "20 Men's Leather Formal Shoes for Colombo",
    "150 Men's Black School Shoes for Colombo",
    "I need some shoes",
]

for text in requests:
    result = app.invoke({"request_text": text})
    print("\n" + "=" * 70)
    print("REQUEST:", text)
    print("MESSAGE:", result["message"])
    best = result.get("recommended_supplier")
    if best:
        print(f"WINNER : {best['supplier_name']} | Rs {best['unit_price']}/pair | "
              f"{best['delivery_days']} days | total Rs {best['total_cost']:,.2f} | "
              f"score {best['total_score']}")