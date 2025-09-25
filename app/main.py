from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os



# Aqui está importando as rotas da metrica e da autenticação do usuario
from app.routes.auth import router as auth_router
from app.routes.metrics import router as metrics_router

app = FastAPI(
    title="API de Autenticação e Métricas",
    description="Gerencia usuários e fornece acesso a métricas com autenticação JWT.",
    version="1.0.0"
)

app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

app.include_router(auth_router, prefix="/autenticar", tags=["Autenticação"])
app.include_router(metrics_router, prefix="/dados", tags=["Métricas"])

@app.get("/")
def read_root():
    return {"message": "API está rodando!"}
