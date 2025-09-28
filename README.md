# 📊 Sistema de Métricas com FastAPI

Este projeto é uma aplicação **FastAPI** que implementa autenticação com diferentes papéis de usuário (**admin** e **usuário**) e exibição de métricas.  
- Usuários comuns podem visualizar métricas sem o campo `cost_micros`.  
- Administradores têm acesso completo aos dados.

---

## 🚀 Tecnologias utilizadas
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- Pandas (para manipulação de dados em CSV)
- HTML + Bootstrap (para interface de login e métricas)

--- 

## Como rodar o projeto

### 1 - Clonar o repositorio

[Repositorio do Github](https://github.com/itamarHenrique/agencia-marketing-digital.git)

### 2 - Criar e ativar o ambiente virtual

python -m venv venv

source venv/bin/activate ***#Linux e Mac***

venv\Scripts\activave ***#Windows***

### 3 - Instalar as dependências

pip install -r requirements.txt

### 4 - Rodar o servidor com o Uvicorn

uvicorn app.main:app --reload

### 5 - Acessar o frontend

Após iniciar o servidor, abra no navegador:

http://127.0.0.1:8000/frontend



---
