from fastapi import FastAPI
from .users.routes import users_routes
from .institutions.routes import institution_routes

# Create an instance of the FastAPI class
app = FastAPI(
    title="School Project API",
    description="School Project API documentation goes here",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(users_routes.router)
app.include_router(institution_routes.router)

# Define the root route
@app.get("/")
async def root():
    return {"Hello": "Welcome to my API"}