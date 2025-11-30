from database.dms import get_messsages_from_dm, store_direct_message
from database.channels import create_channel
from database.servers import create_server
from database.login import create_user, verify_user
from auth_token import create_access_token

def test_remove_dm(client, db):
    create_user("name1", "pass")
    user_id1 = verify_user("name1", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    dm_id = store_direct_message(user_id1, user_id2, "test", None)["dm_id"]
    token = create_access_token({"id": user_id1})

    res = client.patch("/remove_dm", json={
        "token": token,
        "dm_id": dm_id
    })

    assert res.status_code == 200

    res = get_messsages_from_dm(50, user_id1, user_id2)

    assert res["messages"] == []

def test_edit_dm(client, db):
    create_user("name1", "pass")
    user_id1 = verify_user("name1", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    dm_id = store_direct_message(user_id1, user_id2, "test", None)["dm_id"]
    token = create_access_token({"id": user_id1})

    res = client.put("/edit_dm", json={
        "token": token,
        "dm_id": dm_id,
        "new_content": "test2"
    })

    assert res.status_code == 200

    res = get_messsages_from_dm(50, user_id1, user_id2)

    assert res["messages"][0]["author_id"] == user_id1
    assert res["messages"][0]["content"] == "test2"