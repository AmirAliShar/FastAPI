from pydantic import BaseModel

from typing import List,Dict

class Address(BaseModel):
    city:str
    pin:str
    state:str

class Patient(BaseModel):
    name:str
    age:int
    address:Address

#Create the  pydantic model
address_info ={"city":"karachi","state":"sind","pin":"1234"}

# Unpack this
address1 =Address(**address_info)

patient_info = {"name":"abc","age":34,"address":address1}

patient1=Patient(**patient_info)

print(patient1)
print(patient1.address.city)