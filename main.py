from fastapi import FastAPI

from src.routes import contacts

app = FastAPI()


app.include_router(contacts.router, prefix='/api') # для включення маршрутизації, визначеної в модулі contacts

@app.get("/")
def root():
    return {"message": "Welcome to my second version of homework 11!"}