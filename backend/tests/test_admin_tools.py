import datetime
from auth_token import create_access_token
from database.servers import create_server, get_users_in_server, join_server
from database.channels import create_channel
from database.login import create_user, verify_user


def test_mute(client, db):
    create_user("name1", "pass")
    user_id1 = verify_user("name1", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    server_id = create_server(user_id1, "name", "link")["server_id"]
    join_server(user_id2, server_id)
    channel_id = create_channel(server_id, "name")["channel_id"]
    token1 = create_access_token({"id": user_id1})
    token2 = create_access_token({"id": user_id2})

    timestamp = (datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()

    res = client.post("/mute", json={
        "token": token1,
        "user_id": user_id2,
        "server_id": server_id,
        "muted_till": int(timestamp)
    })

    assert res.status_code == 200

    with client.websocket_connect(f"/ws?token={token2}") as ws:
        ws.receive_json()

        ws.send_json({"type": "channel", "content": channel_id})
        ws.receive_json()

        ws.send_json({"type": "message", "content": "test"})
        res = ws.receive_json()

        assert res["status"] == 403

        ws.send_json({"type": "channel", "content": channel_id})
        
        res = ws.receive_json()

        assert res["messages"] == []

    res = client.post("/unmute", json={
        "token": token1,
        "user_id": user_id2,
        "server_id": server_id,
    })

    assert res.status_code == 200

    with client.websocket_connect(f"/ws?token={token2}") as ws:
        ws.receive_json()

        ws.send_json({"type": "channel", "content": channel_id})
        ws.receive_json()

        ws.send_json({"type": "message", "content": "test"})
        ws.receive_json()
        res = ws.receive_json()

        assert res["status"] == 201

        ws.send_json({"type": "channel", "content": channel_id})
        
        res = ws.receive_json()

        assert res["messages"][0]["content"] == "test"


def test_ban(client, db):
    create_user("name1", "pass")
    user_id1 = verify_user("name1", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    server_id = create_server(user_id1, "name", "link")["server_id"]
    join_server(user_id2, server_id)
    token1 = create_access_token({"id": user_id1})
    token2 = create_access_token({"id": user_id2})

    res = client.post("/ban", json={
        "token": token1,
        "user_id": user_id2,
        "server_id": server_id,
        "reason": "test"
    })

    assert res.status_code == 200

    res = get_users_in_server(server_id)

    assert len(res["users"]) == 1
    assert res["users"][0]["user_id"] == user_id1

    res = client.put("/join", json={
        "token": token2,
        "link": "link"
    })

    assert res.status_code == 403


def test_kick(client, db):
    create_user("name1", "pass")
    user_id1 = verify_user("name1", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    server_id = create_server(user_id1, "name", "link")["server_id"]
    join_server(user_id2, server_id)
    token1 = create_access_token({"id": user_id1})

    res = client.post("/kick", json={
        "token": token1,
        "user_id": user_id2,
        "server_id": server_id,
    })

    assert res.status_code == 200

    res = get_users_in_server(server_id)

    assert len(res["users"]) == 1
    assert res["users"][0]["user_id"] == user_id1