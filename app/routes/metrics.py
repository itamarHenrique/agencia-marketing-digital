from fastapi import APIRouter, Depends, HTTPException
from ..services.security import get_current_user
from ..Models.db import load_metrics

router = APIRouter()

@router.get("/metrics")
def get_metrics(paginate: int = 0, limit: int = 100, current_user: dict = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Acesso negado")

    df_metrics = load_metrics()
    metrics_preview = df_metrics.iloc[paginate: paginate + limit].to_dict(orient="records")

    return {
        "message": f"Bem-vindo {current_user['username']}!",
        "role": current_user['role'],
        "metrics": metrics_preview
    }
