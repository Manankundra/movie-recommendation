from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def home():
    return{"message":"the api is running"}