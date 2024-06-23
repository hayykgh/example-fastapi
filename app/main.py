from fastapi import FastAPI, HTTPException
from .routers import vote, post, user, auth
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/some-protected-endpoint")
async def some_protected_endpoint():
    raise HTTPException(status_code=401, detail="Not authenticated")


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
    return {"message": "THE COURSE IS DOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONE"}