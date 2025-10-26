import time
import logging
import pandas as pd
import numpy as np
import joblib
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse,FileResponse
from src.schemas import ChurnFeatures, ChurnBatch
from src.utils.validateDataEndpoint import validate_churn_features

app = FastAPI(title="Churn Prediction API")

# Cargar modelo
artifacts = joblib.load("models/trainModel.pkl")
model = artifacts["model"]
columns = artifacts["columns"]

# Configurar logger básico
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# -----------------------------
# Middleware de latencia y logger
# -----------------------------
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time_ms = (time.time() - start_time) * 1000
    response.headers["X-Process-Time-ms"] = f"{process_time_ms:.2f}"
    
    # Log estructurado
    logging.info({
        "path": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
        "process_time_ms": round(process_time_ms, 2)
    })
    return response

@app.get("/health")
def health():
    """Endpoint de estado de la API"""
    return {"status": "ok", "model_loaded": bool(model)}

# -----------------------------
# Endpoint de predicción
# -----------------------------


@app.post("/predict")
def predict(data: ChurnFeatures):
    try:

        validate_churn_features(data)

        input_data = np.array([[ 
            data.Account_Length,
            data.Area_Code,
            data.Intl_Plan,
            data.Vmail_Plan,
            data.Vmail_Message,
            data.CustServ_Calls,
            data.Total_Calls,
            data.Total_Mins,
            data.Total_Charge,
            data.High_Usage,
            data.Many_CustServ_Calls
        ]])

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[:, 1][0]

        return JSONResponse({
            "churn_prediction": int(prediction),
            "churn_probability": float(probability)
        })

    except HTTPException as e:
        raise e

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Error al predecir: {str(e)}"})


@app.post("/predict_batch")
def predict_batch(batch_data: ChurnBatch):
    """Predicción para múltiples registros"""
    try:
        results = []
        for record in batch_data.batch:

            validate_churn_features(record)

            input_data = np.array([[
                record.Account_Length,
                record.Area_Code,
                record.Intl_Plan,
                record.Vmail_Plan,
                record.Vmail_Message,
                record.CustServ_Calls,
                record.Total_Calls,
                record.Total_Mins,
                record.Total_Charge,
                record.High_Usage,
                record.Many_CustServ_Calls
            ]])
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[:, 1][0]
            results.append({
                "prediction": int(prediction),
                "probability": float(probability)
            })
        return {"results": results}

    except HTTPException as e:
        raise e

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Error al predecir: {str(e)}"})



@app.get("/export_predictions")
def export_predictions():

    """Genera y devuelve un Excel con predicciones usando las columnas guardadas en el joblib."""

    df = pd.DataFrame(columns=artifacts["columns"]) 
    df["predicted_churn"] = model.predict(df)
    df["probability_churn"] = model.predict_proba(df)[:, 1]

    output_path = "predicciones_churn.xlsx"
    df.to_excel(output_path, index=False)

    return FileResponse(
        output_path,
        filename="predicciones_churn.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

