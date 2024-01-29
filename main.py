from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import user, auth, ad, admin
import uvicorn

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(ad.router, tags=['Ads'], prefix='/api/ads')
app.include_router(admin.router, tags=['Admin'], prefix='/api/admin')


@app.get('/api/healthchecker')
def root():
    return {'message': 'Hello World'}

if __name__ == "__main__":
    uvicorn.run("main:app",  workers=4)