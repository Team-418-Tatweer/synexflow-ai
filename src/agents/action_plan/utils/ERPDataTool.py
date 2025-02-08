import json
import requests
from pathlib import Path
from typing import List, Dict, Any
from langchain_core.tools import BaseTool
from pydantic import Field

class ERPDataTool(BaseTool):
    """
    Simulates an ERP endpoint by loading data from 'erp_data.json' 
    or fetching from a real API.
    """
    name: str = "erp_data_tool"
    description: str = "Fetch ERP data related to external factors."
    json_file: Path = Field(default=Path("erp_data.json"))

    def _run(self, query: str) -> List[Dict[str, Any]]:
        """
        'query' can be used to filter data or specify what data we want.
        For simplicity, we just return all external_factors from JSON.
        """
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return [{"error": f"File {self.json_file} not found"}]
        except json.JSONDecodeError:
            return [{"error": f"Invalid JSON format in {self.json_file}"}]
        except Exception as e:
            return [{"error": f"Unexpected error: {str(e)}"}]
    
    def run_from_api(self, alert_id: int, base_url: str) -> List[Dict[str, Any]]:
        """
        Fetch ERP data from a remote endpoint (e.g., an internal API).
        We'll assume there's an endpoint like: GET /alerts/{alert_id}.
        """
        url = f"{base_url}/alerts/{alert_id}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [data] if isinstance(data, dict) else data
        except requests.RequestException as e:
            return [{"error": f"Network/HTTP error: {str(e)}"}]
        except ValueError as e:
            return [{"error": f"JSON parse error: {str(e)}"}]
        except Exception as e:
            return [{"error": f"Unexpected error: {str(e)}"}]
