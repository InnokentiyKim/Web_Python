from fastapi import FastAPI
import pydantic


app = FastAPI(
    title="Hello",
    terms_of_service="",
    description="",
)

class InputJson(pydantic.BaseModel):
    name: str
    age: int

class OutputJson(pydantic.BaseModel):
    hello: str

app.post("/api/v1/hello/world/{some_id}")
def hello_world(json_data: InputJson, some_key: str, some_id: int):
    print(f"json_data: {json_data}")
    return {"hello": "world"}
