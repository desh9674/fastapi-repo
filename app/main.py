
from fastapi import FastAPI


from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware


# from .database import Base
#Base.metadata.create_all(bind=engine) -- when there are no tables in database

# import alembic.config
# alembicArgs = [
#     '--raiseerr',
#     "revision", "--autogenerate",
#     'upgrade', 'head',
# ]
# alembic.config.main(argv=alembicArgs)


origins = [
    "https://www.google.com",
    "http://localhost",
    "http://localhost:8080",
    "*" # Every domain in world
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)

# cd FASTAPI
# uvicorn app.main:app --reload >>in cmd
# pip install -r requirements.txt
@app.get("/")
async def main():
    return {"message": "Hello World from docker environment"}

#models.Base.metadata.create_all(bind=engine) # this thing creates TABLES in postgres,
#no longer needed as using alembic


# alembic revision --autogenerate >>>>Then>>>  alembic upgrade head
# alembic revision --help, 
# , or +2 or +1 or downgrade etc

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/test1")
async def root():
    return {"message":"Welcome to fast API!!!"}  # uvicorn app.main:app --reload >>in cmd
    # its better to create new venv when project moves location, all module versions are saved in requirements.txt
    #( it runs a uvicorn server terminal unlike flask)
    #cd to FASTAPI if ASGI app error
    # >venv\Scripts\activate    



