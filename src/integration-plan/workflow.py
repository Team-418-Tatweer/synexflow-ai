from utils import ProductEndpointTool, WebSearchTool
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
import http.client

def build_product_planning_workflow():
    """Construct the LangGraph workflow for product planning"""
    workflow = StateGraph(ProductPlanningState)
    
    # Define tools
    product_tool = ProductEndpointTool()
    web_search_tool = WebSearchTool()
    
    llm = ChatOpenAI(
        model="deepseek/deepseek-r1-distill-llama-70b:free",  # use "gpt-4-turbo" if that's what you prefer
        openai_api_key=DEEPSEEK_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1"
    )

    
    # Add nodes
    workflow.add_node("fetch_product_data", 
                      lambda state: fetch_product_data(state, product_tool))
    workflow.add_node("web_search", 
                      lambda state: web_search_additional_info(state, web_search_tool))
    workflow.add_node("generate_plan", 
                      lambda state: generate_integrated_plan(state, llm))
    
    # Define edges
    workflow.set_entry_point("fetch_product_data")
    workflow.add_edge("fetch_product_data", "web_search")
    workflow.add_edge("web_search", "generate_plan")
    workflow.add_edge("generate_plan", END)
    
    # Compile the graph
    return workflow.compile()