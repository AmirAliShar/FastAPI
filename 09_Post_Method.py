import json
from fastapi import FastAPI,Path, HTTPException
from typing import Annotated,List,Dict,Literal
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field

app =FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="ID of the patient",examples=['P001'])]
    name: Annotated[str,Field(...,title="Name",description='Name of the patient to admit')]
    city:Annotated[str,Field(title="City",desciption="The District of patient")]
    age:Annotated[int,Field(gt=0,lt=101,title="Age",decription="Age of the patient")]
    #gender:Annotated[str,Field(title="Gender",example=["Male","Female","Neutral"])]
    gender:Annotated[Literal["Male","Female","Neutral"],Field(description="Genter of the patient")]
    # gender:str =Path(...,examples=["Male","Female","Neutral"])
    height:Annotated[float,Field(...,gt=0,description="Height of the person in meters")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the person in kgs")]

    @computed_field
    @property
    def bmi(self)-> float:
        bmi = round(self.weight /(self.height**2),2)

        return bmi
    
    @computed_field
    @property
    def vertict(self) -> str:

        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Obese"



def load_data():
    with open ("patient.json","r") as f:
        load = json.load(f)
        return load
    
def save_data(data):
    with open("patient.json","w") as f:
        json.dump(data,f)

@app.get('/')
def hello():
    return {"Message":"Patient Management system API"}


@app.post("/create")
def create_patient(patient:Patient): #Patient is data type of patient
    #Load the existing data
    data = load_data()
    # check if he patient already exist
    if patient.id in data:
        raise HTTPException (status_code=400,detail="Patient already exists")
    
    # new patient add the new database
    #first convert the pydantic object to dictionary
    data[patient.id]=patient.model_dump(exclude=['id'])

    #save into the json file
    save_data(data)

    return JSONResponse(status_code =201,content={"message":"Patient created successfully"})
