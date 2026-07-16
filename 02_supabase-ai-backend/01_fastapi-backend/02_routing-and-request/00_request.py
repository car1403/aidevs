"""
uvicorn 00_request:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title = "Request Test",
    description = "request test",
    version = "0.1"
)

class Customer(BaseModel):
    id:str
    pwd:str
    name:str
    age:int


@app.get("/health")
def health():
    return {"msg":"OK"}

@app.post("/register")
def register(customer:Customer):
    print(customer.id)
    print(customer.name)
    print(customer.age)
    return {"msg":"가입축하!"}