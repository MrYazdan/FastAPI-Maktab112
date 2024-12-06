from pydantic import BaseModel


class User(BaseModel):
    id : int
    status : bool
    name : str

ali = User(name="ali", id=1, status="f")
print(ali)