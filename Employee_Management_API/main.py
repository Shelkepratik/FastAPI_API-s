from fastapi import FastAPI,Path,HTTPException
from typing import Annotated,Literal
from pydantic import BaseModel,Field,EmailStr
import json

app=FastAPI()

class Empoyee(BaseModel):
    name:Annotated[str,Field(max_length=50,min_length=2,description="empoyee name")]
    email:EmailStr
    department:Literal["IT","HR","Finance","sales","Marketing"]
    designation:Annotated[str,Field(min_legth=2,max_length=50)]
    salary:Annotated[int,Field(ge=0,le=500000)]
    experience:Annotated[int,Field(ge=0,le=40)]
    status:Literal["Active","Inactive"]="Active"

def load_data():
    with open("employees.json","r") as file:
        file=json.load(file)
        return file

def save_empoyee(data):
    with open("employees.json","w") as file:
        json.dump(data,file,indent=4)

@app.get("/")
def welcome_message():
    return "welcome to Employee management system"

@app.get("/view")
def display_information():
    data=load_data()
    return data


@app.get("/view/{empolyee_id}")
def show_employee(empolyee_id:Annotated[str,Path(...)]):
    data=load_data()
    if empolyee_id not in data:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    return data[empolyee_id]

@app.get("/view/department/{department_name}")
def show_empolyee_deparment(department_name:str=Path(...)):
    data=load_data()
    result={}
    for empolyee_id,empolyee in data.items():
        if empolyee["department"].lower()==department_name.lower():
            result[empolyee_id]=empolyee
    return result


@app.post("/view",status_code=201)
def add_empoyee(empolyee:Empoyee):
    empolyees=load_data()
    empolyee_ids=[int(key) for key in empolyees.keys()]
    new_id=max(empolyee_ids,default=100)+1
    empolyees[str(new_id)]=empolyee.model_dump()
    save_empoyee(empolyees)
    return{
        "message":"Employee added successfully"
    }
    
    

