from typing import TypedDict


class ProcurementState(TypedDict, total=False):
    # Input
    request_text: str

    # Filled by the intake node
    request_id: int
    sku: str
    product_id: int
    product_name: str
    quantity_requested: int
    branch: str
    needs_clarification: bool

    # Filled by the stock check node
    stock_available: int
    quantity_to_order: int

    # Filled by later nodes (we will use these soon)
    quotations: list
    recommended_supplier: dict
    purchase_order: dict
    approval_status: str

    # Human-readable status for the user
    message: str