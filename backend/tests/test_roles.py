from auth_token import create_access_token
from database.login import create_user, verify_user
from database.roles import get_roles_in_server, create_role, add_role_to_user, get_user_roles_in_server
from database.servers import create_server
from database.permissions import convert_to_permissions, permissions



def test_add_role(client, db):
    perms = convert_to_permissions("0000000")
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    token = create_access_token({"id": user_id})

    res = client.post("/add_role", json={
        "token": token,
        "server_id": server_id,
        "role_name": "name",
        "role_color": "#FF00E6"
    })

    assert res.status_code == 201

    res = get_roles_in_server(server_id)

    assert res["roles"][0]["role_name"] == "name"
    assert res["roles"][0]["color"] == "#FF00E6"
    assert res["roles"][0]["permissions"] == perms

def test_remove_role(client, db):
    perms = convert_to_permissions("0000000")
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]
    token = create_access_token({"id": user_id})

    res = client.patch("/remove_role", json={
        "token": token,
        "server_id": server_id,
        "role_id": role_id
    })

    assert res.status_code == 200

    res = get_roles_in_server(server_id)

    assert res["roles"] == []


def test_add_role_to_user(client, db):
    perms = convert_to_permissions("0000000")
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]
    token = create_access_token({"id": user_id})

    res = client.put("/add_role", json={
        "token": token,
        "role_id": role_id,
        "user_id": user_id
    })

    assert res.status_code == 200

    res = get_user_roles_in_server(user_id, server_id)

    assert res["roles"][0] == role_id


def test_remove_role_from_user(client, db):
    perms = convert_to_permissions("0000000")
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]
    add_role_to_user(user_id, server_id, role_id)
    token = create_access_token({"id": user_id})

    res = client.put("/remove_role", json={
        "token": token,
        "role_id": role_id,
        "user_id": user_id
    })

    assert res.status_code == 200

    res = get_user_roles_in_server(user_id, server_id)
    
    assert res["roles"] == []


def test_get_roles_in_server(client, db):
    perms = convert_to_permissions("0000000")
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]

    res = client.get(f"/roles_in_server/{server_id}")
    data = res.json()

    assert data[0]["id"] == role_id
    assert data[0]["role_name"] == "name"
    assert data[0]["permissions"] == perms
    assert data[0]["color"] == "#FF00E6"

def test_get_role_color(client, db):
    perms = convert_to_permissions("0000000")
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]
    add_role_to_user(user_id, server_id, role_id)


    res = client.get(f"/highest_role_color/{user_id}/{server_id}")

    assert res.status_code == 200

    data = res.json()

    assert data == "#FF00E6"

def test_get_all_roles(client, db):
    perms = convert_to_permissions("0000000")
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]
    add_role_to_user(user_id, server_id, role_id)

    res = client.get(f"/all_user_roles/{user_id}/{server_id}")

    assert res.status_code == 200

    data = res.json()

    assert data[0]["id"] == role_id
    assert data[0]["role_name"] == "name"
    assert data[0]["permissions"] == perms
    assert data[0]["color"] == "#FF00E6"


def test_get_role(client, db):
    perms = convert_to_permissions("0000000")
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]

    res = client.get(f"/role/{role_id}")

    assert res.status_code == 200
    
    data = res.json()

    assert data["id"] == role_id
    assert data["role_name"] == "name"
    assert data["permissions"] == perms
    assert data["color"] == "#FF00E6"

def test_edit_role_name(client, db):
    perms = convert_to_permissions("0000000")
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]
    token = create_access_token({"id": user_id})

    res = client.put("/edit_role/name", json={
        "token": token,
        "role_id": role_id,
        "new_val": "name2"
    })

    assert res.status_code == 200


    res = get_roles_in_server(server_id)

    assert res["roles"][0]["role_name"] == "name2"
    assert res["roles"][0]["color"] == "#FF00E6"
    assert res["roles"][0]["permissions"] == perms


def test_edit_role_color(client, db):
    perms = convert_to_permissions("0000000")      
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]
    token = create_access_token({"id": user_id})

    res = client.put("/edit_role/color", json={
        "token": token,
        "role_id": role_id,
        "new_val": "#00FFE6"
    })

    assert res.status_code == 200

    res = get_roles_in_server(server_id)

    assert res["roles"][0]["role_name"] == "name"
    assert res["roles"][0]["color"] == "#00FFE6"
    assert res["roles"][0]["permissions"] == perms


def test_edit_role_permissions(client, db):
    perms2 = convert_to_permissions("1111111")
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    role_id = create_role(server_id, "name", perms2, "#FF00E6")["role_id"]
    token = create_access_token({"id": user_id})

    res = client.put("/edit_role/permissions", json={
        "token": token,
        "role_id": role_id,
        "new_permissions": perms2
    })

    assert res.status_code == 200

    res = get_roles_in_server(server_id)

    assert res["roles"][0]["role_name"] == "name"
    assert res["roles"][0]["color"] == "#FF00E6"
    assert res["roles"][0]["permissions"] == perms2
