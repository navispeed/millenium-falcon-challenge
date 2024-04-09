import os


from fastapi import FastAPI
from starlette.responses import Response

from calculator.models.empire import Empire
from service import Service

MAX_DURATION = int(os.environ["MAX_DURATION"])

app = FastAPI()

service: Service = Service(os.environ["FALCON_FILE"])


@app.get("/")
def root():
    return {"up": True}


@app.get("/route")
def route(empire: Empire, response: Response):
    if empire["countdown"] > MAX_DURATION:
        response.status_code = 400
        return {"message": f"Countdown must be less than {MAX_DURATION}"}
    return service.navigate(empire)
