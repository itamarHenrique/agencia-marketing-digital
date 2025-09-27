from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.security import get_current_user  
from app.Models.db import load_metrics
from typing import Optional
import pandas as pd

router = APIRouter()

@router.get("/metrics")
def get_metrics(paginate: int = 0, limit: int = 100, data_inicial: Optional[str] = Query(None, description="Data Inicial (YYYY-MM-DD)"), data_final: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)"), current_user: dict = Depends(get_current_user)):
    
    df_metrics = load_metrics()
    
    df_metrics['date'] = pd.to_datetime(df_metrics['date'], format='%Y-%m-%d', errors='coerce')
    
    if data_inicial:
        df_metrics = df_metrics[df_metrics['date'] >= data_inicial]
    if data_final:
        df_metrics = df_metrics[df_metrics['date'] <= data_final]    
    
    
    metrics_preview = df_metrics.iloc[paginate: paginate + limit].to_dict(orient="records")

    return {
        "message": f"Bem-vindo {current_user['username']}!",
        "role": current_user['role'],
        "metrics": metrics_preview
    }
