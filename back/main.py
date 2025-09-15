from fastapi import FastAPI
from views import AuthView


app = FastAPI()

app.include_router(AuthView.router, tags=['Users'])
