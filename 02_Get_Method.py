from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

def load_data():
    with open("patient.json","r") as f:
        data = json.load(f)
        return data

@app.get("/")
def hello():
    return {"Message":"Patient Management System API"}

@app.get("/about")
def about():
    return {"Message":"A Fully functional API to manage your patient record"}

#Create the end point
@app.get("/view")
def view():
    data =load_data()
    return data

#Set the path parameter
@app.get("/patient{patient_id}")

def view_patient(patient_id:str = Path(...,description="ID of the patient in the DB",example="P001")):# Three dots shows to path parameter is required
    #load the all patient data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException (status_code=404,detail="Patient not found")

# Query parameter 
@app.get("/sort")
def sort_patient(sort_by:str = Query(...,description="Sort on the basis of height ,weight or bmi"),
                order:str =Query("asc",description="Sort in asc or desc order")):
    valid_field =["height","weight",'bmi']
    if sort_by not in valid_field:
        raise HTTPException(status_code=400,detail=f'Invaild Field select from{valid_field}')
    if order not in ["asc",'desc']:
        raise HTTPException(status_code=400,detail="Invalid order select between asc or desc")
    
    data = load_data()
    sort_order = True if order == 'desc' else False

    sort_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)

    return sort_data
