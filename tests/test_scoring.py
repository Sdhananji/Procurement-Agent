import pytest
from datetime import date

from app.scoring import rank_quotations

QUOTES = [
    {"supplier_name": "A", "supplier_id": 1, "reliability_score": 0.90,
     "unit_price": 2500.0, "delivery_days": 14, "min_order_qty": 100, "valid_until": None},
    {"supplier_name": "B", "supplier_id": 2, "reliability_score": 0.75,
     "unit_price": 2300.0, "delivery_days": 25, "min_order_qty": 200, "valid_until": None},
    {"supplier_name": "C", "supplier_id": 3, "reliability_score": 0.85,
     "unit_price": 2625.0, "delivery_days": 10, "min_order_qty": 50, "valid_until": None},
]


def test_cheapest_wins_with_default_weights():
    ranked, _ = rank_quotations(QUOTES, 386)
    assert ranked[0]["supplier_name"] == "B"


def test_weights_change_the_winner():
    speed_first = {"price": 0.1, "delivery": 0.8, "reliability": 0.1}
    ranked, _ = rank_quotations(QUOTES, 386, weights=speed_first)
    assert ranked[0]["supplier_name"] == "C"


def test_minimum_order_quantity_excludes_supplier():
    ranked, rejected = rank_quotations(QUOTES, 191)
    assert "B" not in [r["supplier_name"] for r in ranked]
    assert rejected[0]["supplier_name"] == "B"


def test_no_supplier_can_fulfil_small_order():
    ranked, rejected = rank_quotations(QUOTES, 20)
    assert ranked == []
    assert len(rejected) == 3


def test_expired_quotation_is_rejected():
    old = [{**QUOTES[0], "valid_until": "2020-01-01"}]
    ranked, rejected = rank_quotations(old, 386, today=date(2026, 11, 17))
    assert ranked == []
    assert rejected[0]["reason"] == "quotation has expired"


def test_weights_must_sum_to_one():
    with pytest.raises(ValueError):
        rank_quotations(QUOTES, 386, weights={"price": 0.9, "delivery": 0.9, "reliability": 0.9})