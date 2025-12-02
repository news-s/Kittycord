from database.login import create_user, verify_user
from database.profile import get_user_data
from auth_token import create_access_token

def test_profile(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")

    res = client.get(f"/profile/{user_id}")
    data = res.json()

    assert res.status_code == 200
    assert data["name"] == "name"
    assert data["display_name"] == "name"
    assert data["note"] == ""
    assert data["servers"] == []


def test_edit_profile_display_name(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    token = create_access_token({"id": user_id})

    res = client.put("/edit_profile/display_name", json={
        "token": token,
        "new_val": "name2"
    })

    assert res.status_code == 200

    res = get_user_data(user_id)

    assert res["name"] == "name"
    assert res["display_name"] == "name2"
    assert res["note"] == ""
    assert res["servers"] == []

def test_edit_profile_name(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    token = create_access_token({"id": user_id})

    res = client.put("/edit_profile/name", json={
        "token": token,
        "new_val": "name2"
    })

    assert res.status_code == 200

    res = get_user_data(user_id)

    assert res["name"] == "name2"
    assert res["display_name"] == "name"
    assert res["note"] == ""
    assert res["servers"] == []


def test_edit_profile_note(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    token = create_access_token({"id": user_id})

    res = client.put("/edit_profile/note", json={
        "token": token,
        "new_val": "note"
    })

    assert res.status_code == 200

    res = get_user_data(user_id)

    assert res["name"] == "name"
    assert res["display_name"] == "name"
    assert res["note"] == "note"
    assert res["servers"] == []