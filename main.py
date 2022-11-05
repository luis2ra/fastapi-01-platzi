# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()


#Enums
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


# Models
class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=120
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    password: str = Field(
        ...,
        min_length=8
    )

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Luis",
                "last_name": "Altuve",
                "age": 46,
                "hair_color": "brown",
                "is_married": False,
                "password": "stringstr"
            }
        }


class PersonOut(BaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=120
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)


class Location(BaseModel):
    city: str = Field(
        ...,
        example="Pamplona"
    )
    state: str = Field(
        ...,
        example="Norte de Santander"
    )
    country: str = Field(
        ...,
        example="Colombia"
    )


@app.get("/")
def home():
    return {"hello": "World"}


# Request and Response Body
@app.post("/person/new", response_model=PersonOut)
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
        description="This is the person name. It's between 1 and 50 characters.",
        example="Dayana Saray"
    ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required.",
        example="44"
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
        description="This is el person Id.",
        example=1
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
        gt=0,
        example=3
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    # results = person.dict()
    # results.update(location.dict())
    results = dict(person)
    results.update(dict(location))

    return results
