import os

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from calculator.business.navigation import NavigationResult
from calculator.models.empire import Empire
from service import Service

MAX_DURATION = int(os.environ["MAX_DURATION"])

app = FastAPI()

service: Service = Service(os.environ["FALCON_FILE"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RouteResponse(BaseModel):
    paths: list[NavigationResult]
    matrix: list[list[int]]
    nodes: list[str]


@app.get("/")
def root():
    return {"up": True}


@app.get("/route")
def route():
    matrix, nodes = service.route()
    return {
        "matrix": matrix,
        "nodes": nodes
    }


@app.post("/navigate")
def navigate(empire: Empire, response: Response) -> NavigationResult:
    if empire["countdown"] > MAX_DURATION:
        response.status_code = 400
        return {"message": f"Countdown must be less than {MAX_DURATION}"}
    navigate = service.navigate(empire)
    return navigate
