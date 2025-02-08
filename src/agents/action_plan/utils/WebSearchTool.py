import json
import http.client
from langchain_core.tools import BaseTool
from typing import Dict, Any

class WebSearchTool(BaseTool):
    name: str = "web_search_tool"
    description: str = "Search the web for additional ERP-related information"
    api_key: str = "YOUR_SERPER_API_KEY"

    def _run(self, query: str) -> Dict[str, Any]:
        try:
            conn = http.client.HTTPSConnection("google.serper.dev")
            payload = json.dumps({"q": query})
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            conn.request("POST", "/search", payload, headers)
            res = conn.getresponse()
            data_bytes = res.read()
            data_str = data_bytes.decode("utf-8")
            return json.loads(data_str)
        except Exception as e:
            return {"error": f"Error in web search: {str(e)}"}
