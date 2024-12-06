from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: bool | None = None):
    return {"item_id": item_id, "q": q}


@app.get("/hi")
@app.get("/hi/{name}")
def say_hi(name: Optional[str] = None):
    print(f"Hey {name}!")
    return {"msg": f"Hey {name}!"}