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
    

def test_edit_channel(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    channel_id = create_channel(server_id, "name")["channel_id"]
    token = create_access_token({"id": user_id})

    res = client.put("/edit_channel/name", json={
        "token": token,
        "channel_id": channel_id,
        "new_name": "name2"
    })

    assert res.status_code == 200

    res = get_channels(server_id)

    assert res["channels"][0]["name"] == "name2"