"""
uvicorn 00_request:app --reload
"""


from fastapi import FastAPI, HTTPException
from mymodels import Customer, CustomerDetail, ApiResponse


app = FastAPI(
    title = "Request Test",
    description = "request test",
    version = "0.1"
)


@app.get("/health")
def health():
    response = ApiResponse(
        success=True,
        message="OK",
    )
    return response

# Request Body
# insert, update
@app.post("/register")
def register(customer:Customer):
    print(customer.id)
    print(customer.name)
    print(customer.age)
    response = ApiResponse(
        success = True,
        message = f"{customer.name} 가입축하!",
    )
    return response

# Path Paramter
# 127.0.0.1:8000/get/id01
# get , delete
@app.get("/get/{input_id}")
def get(input_id : str):
    if input_id != "id01":
        # return "없어요"
        raise HTTPException(status_code=404, detail="ID가 존재 안함")
    customer_data = {
        "id":"id01",
        "pwd":"xsfafdsa",
        "name":"james",
        "age":20
    }
    response = ApiResponse(
        success = True,
        message = "정상조회",
        data =  CustomerDetail( 
                    id=customer_data["id"],
                    name=customer_data["name"],
                    age=customer_data["age"],
        )
    )
    return response


# Query Parameter
# 검색
@app.get("/search")
def search(
    id : str | None = None,
    name : str | None = None,
    age : int | None = None,
):
    print(f"{id}로 검색 합니다.")
    print(f"{name}로 검색 합니다.")
    print(f"{age}로 검색 합니다.")

    customers = [
        {
            "id" : "id01",
            "name" : "name1",
            "age" : 10
        },
        {
            "id" : "id02",
            "name" : "name2",
            "age" : 20
        },
        {
            "id" : "id03",
            "name" : "name3",
            "age" : 30
        },
    ]

    response = ApiResponse(
        success = True,
        message = "정상조회",
        data =  customers
    )
    return response

