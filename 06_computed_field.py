from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float # kg
    height: float # meter
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi



def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('BMI', patient.bmi)
    print('updated')

patient_info = {'name':'Amir', 'email':'abcr@icici.com', 'age': '65', 'weight': 34.2, 'height': 1.32, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'23534624', 'emergency':'2352346'}}

patient1 = Patient(**patient_info) 

update_patient_data(patient1)