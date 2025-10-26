from fastapi.testclient import TestClient
from app import app 


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}



def test_predict_valid():
    payload = {
        "Account_Length": 120,
        "Area_Code": 415,
        "Intl_Plan": 0,
        "Vmail_Plan": 1,
        "Vmail_Message": 30,
        "CustServ_Calls": 3,
        "Total_Calls": 500,
        "Total_Mins": 1000,
        "Total_Charge": 200,
        "High_Usage": 0,
        "Many_CustServ_Calls": 0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "churn_prediction" in response.json()
    assert "churn_probability" in response.json()

def test_predict_batch():
    batch_payload = {
        "batch": [
            {
                "Account_Length": 100,
                "Area_Code": 408,
                "Intl_Plan": 1,
                "Vmail_Plan": 0,
                "Vmail_Message": 20,
                "CustServ_Calls": 2,
                "Total_Calls": 400,
                "Total_Mins": 800,
                "Total_Charge": 150,
                "High_Usage": 1,
                "Many_CustServ_Calls": 0
            },
            {
                "Account_Length": 200,
                "Area_Code": 510,
                "Intl_Plan": 0,
                "Vmail_Plan": 1,
                "Vmail_Message": 10,
                "CustServ_Calls": 5,
                "Total_Calls": 600,
                "Total_Mins": 1200,
                "Total_Charge": 300,
                "High_Usage": 0,
                "Many_CustServ_Calls": 1
            }
        ]
    }
    response = client.post("/predict_batch", json=batch_payload)
    assert response.status_code == 200
    assert len(response.json()["results"]) == 2
