import json
from fastapi import FastAPI,Path, HTTPException
from typing import Annotated,List,Dict,Literal,Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field,field_validator

app =FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="ID of the patient",examples=['P001'])]
    name: Annotated[str,Field(...,title="Name",description='Name of the patient to admit')]
    city:Annotated[str,Field(title="City",desciption="The District of patient")]
    age:Annotated[int,Field(gt=0,lt=101,title="Age",decription="Age of the patient")]
    #gender:Annotated[str,Field(title="Gender",example=["Male","Female","Neutral"])]
    gender:Annotated[Literal["male","female","other"],Field(...,description="Genter of the patient")]
    # gender:str =Path(...,examples=["Male","Female","Neutral"])
    height:Annotated[float,Field(...,gt=0,description="Height of the person in meters")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the person in kgs")]

    
    # field_validator("gender",mode="before")
    # @classmethod
    # def valid_gender(cls,v:str)->str:
    #     v=v.title()
    #     if v not in {"female","male","neutral"}:
    #         raise ValueError("Plsea")
    #     return v

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



class PatientUpdate(BaseModel):
    name: Annotated[Optional[str],Field(title="Name",description='Name of the patient to admit',default=None)]
    city:Annotated[Optional[str],Field(title="City",desciption="The District of patient",default =None)]
    age:Annotated[Optional[int],Field(gt=0,lt=101,title="Age",decription="Age of the patient",default =None)]
    gender:Annotated[Optional[Literal["male","female","other"]],Field(description="Genter of the patient",default =None)]
    height:Annotated[Optional[float],Field(gt=0,description="Height of the person in meters",default = None)]
    weight:Annotated[Optional[float],Field(gt=0,description="Weight of the person in kgs",default =None)]

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

    return JSONResponse(status_code =201,content={"message":"Pateent created successfully"})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    """
    Update a patient's information in the database.
    
    Args:
        patient_id: ID of the patient to update
        patient_update: Pydantic model containing the updated fields
        
    Returns:
        JSON response with success message or error
    """
    
    # 1. Load existing data
    data = load_data()
    
    # 2. Check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    # 3. Get the existing patient record
    existing_patient = data[patient_id]
    
    # 4. Convert update model to dict (ignore unset fields)
    updates = patient_update.model_dump(exclude_unset=True)
    
    # 5. Apply updates to existing record
    existing_patient.update(updates)
    
    # 6. Create Pydantic object to validate and calculate derived fields (like BMI)
    #    Also ensures the ID stays the same
    validated_patient = Patient(id=patient_id, **existing_patient)
    
    # 7. Convert back to dict (excluding id since it's already in our data structure)
    updated_record = validated_patient.model_dump(exclude={'id'})
    
    # 8. Save the updated record
    data[patient_id] = updated_record
    save_data(data)
    
    return JSONResponse(
        status_code=200,
        content={'message': 'Patient updated successfully'}
    )

#delete the data
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id :str):
    data = load_data()

    if patient_id in data:
        del data[patient_id] 

        save_data(data)

        return JSONResponse (status_code =200 ,content ={"message":'Patient is successfuly deleted'})
    else:
        raise HTTPException (status_code = 400,detail ="Patien is not found")
