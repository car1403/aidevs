"""
uvicorn 00_request:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title = "Request Test",
    description = "request test",
    version = "0.1"
)

class Customer(BaseModel):
    id:str = Field(min_length=3, examples=["id01"])
    pwd:str = Field(min_length=4, examples=["pwd01"])
    name:str = Field(min_length=5, examples=["james"])
    age:int = Field(ge=1, examples=[20])


@app.get("/health")
def health():
    return {"msg":"OK"}

@app.post("/register")
def register(customer:Customer):
    print(customer.id)
    print(customer.name)
    print(customer.age)
    return {"msg":f"{customer.name} 가입축하!"}