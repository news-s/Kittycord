from database.permissions import convert_to_permissions
from database.roles import create_role
from database.channels import create_channel, get_channels, delete_channel
from database.servers import create_server
from database.login import create_user, verify_user
from auth_token import create_access_token

def test_add_channel(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    token = create_access_token({"id": user_id})
    
    res = client.post("/add_channel", json={
        "token": token,
        "server_id": server_id,
        "channel_name": "name"
    })

    assert res.status_code == 201

    res = get_channels(server_id)

    assert res["channels"][0]["name"] == "name"
    
def test_remove_channel(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    channel_id = create_channel(server_id, "name2")["channel_id"]
    token = create_access_token({"id": user_id})

    res = client.patch("/remove_channel", json={
        "token": token,
        "channel_id": channel_id
    })

    assert res.status_code == 200

    res = get_channels(server_id)

    assert res["channels"] == []
    

def test_edit_channel_name(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    channel_id = create_channel(server_id, "name")["channel_id"]
    token = create_access_token({"id": user_id})

    res = client.put("/edit_channel/name", json={
        "token": token,
        "channel_id": channel_id,
        "new_val": "name2"
    })

    assert res.status_code == 200

    res = get_channels(server_id)

    assert res["channels"][0]["name"] == "name2"

def test_edit_channel_color(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    channel_id = create_channel(server_id, "name")["channel_id"]
    token = create_access_token({"id": user_id})

    res = client.put("/edit_channel/color", json={
        "token": token,
        "channel_id": channel_id,
        "new_val": "#00FFE6"
    })

    assert res.status_code == 200

    res = get_channels(server_id)

    assert res["channels"][0]["color"] == "#00FFE6"


def test_edit_channel_role_needed(client, db):
    perms = convert_to_permissions("0000000")
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    channel_id = create_channel(server_id, "name")["channel_id"]
    role_id = create_role(server_id, "name", perms, "#FF00E6")["role_id"]
    token = create_access_token({"id": user_id})

    res = client.put("/edit_channel/role_needed", json={
        "token": token,
        "channel_id": channel_id,
        "new_val": str(role_id)
    })

    assert res.status_code == 200

    res = get_channels(server_id)

    assert res["channels"][0]["role_needed"] == str(role_id)