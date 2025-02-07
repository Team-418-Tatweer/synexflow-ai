from state_management import ProductPlanningState
from utils import ProductEndpointTool

def fetch_product_data(state: ProductPlanningState, tool: ProductEndpointTool) -> ProductPlanningState:
    """Fetch initial product data from endpoint"""
    product_name = state.product_info.get('name', '') # change name
    product_info = tool._run(product_name)
    state.product_info.update(product_info)
    return state