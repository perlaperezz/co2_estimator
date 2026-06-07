from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from src.web.routes import router

app = FastAPI(title="CO\u2082 Estimator", version="0.1.0")

static_dir = os.path.join(os.path.dirname(__file__), "web", "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(router)
