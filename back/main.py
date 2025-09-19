from fastapi import FastAPI
from views import AuthView, SampleView


app = FastAPI()

app.include_router(AuthView.router, tags=['Users'])
app.include_router(SampleView.router, tags=['Samples'])
