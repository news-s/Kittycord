from auth_token import create_access_token
from database.friends import get_friend_requests, invite_friend
from database.login import create_user, verify_user
from database.profile import get_user_data


def test_send_friend_req(client, db):
    create_user("name1", "pass")
    user_id1 = verify_user("name1", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    token1 = create_access_token({"id": user_id1})

    res = client.post("/send_friend_req", json={
        "token": token1,
        "user_id": user_id2
    })

    assert res.status_code == 201

    res = get_friend_requests(user_id2)

    assert len(res["friend_requests"]) == 1
    assert res["friend_requests"][0]["from_user_id"] == user_id1


def test_accept_friend_req(client, db):
    create_user("name1", "pass")
    user_id1 = verify_user("name1", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    token2 = create_access_token({"id": user_id2})
    invite_friend(user_id1, user_id2)

    res = client.put("/accept_friend_req", json={
        "token": token2,
        "user_id": user_id1
    })

    assert res.status_code == 200

    res = get_friend_requests(user_id2)

    assert len(res["friend_requests"]) == 0

    res = get_user_data(user_id1)

    assert res["friends"] == [user_id2]

    res = get_user_data(user_id2)

    assert res["friends"] == [user_id1]


def test_reject_friend_req(client, db):
    create_user("name1", "pass")
    user_id1 = verify_user("name1", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    token2 = create_access_token({"id": user_id2})
    invite_friend(user_id1, user_id2)

    res = client.patch("/reject_friend_req", json={
        "token": token2,
        "user_id": user_id1,       
    })

    assert res.status_code == 200

    res = get_friend_requests(user_id2)

    assert len(res["friend_requests"]) == 0
    res = get_user_data(user_id1)

    assert res["friends"] == []

    res = get_user_data(user_id2)

    assert res["friends"] == []





def test_get_friend_reqs(client, db):
    create_user("name1", "pass")
    user_id1 = verify_user("name1", "pass")
    create_user("name2", "pass")
    user_id2 = verify_user("name2", "pass")
    token2 = create_access_token({"id": user_id2})
    invite_friend(user_id1, user_id2)

    res = client.post("/get_friend_reqs", json={
        "token": token2,
    })

    assert res.status_code == 200

    data = res.json()

    assert len(data["friend_requests"]) == 1
    assert data["friend_requests"][0]["from_user_id"] == user_id1
