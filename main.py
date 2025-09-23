from fastapi import FastAPI, HTTPException
import pandas as pd
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta


app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


df_users = pd.read_csv('users.csv')
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
    username: str
    password: str
    
    
class UserRegister(BaseModel):
    username: str
    password: str
    role: str = "user"

@app.post("/login")
def login(user: UserLogin):
    user_data = df_users[df_users['username'] == user.username]
    
    if user_data.empty:
        raise HTTPException(status_code = 400, detail= "Credenciais invalidas")
    
    stored_password = user_data['password'].iloc[0]
    
    if not pwd_context.verify(user.password, stored_password):
        raise HTTPException(status_code = 400, detail="Credenciais invalidas")
    
    role = user_data['role'].iloc[0]
    
    return {
        "message": "Login bem-sucedido", "role": role
        }

@app.post("/register")
def cadastro(user: UserRegister):
    global df_users
    if not df_users[df_users['username'] == user.username].empty:
        raise HTTPException(status_code = 400, detail="Usuario já existe!")
    
    hashed_password = pwd_context.hash(user.password)
    
    new_user = pd.DataFrame(
        [[user.username, user.password, user.role]],
        columns=["username", "password", "role"]
    )
    df_users = pd.concat([df_users, new_user], ignore_index=True)
    df_users.to_csv("users_csv", index=False)
    
    return {
        "message": "Usuário cadastrado com sucesso"
    }