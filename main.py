# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Body, Query

app = FastAPI()

# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get("/")
def home():
    return {"hello": "World"}


# Request and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=2, max_length=50),
    age: str = Query(...)  # esto no es muy comun, que un query parameter sea obligatorio
):
    return {"name": name, "age": age}
