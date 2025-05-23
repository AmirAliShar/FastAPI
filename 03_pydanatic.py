from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import List,Dict,Optional,Annotated

#Step 1 --> Create the class
# Common use cases
# class Patient(BaseModel):
#     name:str
#     age: int
#     weight:float
#     FaceBook:Optional[AnyUrl] = None
#     married:Optional[bool] = None
#     allergies:List[str]
#     contact:Dict[str,str]
#     email:EmailStr 

class Patient(BaseModel):
    name:str = Annotated[str,Field(max_length=50,title="Name of the patient",description="give the name of the patient in less than 50 charcter",examples=["Amir","Ali"])]
    age: int
    weight:Annotated[float,Field(gt =0,lt=100,strict=True)]# Strict is used to do not allow the type conversion
    FaceBook:Optional[AnyUrl] = None
    married:Annotated[bool,Field(default=None,description="Is the patient married or not")]
    allergies:List[str] = Field(max_length=8)
    contact:Dict[str,str]
    email:EmailStr 



def insert_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted data")

#Step 2 --> Create the object
patient = {"name":"amir","age":20,"weight":34.4,"married":False,
           "allergies":["pollan",'dust'],"contact":{"email":"amir@gmail.com","Phone":"0200220"},"email":"amir@gmail.com" }

patient1 =Patient(**patient)

insert_data(patient1)
