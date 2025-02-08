import json
from typing import List, Dict, Any
import requests
from langchain_core.tools import BaseTool
from pydantic import Field
from pathlib import Path

class ProductEndpointTool(BaseTool):
    name: str = "product_endpoint_tool"
    description: str = "Fetch product information from endpoint"
    json_file: Path = Field(default=Path("product_catalog.json"))
        
    def _run(self, product_name: str) -> Dict[str, Any]:
        try:
            # Load JSON from file
            with open(self.json_file, 'r') as f:
                products = json.load(f)
            
            # Filter products by name (exact match)
            matches = [p for p in products if p["name"] == product_name]
            
            return {
                "count": len(matches),
                "results": matches
            }
            
        except FileNotFoundError:
            return {"error": f"File {self.json_file} not found"}
        except json.JSONDecodeError:
            return {"error": f"Invalid JSON format in {self.json_file}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
        
    def run_from_api(self, product_id: int, base_url: str) -> List[Dict[str, Any]]:
        """
        Fetch ERP data from a remote endpoint (e.g., an internal API).
        We'll assume there's an endpoint like: GET /alerts/{alert_id}.
        Adjust to match your actual API's structure.
        """
        url = f"{base_url}/product/{product_id}"  # e.g. "https://erp.example.com/alerts/101"
        
        try:
            response = requests.get(url, timeout=10)  # Optional: set a timeout
            response.raise_for_status()  # Raise an exception for 4xx/5xx errors
            
            data = response.json()
            
            # Convert single dict to a list for uniformity, or adapt as needed
            return [data] if isinstance(data, dict) else data
        except requests.RequestException as e:
            return [{"error": f"Network or HTTP error: {str(e)}"}]
        except ValueError as e:
            # This typically means invalid JSON was returned
            return [{"error": f"JSON parse error: {str(e)}"}]
        except Exception as e:
            return [{"error": f"Unexpected error: {str(e)}"}]