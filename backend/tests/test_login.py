from database.login import create_user, verify_user
from auth_token import create_access_token

    
def test_login(client, db):
    create_user("test", "pass")
    user_id = verify_user("test", "pass")
    res = client.post("/login", json={
        "username": "test",
        "hashed_password": "pass"
    })
    data = res.json()

    assert res.status_code == 200
    assert "token" in data
    assert data["user_id"] == user_id


def test_add_user(client, db):
    res = client.post("/add_user", json={
        "name": "newuser",
        "hashed_password": "pass"
    })


    assert res.status_code == 201

def test_remove_user(client, db):
    create_user("test", "pass")
    user_id = verify_user("test", "pass")
    token = create_access_token({"id": user_id})

    res = client.patch("/remove_user", json={
        "token": token,
        "name": "test",
        "hashed_password": "pass"
    })

    assert res.status_code == 200