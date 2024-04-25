from pydantic import BaseModel

class ToDo(BaseModel):
    task:str
    params: str


