from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GEMINI_MODEL
from app.db import queries
from app.graph.state import ProcurementState

llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0)


class ParsedRequest(BaseModel):
    sku: str | None = Field(None, description="SKU chosen from the catalog, or null")
    quantity: int | None = Field(None, description="Number of pairs requested, or null")
    branch: str | None = Field(None, description="Branch name from the list, or null")
    needs_clarification: bool = Field(
        description="True if product, quantity or branch is missing or ambiguous"
    )
    clarification_question: str | None = Field(
        None, description="One short question to ask the employee, if needed"
    )


parser = llm.with_structured_output(ParsedRequest)


def intake_node(state: ProcurementState) -> dict:
    products = queries.get_products()
    branches = queries.get_branches()

    catalog = "\n".join(f"- {p['sku']}: {p['name']}" for p in products)
    prompt = f"""You extract details from an employee's purchase request.

Product catalog:
{catalog}

Branches: {", ".join(branches)}

Rules:
- Choose the sku ONLY from the catalog above.
- If the product, quantity or branch is missing or unclear, set
  needs_clarification to true and ask one short question. Do not guess.

Request: {state["request_text"]}"""

    parsed = parser.invoke(prompt)

    # Never trust LLM output blindly: validate it with code.
    product = next((p for p in products if p["sku"] == parsed.sku), None)
    valid = (
        product is not None
        and parsed.branch in branches
        and parsed.quantity is not None
        and parsed.quantity > 0
    )

    if parsed.needs_clarification or not valid:
        question = parsed.clarification_question or (
            "Please tell me the product, quantity and branch."
        )
        return {"needs_clarification": True, "message": question}

    request_id = queries.create_request(state["request_text"], parsed.branch)
    queries.log_event(
        "purchase_request", request_id, "request_parsed", "intake_node",
        {"sku": parsed.sku, "quantity": parsed.quantity, "branch": parsed.branch},
    )

    return {
        "request_id": request_id,
        "sku": product["sku"],
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity_requested": parsed.quantity,
        "branch": parsed.branch,
        "needs_clarification": False,
    }

def stock_check_node(state: ProcurementState) -> dict:
    row = queries.get_stock(state["product_id"], state["branch"])
    available = row["quantity"] if row else 0
    to_order = max(state["quantity_requested"] - available, 0)

    queries.log_event(
        "purchase_request", state["request_id"], "stock_checked", "stock_check_node",
        {"available": available, "requested": state["quantity_requested"],
         "to_order": to_order},
    )

    if to_order == 0:
        message = f"{available} pairs already in stock at {state['branch']}. No purchase needed."
    else:
        message = (f"{available} in stock at {state['branch']}; "
                   f"need to order {to_order} more pairs.")

    return {"stock_available": available, "quantity_to_order": to_order,
            "message": message}