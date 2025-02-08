from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

from datetime import datetime
from typing import Optional

from agents.integration_plan.integration_plan_workflow import build_product_planning_workflow
from agents.action_plan.action_plan_workflow import build_erp_workflow
from agents.integration_plan.state_management.ProductPlanningState import ProductPlanningState
from agents.action_plan.state_management.ERPAgentState import ERPAgentState

from nixtla import NixtlaClient

load_dotenv()

SERVER_ENDPOINT = os.getenv('SERVER_ENDPOINT')
TIMEGPT_API_KEY = os.getenv('TIMEGPT_API_KEY')

client = NixtlaClient(
    api_key=TIMEGPT_API_KEY
)

app = FastAPI()

# ------------------------------------------------------------
# Pydantic models
# ------------------------------------------------------------
class ProductRequest(BaseModel):
    name: str

class AlertRequest(BaseModel):
    alert_id: Optional[int] = None

class TrainData(BaseModel):
    Date: datetime
    TotalPrice: float

class ForecastRequest(BaseModel):
    data: List[TrainData]
    h: int = 7  # default horizon

class ForecastResponse(BaseModel):
    ds: datetime
    y: float
    y_lower: Optional[float] = None
    y_upper: Optional[float] = None

# -----------------------------------------------------------------
# ENDPOINT: Train
# -----------------------------------------------------------------
@app.post("/forecast", response_model=List[ForecastResponse])
async def train_and_forecast(request: ForecastRequest):
    """
    1) Receive historical data + forecast horizon h in one request.
    2) Validate and save data to CSV.
    3) Call TimeGPT to get the next h predictions.
    4) Return the forecast as JSON with error handling.
    """
    # Convert input list of TrainData to a DataFrame
    try:
        df_in = pd.DataFrame([d.dict() for d in request.data])
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not parse input data into DataFrame: {str(e)}"
        )

    # Validate your data
    if len(df_in) < 2:
        raise HTTPException(
            status_code=400,
            detail="Not enough data points. Provide at least 2 or more."
        )
    if df_in["TotalPrice"].isnull().any():
        raise HTTPException(
            status_code=400,
            detail="Some entries have missing 'TotalPrice'."
        )
    if (df_in["TotalPrice"] < 0).any():
        raise HTTPException(
            status_code=400,
            detail="Negative prices are not allowed."
        )
    if request.h < 1 or request.h > 365:
        raise HTTPException(
            status_code=400,
            detail="Forecast horizon must be between 1 and 365."
        )

    try:
        # Sort by date and rename columns for TimeGPT
        df_in = df_in.sort_values("Date").rename(
            columns={"Date": "ds", "TotalPrice": "y"}
        )
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required column: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error sorting/renaming columns: {str(e)}"
        )

    try:
        # Reset index and reformat 'ds' column to a safe string format
        df_in.reset_index(drop=True, inplace=True)
        df_in["ds"] = df_in["ds"].dt.strftime("%Y-%m-%d")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing date column: {str(e)}"
        )

    try:
        # Save data to CSV (overwrites existing)
        df_in.to_csv("data/history_data.csv", index=False)
    except OSError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error writing CSV file: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error saving CSV: {str(e)}"
        )

    try:
        # Option 1: Try forecasting without optional parameters first
        # forecast_df = client.forecast(
        #     df=df_in,
        #     h=request.h
        # )
        # Option 2: If you need freq and level, reintroduce them:
        forecast_df = client.forecast(
            df=df_in,
            h=request.h,
            freq='D',         # Daily frequency
            time_col='ds', 
            target_col='y'
        )
        print(forecast_df.head())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during forecasting: {str(e)}"
        )

    try:
        # Build response
        output = []
        for _, row in forecast_df.iterrows():
            output.append(ForecastResponse(
                ds=row["ds"],
                y=row["y"],
                y_lower=row.get("y_lower_80"),
                y_upper=row.get("y_upper_80")
            ))
    except KeyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Forecast data missing expected columns: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error building forecast response: {str(e)}"
        )

    return output
    
@app.post("/alert-plan")
def create_alert_plan(request: AlertRequest):
    """
    Runs the entire workflow for a single alert_id if provided.
    If no alert_id is provided, it processes all alerts in the JSON.
    """
    # Build the workflow, passing the alert_id from the request
    workflow = build_erp_workflow(alert_id=request.alert_id)
    
    # Create the initial state
    initial_state = ERPAgentState()

    # Run the entire pipeline
    result_state = workflow.invoke(initial_state)

    # Return the final plan plus any relevant details
    return {
        "classification_results": result_state.classification_results,
        "web_search_results": result_state.web_search_results,
        "final_plan": result_state.final_plan
    }



@app.post("/generate-plan")
def generate_plan(request: ProductRequest):
    """
    This endpoint runs the entire workflow:
      1) fetch_product_data
      2) web_search_additional_info
      3) generate_integrated_plan

    and then returns the final integrated plan.
    """
    # Build the workflow (as defined in your `workflow.py`)
    workflow = build_product_planning_workflow()

    # Create an initial state with the product name from the request
    initial_state = ProductPlanningState(
        product_info={"name": request.name}
    )

    # Invoke the workflow
    result_state = workflow.invoke(initial_state)

    # Return the integrated plan, plus any other details you want to expose
    return {
        "product_info": result_state.product_info,
        "web_search_results": result_state.web_search_results,
        "integrated_plan": result_state.integrated_plan
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)