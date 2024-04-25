from typing import Union
from fastapi import FastAPI, status, HTTPException
from database import engine, Base, ToDo
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI, version
import shemas

#ustvarimo podatkovno bazo instanco
Base.metadata.create_all(engine)

app = FastAPI() #definiramo aplikacijo

origins = ["*"] #nismo omejeni da bi lahko se checkali

app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_methods=["*"], #vse lahko put,get, post
allow_headers = ["*"], 
#tukaj b alhko bilo še cookies,
)


@app.get("/")
def read_root():
    return "TODO app"

@app.post("/dodaj")
@version(1)
def dodaj_todo(todo:shemas.ToDo):  #kaj je ta todo
    session = Session(bind=engine, expire_on_commit =False)
    todoDB =ToDo(task=todo.task) #struktura podatka v database, task je
    session.add(todoDB)
    session.commit()
    id = todoDB.id
    session.close()
    return f"Nov ToDo id:{id}"

@app.post("/dodaj", status_code=status.HTTP_201_CREATED)
@version(2)
def dodaj_todo(todo:shemas.ToDo):  #kaj je ta todo
    session = Session(bind=engine, expire_on_commit =False) #začnep nov sesion z bazo
    todoDB =ToDo(task=todo.task) #dodamo v coloum 
    todoDB =ToDo(params=todo.params)
    session.add(todoDB)
    session.commit()
    id = todoDB.id
    session.close()
    return f"Nov ToDo id:{id}"


@app.delete("/delete/{id}") #bomo appendali iid
@version(1)
def delete_todo(id:int):
    return "delete ToDO"

@app.delete("/delete/{id}") #bomo appendali iid
@version(2)
def delete_todo(id:int):
    session = Session(bind=engine, expire_on_commit =False) #začnep nov sesion z bazo
    toDo = session.query(ToDo).get(id)
    if toDo:
        session.delete(toDo)
        session.commit()
        session.close()
    else:
        session.close()
        raise HTTPException(status_code=404, detail=f"ToDo z id: {id}, ne obstaja.")
    return "delete ToDO"

@app.put("/update/{id}/{task}")
@version(2)
def update_todo(id:int, task:str):
    session = Session(bind=engine, expire_on_commit =False) #začnep nov sesion z bazo
    todo = session.query(ToDo).get(id)
    if todo:
        todo.task = task
        session.commit()
        session.close()
        return "update ToDo"
    else:
        session.close()
        raise HTTPException(status_code=404, detail=f"ToDo z id: {id}, ne obstaja.")

@app.get("/get/{id}")
def get_todo():
    return "get ToDo"


@app.get("/get/{id}")
@version(2)
def get_todo(id: int):
    session = Session(bind=engine, expire_on_commit =False) #začnep nov sesion z bazo
    todo = session.query(ToDo).get(id)
    session.close()

    if not todo:
        raise HTTPException(status_code=404, detail=f"ToDo z id: {id}, ne obstaja.")

    return todo


@app.get("/list")
@version(2)
def get_all_todo():
    session = Session(bind=engine, expire_on_commit =False)
    todo = session.query(ToDo).all()
    session.close()
    if not todo:
        raise HTTPException(status_code=404, detail=f"ToDo baza je prazna")

    return todo



app=VersionedFastAPI(app, version_format='{major}', prefix_format="/v{major}")




