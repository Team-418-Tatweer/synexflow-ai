from ..state_management.ERPAgentState import ERPAgentState
from langchain_openai import ChatOpenAI
import json

def classify_alert_messages(state: ERPAgentState, llm: ChatOpenAI) -> ERPAgentState:
    """
    Step 2: Use LLM to classify alerts by type, severity, etc.
    """
    prompt_parts = []
    for factor in state.external_factors:
        alert = factor.get("Alert", {})
        prompt_parts.append(f"""
AlertID: {alert.get("AlertID")}
Type: {alert.get("Type")}
Severity: {alert.get("Severity")}
Description: {alert.get("Description")}
        """)
    prompt_str = "\n".join(prompt_parts)

    prompt = f"""
You are an expert in classifying ERP alerts. 
We have the following alerts:

{prompt_str}

Valid AlertType categories are: WEATHER, FINANCIAL, OPERATIONAL, OTHER.

For each alert, output the most appropriate AlertType based on its info.
Provide your answer as a JSON list of objects in the format:
[{{"AlertID": <id>, "Classification": <AlertType>}}, ...]
"""
    response = llm.invoke(prompt)
    try:
        classification_data = json.loads(response.content)
        state.classification_results = classification_data
    except:
        state.classification_results = []
    return state