import pandas as pd
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

df = pd.read_csv("users.csv")

df["password"] = df["password"].apply(lambda x: pwd_context.hash(x))

df.to_csv("users.csv", index=False)

print("Arquivo users.csv criado com senhas hashadas.")