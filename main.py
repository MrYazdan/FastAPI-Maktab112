from enum import Enum
from typing import Annotated

from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: bool | None = None):
    return {"item_id": item_id, "q": q}


@app.get("/hi")
@app.get("/hi/{name}")
def say_hi(name: str | None = None):
    print(f"Hey {name}!")
    return {"msg": f"Hey {name}!"}


# @app.get("/users/{user_id}")
# async def read_user(user_id: int):
#     return {"user_id": user_id}
#
# @app.get("/users/me")
# async def read_user():
#     return {"user_id": "the current user"}

@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]

@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


class Fruits(str, Enum):
    apple = "apple"
    banana = "banana"
    pear = "pear"
    peach = "peach"


@app.get("/fruits/{fruit_name}")
async def get_fruit(fruit_name: Fruits):
    if fruit_name == Fruits.apple:
        return {"fruit_name": fruit_name, "msg": "Apple is red."}

    if fruit_name == Fruits.banana:
        return {"fruit_name": fruit_name, "msg": "Banana is yellow."}

    if fruit_name == Fruits.pear:
        return {"fruit_name": fruit_name, "msg": "Pear is green."}

    if fruit_name == Fruits.peach:
        return {"fruit_name": fruit_name, "msg": "Peach is pink."}

    return {"fruit_name": fruit_name, "msg": "I don't know this fruit."}


# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return HTMLResponse(f"""
#     <html>
#         <head>
#             <title>Files</title>
#         </head>
#         <body>
#             <h1>Files</h1>
#             <p>Path: {file_path}</p>
#             <hr/>
#             <img src="{file_path}" />
#             <hr/>
#             <audio id="audio" controls>
#                 <source src="{file_path}" ></source>
#             </audio>
#         </body>
#     </html>
#     """)

@app.get("/loader")
async def loader(audio: str = "", img: str = ""):
    return HTMLResponse(f"""
    <html>
        <head>
            <title>Files</title>
        </head>
        <body>
            <h1>Loader</h1>
            {
                audio and f"""
                <p>Audio: {audio}</p>
                <hr/>
                <audio id="audio" controls>
                    <source src="{audio}" ></source>
                </audio>
                """
            }
            {
                img and f"""
                <p>Image: {img}</p>
                <hr/>
                <img src="{img}" />
                """
            }
        </body>
    </html>
    """)


# shuffle all items in numbers list
import random
numbers = list(range(1,101))
# random.shuffle(numbers)

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=len(numbers))
    offset: int = Field(1, ge=0, le=len(numbers))

# @app.get("/numbers")
# async def get_numbers(params: Annotated[FilterParams, Query()]):
#     return (numbers[params.offset-1:params.offset+params.limit-2]

async def offset_and_limit_query_params(offset: int = 0, limit: int = 100):
    return {"offset": offset, "limit": limit}

@app.get("/numbers")
async def get_numbers(commons : dict = Depends(offset_and_limit_query_params)):
    return numbers[commons["offset"]: commons["limit"]]



data = {
    "plumbus": {"description": "Freshly pickled plumbus", "owner": "Morty"},
    "portal-gun": {"description": "Gun to create portals", "owner": "Rick"},
}


class OwnerError(Exception):
    pass


def get_username():
    try:
        yield "Rick"
    except OwnerError as e:
        raise HTTPException(status_code=403, detail=f"Owner error: {e}")

@app.get("/data/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(username)
    return item


def isolate_mode():
    try:
        yield
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Error Ommad !")


@app.get("/error")
def error(isolate: Annotated[None, Depends(isolate_mode)]):
    print("In View Func")
    raise HTTPException(status_code=500, detail="Internal Server Error")