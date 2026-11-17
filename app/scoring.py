from datetime import date

from app.config import SCORING_WEIGHTS


def _normalise(value: float, lo: float, hi: float, higher_is_better: bool) -> float:
    """Scale a value to 0..1 relative to the other candidates."""
    if hi == lo:                       # all candidates are equal on this factor
        return 1.0
    score = (value - lo) / (hi - lo)
    return score if higher_is_better else 1.0 - score


def rank_quotations(quotations, quantity, weights=None, today=None):
    """Return (ranked, rejected). ranked is best-first."""
    weights = weights or SCORING_WEIGHTS
    if abs(sum(weights.values()) - 1.0) > 1e-6:
        raise ValueError("Scoring weights must add up to 1.0")
    today = today or date.today()

    # Step 1: hard constraints. A quotation that breaks them is rejected, not scored.
    eligible, rejected = [], []
    for q in quotations:
        if q["valid_until"] and date.fromisoformat(q["valid_until"]) < today:
            rejected.append({**q, "reason": "quotation has expired"})
        elif q["min_order_qty"] > quantity:
            rejected.append({
                **q,
                "reason": f"minimum order {q['min_order_qty']} is above the "
                          f"{quantity} pairs needed",
            })
        else:
            eligible.append(q)

    if not eligible:
        return [], rejected

    # Step 2: soft scoring of the remaining candidates.
    prices = [q["unit_price"] for q in eligible]
    days = [q["delivery_days"] for q in eligible]

    ranked = []
    for q in eligible:
        scores = {
            "price": _normalise(q["unit_price"], min(prices), max(prices), False),
            "delivery": _normalise(q["delivery_days"], min(days), max(days), False),
            "reliability": q["reliability_score"],
        }
        total = sum(weights[k] * scores[k] for k in weights)
        ranked.append({
            **q,
            "quantity": quantity,
            "total_cost": round(q["unit_price"] * quantity, 2),
            "scores": {k: round(v, 3) for k, v in scores.items()},
            "total_score": round(total, 4),
        })

    # Best score first; if tied, the cheaper total cost wins.
    ranked.sort(key=lambda r: (-r["total_score"], r["total_cost"]))
    return ranked, rejected