from typing import Any, Optional
from ..state_management.ERPAgentState import ERPAgentState
from ..utils.ERPDataTool import ERPDataTool
from dotenv import load_dotenv
import os

load_dotenv()

SERVER_ENDPOINT = os.getenv('SERVER_ENDPOINT')

def fetch_erp_data(state: ERPAgentState, tool: ERPDataTool, alert_id: Optional[int] = None) -> ERPAgentState:
    """
    Step 
    : Retrieve external factor data from the ERP (simulated JSON file).
    """
    # We might pass a parameter or factor ID into _run, but for simplicity
    # let's just fetch everything:
    data = tool.run_from_api(alert_id, SERVER_ENDPOINT)

    state.external_factors = data
    return state