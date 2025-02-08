# SYNEXFLOW-AI

## Overview
SYNEXFLOW-AI is an AI-powered forecasting and planning system designed to assist businesses with sales forecasting, product planning, and alert processing. It leverages machine learning models, including LSTMs and TimeGPT, to provide accurate predictions based on historical data. The system is built using FastAPI and integrates with external APIs for enhanced predictive capabilities.

## Features  
- **Sales Forecasting:** Utilizes TimeGPT and machine learning models to predict future sales trends with high accuracy.  
- **Product Planning Workflow:** Automates product research, web data collection, and business plan generation using Agentic programming (LLMs).  
- **Alert Processing:** Implements a structured workflow for detecting, processing, and responding to alerts using Agentic programming (LLMs).  
- **REST API Interface:** Exposes endpoints for sales forecasting, business plan generation, and alert management.  

## Tech Stack  
- **Backend:** FastAPI, Python  
- **Machine Learning:** TensorFlow, Prophet, scikit-learn, TimeGPT  
- **Data Processing:** Pandas, NumPy, SciPy  
- **Agentic Programming:** LangGraph, LangChain, LangSmith  
- **Environment Management:** Python-dotenv  
- **Deployment:** Uvicorn

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/synexflow-ai.git
   cd synexflow-ai
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```
4. Set up environment variables:
   - Copy `.env.example` to `.env` and configure the required API keys.
   
## Usage
### Running the API Server
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
### API Endpoints
#### 1. Sales Forecasting
**Endpoint:** `POST /forecast`
**Request Body:**
```json
{
  "data": [
    { "Date": "2024-02-01", "TotalPrice": 1500.50 },
    { "Date": "2024-02-02", "TotalPrice": 1600.75 }
  ],
  "h": 7
}
```
**Response:**
```json
[
  { "ds": "2024-02-08", "y": 1700.20, "y_lower": 1650.00, "y_upper": 1750.00 }
]
```

#### 2. Generate Product Plan
**Endpoint:** `POST /generate-plan`
**Request Body:**
```json
{
  "name": "Smart Sensor"
}
```
**Response:**
```json
{
  "product_info": { "name": "Smart Sensor" },
  "integrated_plan": "Plan details here..."
}
```

#### 3. Alert Processing
**Endpoint:** `POST /alert-plan`
**Request Body:**
```json
{
  "alert_id": 101
}
```
**Response:**
```json
{
  "classification_results": "Results...",
  "web_search_results": "Search details...",
  "final_plan": "Final plan details..."
}
```

## Project Structure
```
SYNEXFLOW-AI
│── experimental
│   ├── agents
│   │   ├── alert_processing
│   │   ├── integration-plan
│   ├── forecast
│   │   ├── data
│   │   ├── lstm_forecasting
│   │   ├── total_sales_forecasting
│── src
│   ├── agents
│   │   ├── action_plan
│   │   ├── integration_plan
│   │── __init__.py
│   │── main.py
│── .env.example
│── .gitignore
│── LICENSE
│── README.md
│── requirement.txt
```

## License
This project is licensed under the MIT License.

## Contact
For inquiries, open an issue or contact the development team.