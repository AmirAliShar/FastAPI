from fastapi import FastAPI
app = FastAPI()

#Define the endpoint
@app.get("/")
def hello():
    return {"message":"Hello World"}

#Second Endpoint
@app.get("/about")
def about():
    return {"message":"Amir ALi Data scientist and AI Engineer"}