from typing import Any
from ..state_management.ERPAgentState import ERPAgentState
from ..utils.WebSearchTool import WebSearchTool
from langchain_openai import ChatOpenAI

def finalize_action_plan(state: ERPAgentState, llm: ChatOpenAI) -> ERPAgentState:
    """
    Step 4: Combine alert classification, original data, and any web search results
    to recommend a final plan or confirm the recommended action.
    """
    context = {
        "external_factors": state.external_factors,
        "classification_results": state.classification_results,
        "web_search_results": state.web_search_results
    }

    prompt = f"""
Given the following context:
- External Factors Data: {context["external_factors"]}
- Alert Classifications: {context["classification_results"]}
- Web Search Results: {context["web_search_results"]}

Propose a final recommended action plan for each alert. 
Consider severity, classification, and best practices from the search results.
Present the final plan as structured text.
"""

    response = llm.invoke(prompt)
    state.final_plan = response.content
    return state