import json

from database.login import create_user, verify_user
from database.servers import create_server
from database.channels import create_channel

from auth_token import create_access_token

def test_send_message(client, db):
    create_user("test", "pass")
    user_id = verify_user("test", "pass")
    res = create_server(user_id, "testname", "testlink")
    channel_id = create_channel(res["server_id"], "testname")["channel_id"]
    token = create_access_token({"id": user_id})


    with client.websocket_connect(f"/ws?token={token}") as ws:
        ws.receive_json()

        ws.send_json({"type": "channel", "content": channel_id})
        ws.receive_json()

        ws.send_json({"type": "message", "content": "test"})
        ws.receive_json()
        ws.receive_json()

        ws.send_json({"type": "channel", "content": channel_id})

        res = ws.receive_json()
        data = json.loads(res)

        assert data["messages"][0]["content"] == "test"
        

def test_change_channel(client, db):
    create_user("test", "pass")
    user_id = verify_user("test", "pass")
    res = create_server(user_id, "testname", "testlink")
    channel_id = create_channel(res["server_id"], "testname")["channel_id"]
    token = create_access_token({"id": user_id})

    with client.websocket_connect(f"/ws?token={token}") as ws:
        ws.receive_json()

        ws.send_json({"type": "channel", "content": channel_id})

        res = ws.receive_json()
        data = json.loads(res)

        assert data["status"] == 200
        assert data["messages"] == []

def test_change_server(client, db):
    create_user("test", "pass")
    user_id = verify_user("test", "pass")
    res = create_server(user_id, "name", "link")
    create_channel(res["server_id"], "name")
    token = create_access_token({"id": user_id})

    with client.websocket_connect(f"/ws?token={token}") as ws:
        ws.receive_json()

        ws.send_json({"type": "server", "content": res["server_id"]})

        res = ws.receive_json()
        data = json.loads(res)

        assert data["status"] == 200
        assert len(data["channels"]) == 1
        assert data["channels"][0]["name"] == "name"
        assert data["messages"] == []