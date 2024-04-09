import os

from fastapi import FastAPI

from calculator.models.empire import Empire
from service import Service

app = FastAPI()

service: Service = Service(os.environ["FALCON_FILE"])


@app.get("/")
def root():
    return {"up": True}


@app.get("/route")
def route(empire: Empire):
    return service.navigate(empire)
