# Python
from typing import Optional
from unicodedata import decimal

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()


# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

class Location(BaseModel):
    city: str
    state: str
    country: str


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
    name: Optional[str] = Query(
        None,
        min_length=2,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters."
    ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required."
    )  # esto no es muy comun, que un query parameter sea obligatorio
):
    return {"name": name, "age": age}


# Validaciones: Path Parameters
@app.get("/person/detail/{person_id}")
def show_person_with_id(
    person_id: int = Path(
        ..., 
        ge=1,
        title="Person Id",
        description="This is el person Id."
    )
):
    return {"person_id": person_id}


# Validaciones: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())

    return results
