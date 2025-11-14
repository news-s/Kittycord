from fastapi import APIRouter, HTTPException


from users import users

router = APIRouter()



@router.get("/profile/{user_id}")
async def profile(user_id: int):
    # TODO Database intergration

    found = False
    userdata = users[0]
    for user in users:
        if user.id == user_id:
            userdata = user
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="User not found")
    
    return userdata.json()
