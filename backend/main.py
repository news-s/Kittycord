from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes import login, profile, channel, ws

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(profile.router)
app.include_router(channel.router)
app.include_router(ws.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)