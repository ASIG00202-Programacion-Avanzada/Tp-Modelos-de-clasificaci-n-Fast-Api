
from fastapi import HTTPException
from src.schemas import ChurnFeatures



def validate_churn_features(data: ChurnFeatures):
    """Valida los rangos típicos de cada campo y lanza excepción si hay errores."""
    warnings = []

    if not (0 <= data.Account_Length <= 500):
        warnings.append("Account_Length fuera de rango típico (0-500)")
    if not (200 <= data.Area_Code <= 999):
        warnings.append("Area_Code fuera de rango típico (200-999)")
    if not (0 <= data.Intl_Plan <= 1):
        warnings.append("Intl_Plan debe ser 0 o 1")
    if not (0 <= data.Vmail_Plan <= 1):
        warnings.append("Vmail_Plan debe ser 0 o 1")
    if not (0 <= data.Vmail_Message <= 1000):
        warnings.append("Vmail_Message fuera de rango típico (0-1000)")
    if not (0 <= data.CustServ_Calls <= 20):
        warnings.append("CustServ_Calls fuera de rango típico (0-20)")
    if not (0 <= data.Total_Calls <= 5000):
        warnings.append("Total_Calls fuera de rango típico (0-5000)")
    if not (0 <= data.Total_Mins <= 10000):
        warnings.append("Total_Mins fuera de rango típico (0-10000)")
    if not (0 <= data.Total_Charge <= 2000):
        warnings.append("Total_Charge fuera de rango típico (0-2000)")
    if not (0 <= data.High_Usage <= 1):
        warnings.append("High_Usage debe ser 0 o 1")
    if not (0 <= data.Many_CustServ_Calls <= 1):
        warnings.append("Many_CustServ_Calls debe ser 0 o 1")

    if warnings:
        raise HTTPException(status_code=400, detail=warnings)