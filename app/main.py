from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import models
from .api.endpoints import articles, search

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Research Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(articles.router, prefix="/api/v1", tags=["articles"])
app.include_router(search.router, prefix="/api/v1", tags=["search"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Fitness Research Assistant API"}