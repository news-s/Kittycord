from database.login import create_user, verify_user
from database.servers import create_server, join_server, get_servers_of_user
from auth_token import create_access_token

def test_join_server(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    token = create_access_token({"id": user_id2})

    res = client.put("/join", json={
        "token": token,
        "link": "link",
    })

    assert res.status_code == 200

    res = get_servers_of_user(user_id2)

    assert res["servers"][0]["server_id"] == server_id



def test_leave_server(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    join_server(user_id2, server_id)
    token = create_access_token({"id": user_id2})

    res = client.put("/leave", json={
        "token": token,
        "server_id": server_id
    })

    assert res.status_code == 200

    res = get_servers_of_user(user_id2)

    assert res["servers"] == []

def test_add_server(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    token = create_access_token({"id": user_id})

    res = client.post("/add_server", json={
        "token": token,
        "server_name": "name",
        "invite_link": "link",
    })

    assert res.status_code == 201

def test_remove_server(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    token = create_access_token({"id": user_id})

    res = client.patch("/remove_server", json={
        "token": token,
        "server_id": server_id,
    })

    assert res.status_code == 200


def test_edit_server_name(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    token = create_access_token({"id": user_id})

    res = client.put("/edit_server/name", json={
        "token": token,
        "server_id": server_id,
        "new_val": "name2",
    })

    assert res.status_code == 200