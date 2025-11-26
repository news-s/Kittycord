from database.login import create_user, verify_user
from database.profile import get_user_data
from auth_token import create_access_token

    
def test_login(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    res = client.post("/login", json={
        "username": "name",
        "hashed_password": "pass"
    })
    data = res.json()

    assert res.status_code == 200
    assert "token" in data
    assert data["user_id"] == user_id


def test_add_user(client, db):
    res = client.post("/add_user", json={
        "name": "name",
        "hashed_password": "pass"
    })

    assert res.status_code == 201


    user_id = verify_user("name", "pass")
    res = get_user_data(user_id)

    assert res["name"] == "name"
    assert res["display_name"] == "name"
    assert res["note"] == ""
    assert res["servers"] == []

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

    res = get_user_data(user_id)

    assert res["status"] == "error"