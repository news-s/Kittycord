from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os, dotenv
from database import models

from routes import admin_tools, login, profile, channel, server, message, roles, friends, dms, files, ws

dotenv.load_dotenv()
models.init_db(
    f'postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_tools.router)
app.include_router(login.router)
app.include_router(profile.router)
app.include_router(channel.router)
app.include_router(server.router)
app.include_router(message.router)
app.include_router(roles.router)
app.include_router(friends.router)
app.include_router(dms.router)
app.include_router(files.router)
app.include_router(ws.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)