"""
uvicorn 00_request:app --reload
"""

from http.client import HTTPException

from fastapi import FastAPI
from mymodels import Customer, CustomerDetail


app = FastAPI(
    title = "Request Test",
    description = "request test",
    version = "0.1"
)


@app.get("/health")
def health():
    return {"msg":"OK"}

@app.post("/register")
def register(customer:Customer):
    print(customer.id)
    print(customer.name)
    print(customer.age)
    return {"msg":f"{customer.name} 가입축하!"}

# path paramter
# 127.0.0.1:8000/get/id01
@app.get("/get/{input_id}")
def get(input_id : str):
    if input_id != "id01":
        # return "없어요"
        raise HTTPException(status_code=404, detail="ID가 존재 안함")
    customer_detail = CustomerDetail(
        id = input_id,
        name = "james",
        age = 20
    )
    return {"data":customer_detail}
