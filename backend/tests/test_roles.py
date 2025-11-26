from auth_token import create_access_token
from database.login import create_user, verify_user
from database.roles import get_roles_in_server, create_role, add_role_to_user, get_user_roles_in_server
from database.servers import create_server
from database.permissions import permissions



def test_add_role(client, db):
    perms = {}
    for perm in permissions:
        perms[perm] = False

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
    perms = {}
    for perm in permissions:
        perms[perm] = False

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
    perms = {}
    for perm in permissions:
        perms[perm] = False

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
    perms = {}
    for perm in permissions:
        perms[perm] = False
        
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


def test_edit_role_name(client, db):
    perms = {}
    for perm in permissions:
        perms[perm] = False
        
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
    perms = {}
    for perm in permissions:
        perms[perm] = False
        
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
    perms2 = {}
    for perm in permissions:
        perms2[perm] = True
    
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