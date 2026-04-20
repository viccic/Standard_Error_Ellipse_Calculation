from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from error_ellipse import Calculation
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPH_DIR = os.path.join(BASE_DIR, "Graph_Database")

if not os.path.exists(GRAPH_DIR):
    os.makedirs(GRAPH_DIR)

app.mount("/Graph_Database", StaticFiles(directory=GRAPH_DIR), name="images")

class Points(BaseModel):
    point_names: list[str]
    point_coordinates: list[list[float]]
    point_sigmas: list[list[float]]

@app.post("/upload")
def upload(data: Points):
    #print(data.point_names)
    #print(data.point_coordinates)
    #print(data.point_sigmas)

    point_name, max_ax, min_ax, angle_rot_rad, angle_rot_grad = Calculation(
        data.point_names,
        data.point_coordinates,
        data.point_sigmas
    )

    return {
        "point_name": point_name,
        "images": [
            f"http://127.0.0.1:8000/Graph_Database/Ellipse_{name}.png"
            for name in point_name
        ]
        }