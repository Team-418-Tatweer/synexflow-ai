import json
from langchain_core.tools import BaseTool
import http.client

class WebSearchTool(BaseTool):
    name: str = "web_search_tool"
    description: str = "Search the web for additional product information"

    def _run(self, query: str) -> str:
        try:
            # Replace with your actual web search API endpoint
            conn = http.client.HTTPSConnection("google.serper.dev")
            payload = json.dumps({
                "q": query
            })
            headers = {
                'X-API-KEY': '9e47c410e6f594092fd799e42873d35a38de67d4',
                'Content-Type': 'application/json'
            }
            conn.request("POST", "/search", payload, headers)
            res = conn.getresponse()
            data_bytes = res.read()
            data_str = data_bytes.decode("utf-8")
            # Correctly parse the JSON string into a Python dictionary
            data = json.loads(data_str)
            return data
        except Exception as e:
            return f"Error in web search: {str(e)}"