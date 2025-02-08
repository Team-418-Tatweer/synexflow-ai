from langchain_openai import ChatOpenAI  
from ..state_management import ProductPlanningState
from ..utils import WebSearchTool


def web_search_additional_info(state: ProductPlanningState, tool: WebSearchTool) -> ProductPlanningState:
    """Perform web search to gather additional product insights"""
    query = f"Current market trends for {state.product_info.get('name', '')} product" # change name
    search_results = tool._run(query)
    state.web_search_results = search_results
    return state