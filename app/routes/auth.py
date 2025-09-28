from fastapi import APIRouter, HTTPException
import pandas as pd
from datetime import timedelta
from app.Models.model import UserLogin, UserRegister 
from app.services.security import pwd_context, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.Models.db import load_users, save_users
router = APIRouter()

@router.post("/login")
def login(user: UserLogin):
    df_users = load_users()
    user_data = df_users[df_users['username'] == user.username]
    
    if user_data.empty:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    stored_password = user_data['password'].iloc[0]

    if not pwd_context.verify(user.password, stored_password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    role = user_data['role'].iloc[0]
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": role}


@router.post("/register")
def register(user: UserRegister):
    df_users = load_users()
    if not df_users[df_users['username'] == user.username].empty:
        raise HTTPException(status_code=400, detail="Usuário já existe!")

    hashed_password = pwd_context.hash(user.password)

    new_user = pd.DataFrame([[user.username, hashed_password, user.role]],
                            columns=["username", "password", "role"])

    df_users = pd.concat([df_users, new_user], ignore_index=True)
    save_users(df_users)

    return {"message": "Usuário cadastrado com sucesso"}
