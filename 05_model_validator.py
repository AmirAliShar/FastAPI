from pydantic import BaseModel,model_validator,Field

from typing import List,Annotated

class basic (BaseModel):

    name:Annotated[str,Field(title="name of candidate",description="Enter the name of candidate")]
    age:Annotated[int,Field(title="age of candidate",description="enter the age of candidate")]
    marks:Annotated[int,Field(title="marks of candidate",description="enter the marks of candidate")]
    contact:Annotated[dict,Field(title="contact of candidate",description="enter the contact of candidate")]

    @model_validator(mode="after")
    def validotr(cls,model):
        if model.age > 65 and "emergency " not in model.contact:
            raise ValueError("Emergency contact is required for candidates above 65 years old")
        return model


marks ={"name":"amir","age":20,"marks":40,"contact":{"email":"amir@gmail.com","emergency":"0200220"}}

mark1 =basic(**marks)

print(mark1.age)

