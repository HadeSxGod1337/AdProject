from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import user, auth, post

app = FastAPI()


@app.get('/api/healthchecker')
def root():
    return {'message': 'Hello World'}