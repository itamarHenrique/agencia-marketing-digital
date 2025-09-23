from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from passlib.context import CryptContext


app = FastAPI()


df_users = pd.read_csv('user.csv')
df_metrics = pd.read_csv('metrics.csv')

@app.get('/')
def read_root():
    return {
        "message" : "Olá, fastapi está funcionando" 
    }
    
@app.get("/saudacao/{nome}")
def saudacao(nome: str):
    return {
        "message": f"Bem-vindo {nome}!"
}
    
    
class UserLogin(BaseModel):
    nome: str
    senha: str

@app.post("/login")
def login(user: UserLogin):
    user_data = df_users[df_users['username'] == user.nome]
    
    if user_data.empty:
        raise HTTPException(status_code = 400, detail= "Credenciais invalidas")
    
    stored_senha = user_data['password'].iloc[0]
    
    if not pwd_content.verify(user.password, stored_senha):
        raise HTTPException(status_code = 400, detail="Credenciais invalidas")
    
    role = user_data['role'].iloc[0]