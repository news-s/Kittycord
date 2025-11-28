from database.login import create_user, verify_user
from database.servers import join_server, create_server
from database.channels import get_channels
from database.roles import create_role, add_role_to_user, get_roles_in_server
from database.permissions import permissions, convert_to_permissions

from auth_token import create_access_token


def test_manage_channels_permission(client, db):
    perms = convert_to_permissions("0001000")
    create_user("name1", "pass")
    user_id1 = verify_user("name1", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    create_user("name3", "pass")
    user_id3 = verify_user("name3", "pass")
    server_id = create_server(user_id1, "name", "link")["server_id"]
    join_server(user_id2, server_id)
    join_server(user_id3, server_id)
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]
    add_role_to_user(user_id2, server_id, role_id)
    token1 = create_access_token({"id": user_id1})
    token2 = create_access_token({"id": user_id2})
    token3 = create_access_token({"id": user_id3})

    res = client.post("/add_channel", json={
        "token": token1,
        "server_id": server_id,
        "channel_name": "name1",
        "channel_color": "#FF00E6",
    })
    assert res.status_code == 201

    channel_id1 = res.json()

    res = client.post("/add_channel", json={
        "token": token2,
        "server_id": server_id,
        "channel_name": "name2",
        "channel_color": "#FF00E6",
    })
    assert res.status_code == 201

    channel_id2 = res.json()

    res = client.post("/add_channel", json={
        "token": token3,
        "server_id": server_id,
        "channel_name": "name3",
        "channel_color": "#FF00E6",
    })
    assert res.status_code == 403

    res = get_channels(server_id)

    assert res["channels"][0]["name"] == "name1"
    assert res["channels"][0]["id"] == channel_id1
    assert res["channels"][1]["name"] == "name2"
    assert res["channels"][1]["id"] == channel_id2
    assert len(res["channels"]) == 2

    res = client.put("/edit_channel/name", json={
        "token": token1,
        "channel_id": channel_id1,
        "new_val": "name4",
    })
    assert res.status_code == 200

    res = client.put("/edit_channel/name", json={
        "token": token2,
        "channel_id": channel_id2,
        "new_val": "name5",
    })
    assert res.status_code == 200

    res = client.put("/edit_channel/name", json={
        "token": token3,
        "channel_id": channel_id1,
        "new_val": "name6",
    })
    assert res.status_code == 403

    res = get_channels(server_id)

    assert res["channels"][0]["name"] == "name4"
    assert res["channels"][0]["id"] == channel_id1
    assert res["channels"][1]["name"] == "name5"
    assert res["channels"][1]["id"] == channel_id2
    assert len(res["channels"]) == 2

    res = client.patch("/remove_channel", json={
        "token": token3,
        "channel_id": channel_id1,
    })
    assert res.status_code == 403

    res = client.patch("/remove_channel", json={
        "token": token1,
        "channel_id": channel_id1,
    })
    assert res.status_code == 200

    res = client.patch("/remove_channel", json={
        "token": token2,
        "channel_id": channel_id2,
    })
    assert res.status_code == 200

    res = get_channels(server_id)

    assert len(res["channels"]) == 0


