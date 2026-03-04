from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routes import router
import os


app = FastAPI(title="Рекомендательная система научных статей")


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATIC_PATH = os.path.join(BASE_DIR, "static")

if not os.path.isdir(STATIC_PATH):
    raise RuntimeError(f"Static папка не найдена: {STATIC_PATH}")


app.mount("/static", StaticFiles(directory=STATIC_PATH, html=True), name="static")


@app.get("/", response_class=FileResponse)
def read_root():
    return FileResponse(os.path.join(STATIC_PATH, "index.html"))

app.include_router(router)