from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException
import typing, os, dotenv

dotenv.load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def create_access_token(data: dict[str, typing.Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(hours=1))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["id"]
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")
