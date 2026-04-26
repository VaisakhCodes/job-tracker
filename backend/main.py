from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import engine
import models
from routers import auth_router, applications, analyser

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Application Tracker",
    description="Track applications and analyse job fit with AI",
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

@app.get("/")
def root():
    return {"status": "running", "message": "Job Tracker API is live"}

@app.get("/health")
def health():
    return {"status": "healthy"}