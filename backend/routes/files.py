from typing import Annotated
from fastapi import APIRouter, File, HTTPException
from fastapi.responses import StreamingResponse

from database.files import retrive_file, store_file


router = APIRouter()


@router.post("/upload_file")
async def upload_file(name: str, file: Annotated[bytes, File()]):
    file_id = store_file(name, file)

    return file_id


@router.get("/load_file")
async def load_file(file_id: int):
    file = retrive_file(file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="file doesn't exist")

    return StreamingResponse(
        iter([file.content]),  # bytes from DB
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={file.name}"
        }
    )