def test_manage_roles_permission(client, db):
    perms = convert_to_permissions("0000100")
    create_user("name1", "pass")
    user_id1 = verify_user("name1", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    create_user("name3", "pass")
    user_id3 = verify_user("name3", "pass")
    server_id = create_server(user_id1, "name", "link")["server_id"]
    join_server(user_id2, server_id)
    join_server(user_id3, server_id)
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]
    add_role_to_user(user_id2, server_id, role_id)
    token1 = create_access_token({"id": user_id1})
    token2 = create_access_token({"id": user_id2})
    token3 = create_access_token({"id": user_id3})


    res = client.post("/add_role", json={
        "token": token1,
        "server_id": server_id,
        "role_name": "name1",
        "role_color": "#FF00E6",
    })
    assert res.status_code == 201

    role_id1 = res.json()

    res = client.post("/add_role", json={
        "token": token2,
        "server_id": server_id,
        "role_name": "name2",
        "role_color": "#FF00E6",
    })
    assert res.status_code == 201

    role_id2 = res.json()

    res = client.post("/add_role", json={
        "token": token3,
        "server_id": server_id,
        "role_name": "name3",
        "role_color": "#FFE600",
    })
    assert res.status_code == 403

    res = get_roles_in_server(server_id)

    assert res["roles"][1]["role_name"] == "name1"
    assert res["roles"][1]["color"] == "#FF00E6"
    assert res["roles"][1]["id"] == role_id1
    assert res["roles"][2]["role_name"] == "name2"
    assert res["roles"][2]["color"] == "#FF00E6"
    assert res["roles"][2]["id"] == role_id2
    assert len(res["roles"]) == 3


    res = client.put("/edit_role/name", json={
        "token": token1,
        "role_id": role_id1,
        "new_val": "name4",
    })
    assert res.status_code == 200

    res = client.put("/edit_role/name", json={
        "token": token2,
        "role_id": role_id2,
        "new_val": "name5",
    })
    assert res.status_code == 200

    res = client.put("/edit_role/name", json={
        "token": token3,
        "role_id": role_id1,
        "new_val": "name6",
    })
    assert res.status_code == 403

    res = get_roles_in_server(server_id)

    assert res["roles"][1]["role_name"] == "name4"
    assert res["roles"][1]["color"] == "#FF00E6"
    assert res["roles"][1]["id"] == role_id1
    assert res["roles"][2]["role_name"] == "name5"
    assert res["roles"][2]["color"] == "#FF00E6"
    assert res["roles"][2]["id"] == role_id2
    assert len(res["roles"]) == 3

    res = client.put("/edit_role/color", json={
        "token": token1,
        "role_id": role_id1,
        "new_val": "#00FFE6",
    })
    assert res.status_code == 200

    res = client.put("/edit_role/color", json={
        "token": token2,
        "role_id": role_id2,
        "new_val": "#00FFE6",
    })
    assert res.status_code == 200

    res = client.put("/edit_role/color", json={
        "token": token3,
        "role_id": role_id1,
        "new_val": "#00FFE6",
    })
    assert res.status_code == 403

    res = get_roles_in_server(server_id)

    assert res["roles"][1]["role_name"] == "name4"
    assert res["roles"][1]["color"] == "#00FFE6"
    assert res["roles"][1]["id"] == role_id1
    assert res["roles"][2]["role_name"] == "name5"
    assert res["roles"][2]["color"] == "#00FFE6"
    assert res["roles"][2]["id"] == role_id2
    assert len(res["roles"]) == 3


    res = client.patch("/remove_role", json={
        "token": token3,
        "role_id": role_id1,
        "new_val": "#00FFE6",
    })
    assert res.status_code == 403


    res = client.patch("/remove_role", json={
        "token": token1,
        "role_id": role_id1,
        "new_val": "#00FFE6",
    })
    assert res.status_code == 200

    res = client.patch("/remove_role", json={
        "token": token2,
        "role_id": role_id2,
        "new_val": "#00FFE6",
    })
    assert res.status_code == 200

    res = get_roles_in_server(server_id)

    assert len(res["roles"]) == 1


def test_manage_server_permission(client, db):
    perms = convert_to_permissions("0000010")
    create_user("name1", "pass")
    user_id1 = verify_user("name1", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    create_user("name3", "pass")
    user_id3 = verify_user("name3", "pass")
    server_id = create_server(user_id1, "name", "link")["server_id"]
    join_server(user_id2, server_id)
    join_server(user_id3, server_id)
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]
    add_role_to_user(user_id2, server_id, role_id)
    token1 = create_access_token({"id": user_id1})
    token2 = create_access_token({"id": user_id2})
    token3 = create_access_token({"id": user_id3})

    res = client.put("/edit_server/name", json={
        "token": token1,
        "server_id": server_id,
        "new_val": "name1",
    })
    assert res.status_code == 200

    res = client.put("/edit_server/name", json={
        "token": token2,
        "server_id": server_id,
        "new_val": "name2",
    })
    assert res.status_code == 200

    res = client.put("/edit_server/name", json={
        "token": token3,
        "server_id": server_id,
        "new_val": "name3",
    })
    assert res.status_code == 403