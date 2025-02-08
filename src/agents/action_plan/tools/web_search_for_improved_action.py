from typing import Any
from ..state_management.ERPAgentState import ERPAgentState
from ..utils.WebSearchTool import WebSearchTool

def web_search_for_improved_action(state: ERPAgentState, tool: WebSearchTool) -> ERPAgentState:
    """
    Step 3: Perform web searches to gather additional info for each alert,
    to refine or validate the best action to take.
    """
    # For demonstration, let's just pick the first classification and do a search:
    # (In real usage, you might loop through all classifications or pick critical ones.)
    if not state.classification_results:
        return state

    first_classification = state.classification_results[0]
    classification_type = first_classification.get("Classification", "OTHER")
    search_query = f"Best practices to handle {classification_type} ERP alert"
    search_results = tool._run(search_query)
    state.web_search_results = search_results
    return state