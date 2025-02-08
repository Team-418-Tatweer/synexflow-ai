# state_management/ERPAgentState.py

from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Dict, Any

class AlertType(str, Enum):
    WEATHER = "WEATHER"
    FINANCIAL = "FINANCIAL"
    OPERATIONAL = "OPERATIONAL"
    OTHER = "OTHER"

class ERPAgentState(BaseModel):
    external_factors: List[Dict[str, Any]] = Field(default_factory=list)
    classification_results: List[Dict[str, Any]] = Field(default_factory=list)
    web_search_results: Dict[str, Any] = Field(default_factory=dict)
    final_plan: str = ""
