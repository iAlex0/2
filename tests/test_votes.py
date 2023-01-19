import pytest
from app import schemas
from app import models



@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts, test_user):
    post_data = {"post_id": test_posts[3].id, "dir": 1}
    res = authorized_client.post("/vote/", json=post_data)
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201


def test_delete_vote_not_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404


def test_vote_on_post_not_exist(authorized_client, test_posts, test_user):
    post_data = {"post_id": 100, "dir": 1}
    res = authorized_client.post("/vote/", json=post_data)
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts, test_user):
    post_data = {"post_id": test_posts[3].id, "dir": 1}
    res = client.post("/vote/", json=post_data)
    assert res.status_code == 401