from ..state_management import ProductPlanningState
from ..utils import ProductEndpointTool
from typing import Optional

def fetch_product_data(state: ProductPlanningState, tool: ProductEndpointTool, product_id: Optional[int] = None) -> ProductPlanningState:
    """Fetch initial product data from endpoint"""
    product_info = tool.run_from_api(product_id)
    state.product_info.update(product_info)
    return state