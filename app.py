from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory="./templates")

# Carga el modelo de árbol
modelo_arbol = joblib.load("modelo_arbol.pkl")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("arbol.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, pib_anual: float = Form(...), pib_per_capita: float = Form(...), idh: float = Form(...), esperanza_vida: float = Form(...), muertes: float = Form(...), tasa_mortalidad: float = Form(...)):
    # Preprocesamiento de datos si es necesario
    input_data = np.array([[pib_anual, pib_per_capita, idh, esperanza_vida, muertes, tasa_mortalidad]], dtype=np.float32)

    # Realiza la predicción con el modelo de árbol
    prediction = modelo_arbol.predict(input_data)
    prediction_label = "BAJA EMIGRACION" if prediction[0] == 1 else "ALTA EMIGRACION"
    return templates.TemplateResponse("result.html", {"request": request, "prediction": prediction_label})
