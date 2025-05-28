from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def mostrar_formulario(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ver-resultados", response_class=HTMLResponse)
def ver_resultados(request: Request):
    archivo = "votos.txt"
    estadisticas = {}

    if os.path.exists(archivo):
        with open(archivo, 'r') as f:
            for linea in f:
                _, voto = linea.strip().split(",")
                estadisticas[voto] = estadisticas.get(voto, 0) + 1

    return templates.TemplateResponse("resultados.html", {"request": request, "estadisticas": estadisticas})


@app.post("/procesar", response_class=HTMLResponse)
def procesar_formulario(request: Request, email: str = Form(...), opcion: str = Form(None)):
    archivo = "votos.txt"
    ya_voto = False
    estadisticas = {}

    if os.path.exists(archivo):
        with open(archivo, 'r') as f:
            for linea in f:
                correo, voto = linea.strip().split(",")
                if correo == email:
                    ya_voto = True
                estadisticas[voto] = estadisticas.get(voto, 0) + 1

    
    if ya_voto:
        return templates.TemplateResponse("votoRepetido.html", {"request": request})

    with open(archivo, 'a') as f:
        f.write(f"{email},{opcion}\n")
        estadisticas[opcion] = estadisticas.get(opcion, 0) + 1

    return templates.TemplateResponse("resultados.html", {"request": request, "estadisticas": estadisticas})