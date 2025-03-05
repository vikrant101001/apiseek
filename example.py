from fastapi import FastAPI
from apiseek import init_app

app = FastAPI()

# Initialize APISKEEK (dashboard will be available at /apiseek)
init_app(app)

@app.get("/hello")
def hello():
    return {"message": "Hello, world!"}
