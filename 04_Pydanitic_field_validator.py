from pydantic import BaseModel,field_validator,Field

from typing import List,Annotated

class basic (BaseModel):
    name:Annotated[str,Field(title="name of candidate",description="Enter the name of candidate")]
    age:Annotated[int,Field(title="age of candidate",description="enter the age of candidate")]
    marks:Annotated[int,Field(title="marks of candidate",description="enter the marks of candidate")]

    @field_validator("marks")
    @classmethod
    def check_marks(cls,value):
        if value > 100:
            raise ValueError("Marks should be less than 100")
        return value

marks ={"name":"amir","age":20,"marks":40}

mark1 =basic(**marks)

print(mark1.marks)

