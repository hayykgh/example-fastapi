from fastapi import FastAPI
from . import models
from .routers import post, user, auth, vote
from .database import engine
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

origins = ["https://www.google.com"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# FastAPI router for post.py file
app.include_router(post.router)

# FastAPI router for user.py file
app.include_router(user.router)

# FastAPI router for auth.py file
app.include_router(auth.router)

# FastAPI router for vote.py file
app.include_router(vote.router)

# root path
@app.get("/")
def root():
    return {"data": "welcome to my app"}