from ..state_management import ProductPlanningState
from langchain_openai import ChatOpenAI

def generate_integrated_plan(state: ProductPlanningState, llm: ChatOpenAI) -> ProductPlanningState:
    """Generate comprehensive product planning using collected information"""
    # Combine product endpoint data and web search results
    context = {
        "product_info": state.product_info,
        "web_insights": state.web_search_results
    }
    
    # Generate integrated plan prompt
    prompt = f"""Create a comprehensive product planning report based on the following information:

        Product Details:
        - Name: {context['product_info'].get('name', 'N/A')}
        - Type: {context['product_info'].get('type', 'N/A')}
        - Current Price: {context['product_info'].get('price', 'N/A')}
        - Materials: {context['product_info'].get('materials', 'N/A')}
        - Current Stock: {context['product_info'].get('current_stock', 'N/A')}
        - Predicted Stock: {context['product_info'].get('predicted_stock', 'N/A')}

        Additional Web Insights: {context['web_insights']}

        Integrated Product Plan:
    """
    
    # Generate plan using LLM
    response = llm.invoke(prompt)
    state.integrated_plan = response.content
    return state