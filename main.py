# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field, EmailStr

# FastAPI
from fastapi import FastAPI, Body, Query, Path, Form, Header, Cookie, File, UploadFile, status 

app = FastAPI()


#Enums
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


# Models
class PersonBase(BaseModel):
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


# Person
class Person(PersonBase):
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

# PersonOut
class PersonOut(PersonBase):
    pass


# Location
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


# LoginOut
class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="luis2ra"
    )
    message: str = Field(
        default="Login Succesfully!"
    )


# home
@app.get(
    path="/",
    status_code=status.HTTP_200_OK
)
def home():
    return {"hello": "World"}


'''
En el path operation siguiente, se anula el parametro response_model_exclude y se 
aplica el concepto de herencia de POO para la clase Person.
'''
# Request and Response Body
@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
)
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
)
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
@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
)
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
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
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
    results = dict(person)
    results.update(dict(location))

    return results


# Login (Form)
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_201_CREATED
)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    return LoginOut(username=username)


# Cookies & Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_201_CREATED
)
def contact(
    first_name: str = Form(
        ...,
        max_length=30,
        min_length=2
    ),
    lasst_name: str = Form(
        ...,
        max_length=30,
        min_length=2
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent


# Files
@app.post(
    path="/post-image",
    status_code=status.HTTP_201_CREATED
)
def post_image(
    image: UploadFile = File(
        ...
    )
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": len(image.file.read()) / 1000  # deberia ser 1024 pero no concuerda con el size del archivo demo.
    }
