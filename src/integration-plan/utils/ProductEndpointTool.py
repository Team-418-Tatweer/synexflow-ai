import json
from typing import Dict, Any
import requests
from langchain_core.tools import BaseTool
from pydantic import Field
from pathlib import Path

class ProductEndpointTool(BaseTool):
    name: str = "product_endpoint_tool"
    description: str = "Fetch product information from endpoint"
    json_file: Path = Field(default=Path("product_catalog.json"))

    # def _run(self, product_name: str) -> Dict[str, Any]:
    #     try:
    #         # Replace with your actual product endpoint
    #         # response = requests.get(f"https://your-product-endpoint.com/product?name={product_name}")
    #         response = json.load()
    #         return response.json()
    #     except Exception as e:
    #         return f"Error fetching product info: {str(e)}"
        
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