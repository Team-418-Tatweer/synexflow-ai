from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

from .state_management.ERPAgentState import ERPAgentState
from .utils.ERPDataTool import ERPDataTool
from .utils.WebSearchTool import WebSearchTool
from .tools.fetch_erp_data import fetch_erp_data
from .tools.classify_alert_messages import classify_alert_messages
from .tools.web_search_for_improved_action import web_search_for_improved_action
from .tools.finalize_action_plan import finalize_action_plan


def build_erp_workflow(alert_id: Optional[int] = None):
    """
    Constructs the LangGraph workflow for ERP data retrieval,
    alert classification, web search, and final plan creation.
    """
    workflow = StateGraph(ERPAgentState)
    
    # Tools
    erp_tool = ERPDataTool()
    web_search_tool = WebSearchTool()

    # Replace with your actual LLM details or your custom config
    # For demonstration, we use a stand-in model name.
    llm = ChatOpenAI(
        model="deepseek/deepseek-r1-distill-llama-70b:free",
        openai_api_key=DEEPSEEK_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1"
    )

    # Add nodes (steps)
    workflow.add_node("fetch_erp_data", lambda state: fetch_erp_data(state, erp_tool, alert_id=alert_id))
    workflow.add_node("classify_alerts", lambda state: classify_alert_messages(state, llm))
    workflow.add_node("web_search", lambda state: web_search_for_improved_action(state, web_search_tool))
    workflow.add_node("finalize_plan", lambda state: finalize_action_plan(state, llm))

    # Define transitions
    workflow.set_entry_point("fetch_erp_data")
    workflow.add_edge("fetch_erp_data", "classify_alerts")
    workflow.add_edge("classify_alerts", "web_search")
    workflow.add_edge("web_search", "finalize_plan")
    workflow.add_edge("finalize_plan", END)

    # Compile the graph
    return workflow.compile()

