from pydantic import BaseModel, Field
from typing import List

class ChurnFeatures(BaseModel):
    Account_Length: int = Field(..., ge=0, le=300)
    Area_Code: int = Field(..., ge=100, le=999)
    Intl_Plan: int = Field(..., ge=0, le=1)
    Vmail_Plan: int = Field(..., ge=0, le=1)
    Vmail_Message: int = Field(..., ge=0, le=200)
    CustServ_Calls: int = Field(..., ge=0, le=20)
    Total_Calls: float = Field(..., ge=0, le=1000)
    Total_Mins: float = Field(..., ge=0, le=2000)
    Total_Charge: float = Field(..., ge=0, le=500)
    High_Usage: int = Field(..., ge=0, le=1)
    Many_CustServ_Calls: int = Field(..., ge=0, le=1)

class ChurnBatch(BaseModel):
    batch: List[ChurnFeatures]


class ChurnResponse(BaseModel):
    churn_prediction: int
    churn_probability: float

