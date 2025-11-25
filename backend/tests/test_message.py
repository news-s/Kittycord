from database.messages import store_channel_message
from database.channels import create_channel
from database.servers import create_server
from database.login import create_user, verify_user
from auth_token import create_access_token

def test_remove_message(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    channel_id = create_channel(server_id, "name")["channel_id"]
    message_id = store_channel_message(user_id, channel_id, "test", None)["message_id"]
    token = create_access_token({"id": user_id})

    res = client.patch("/remove_message", json={
        "token": token,
        "message_id": message_id
    })

    assert res.status_code == 200

def test_edit_message(client, db):
    create_user("name", "pass")
    user_id = verify_user("name", "pass")
    server_id = create_server(user_id, "name", "link")["server_id"]
    channel_id = create_channel(server_id, "name")["channel_id"]
    message_id = store_channel_message(user_id, channel_id, "test", None)["message_id"]
    token = create_access_token({"id": user_id})

    res = client.put("/edit_message", json={
        "token": token,
        "message_id": message_id,
        "new_content": "test2"
    })

    assert res.status_code == 200