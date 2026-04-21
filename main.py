from fastapi import FastAPI
from auth_routers import auth_router
from fastapi.middleware.cors import CORSMiddleware

CORSMiddleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()
app.include_router(auth_router)