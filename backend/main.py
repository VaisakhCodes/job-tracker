from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from database import engine
import models
from routers import auth_router, applications, analyser
import os

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application Tracker",
    version="1.0.0",
    swagger_ui_parameters={"syntaxHighlight": False}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(applications.router)
app.include_router(analyser.router)



# In Docker, frontend is at /frontend; locally it's ../frontend
for frontend_path in ["/frontend", "../frontend", "../../frontend"]:
    if os.path.exists(frontend_path):
        app.mount("/", StaticFiles(directory="static", html=True), name="frontend")
        break 