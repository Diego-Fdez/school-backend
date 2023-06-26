from fastapi import FastAPI
from .users.routes import users_routes
from .institutions.routes import institution_routes
from .auth.routes import auth_routes
from .students.routes import students_routes
from .levels.routes import levels_routes
from .subjects.routes import subjects_routes

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
app.include_router(auth_routes.router)
app.include_router(students_routes.router)
app.include_router(levels_routes.router)
app.include_router(subjects_routes.router)

# Define the root route
@app.get("/")
async def root():
    return {"Hello": "Welcome to my API"}
