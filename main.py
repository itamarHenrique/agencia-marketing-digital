from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import pandas as pd
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "teste"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


df_users = pd.read_csv('users.csv')
df_metrics = pd.read_csv('metrics.csv')

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Credenciais invalidas")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido")

class UserLogin(BaseModel):
    username: str
    password: str
    
    
class UserRegister(BaseModel):
    username: str
    password: str
    role: str = "user"


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
    
    

@app.post("/login")
def login(user: UserLogin):
    user_data = df_users[df_users['username'] == user.username]
    
    if user_data.empty:
        raise HTTPException(status_code = 400, detail= "Credenciais invalidas")
    
    stored_password = user_data['password'].iloc[0]
    
    if not pwd_context.verify(user.password, stored_password):
        raise HTTPException(status_code = 400, detail="Credenciais invalidas")
    
    role = user_data['role'].iloc[0]
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    acces_token = create_access_token(data={"sub": user.username, "role": role}, expires_delta=access_token_expires)
    
    return {
        "access_token": acces_token, "token_type": "bearer"
    }
    
    
@app.post("/register")
def cadastro(user: UserRegister):
    global df_users
    if not df_users[df_users['username'] == user.username].empty:
        raise HTTPException(status_code = 400, detail="Usuario já existe!")
    
    hashed_password = pwd_context.hash(user.password)
    
    new_user = pd.DataFrame(
        [[user.username, hashed_password, user.role]],
        columns=["username", "password", "role"]
    )
    df_users = pd.concat([df_users, new_user], ignore_index=True)
    df_users.to_csv("users.csv", index=False)
    
    return {
        "message": "Usuário cadastrado com sucesso"
    }
    
    
@app.get("/metrics")
def pegar_metricas(current_user: dict = Depends(get_current_user)):
    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    metrics_preview = df_metrics.head(50).to_dict(orient="records")
    
    return {
        "message": f"Bem-vindo {current_user['username']}!",
        "role": current_user['role'],
        "metrics": metrics_preview
    }