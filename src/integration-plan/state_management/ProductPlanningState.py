from typing import Dict, Any
from pydantic import BaseModel, Field

class ProductPlanningState(BaseModel):
    product_info: Dict[str, Any] = Field(default_factory=dict)
    integrated_plan: str = ""
    web_search_results: Dict[str, Any] = {}