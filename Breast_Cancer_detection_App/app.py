# main.py
import pickle

import numpy as np
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

with open("breast_cancer_detector.pickle", "rb") as model_file:
    model = pickle.load(model_file)

FEATURES = [
    "mean_radius",
    "mean_texture",
    "mean_perimeter",
    "mean_area",
    "mean_smoothness",
    "mean_compactness",
    "mean_concavity",
    "mean_concave_points",
    "mean_symmetry",
    "mean_fractal_dimension",
    "radius_error",
    "texture_error",
    "perimeter_error",
    "area_error",
    "smoothness_error",
    "compactness_error",
    "concavity_error",
    "concave_points_error",
    "symmetry_error",
    "fractal_dimension_error",
    "worst_radius",
    "worst_texture",
    "worst_perimeter",
    "worst_area",
    "worst_smoothness",
    "worst_compactness",
    "worst_concavity",
    "worst_concave_points",
    "worst_symmetry",
    "worst_fractal_dimension",
]

templates = Jinja2Templates(directory="templates")

# Serve files from the `static` directory at the `/static` URL
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"prediction_text": ""})


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request):
    form = await request.form()
    try:
        values = [float(form.get(feature, 0.0)) for feature in FEATURES]
        arr = np.array([values], dtype=float)
        prediction = int(model.predict(arr)[0])

        if prediction == 0:
            result = "Breast cancer detected"
        else:
            result = "No breast cancer detected"

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"prediction_text": f"Patient has: {result}"},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"prediction_text": f"Please enter valid numeric values. Error: {exc}"},
        )