import pytest
from app import schemas


# Get Post
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    # assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/100")
    assert res.status_code == 404

def test_get_post_by_id(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

# Create Post
@pytest.mark.parametrize("title, content, published", [
    ("awesome title", "awesome content", True),
    ("title 2", "hello you", False),
    ("fine dining", "awesome food", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    post_data = {"title": title, "content": content, "published": published}
    res = authorized_client.post("/posts/", json=post_data)
    
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    post_data = {"title": "title 1", "content": "content 1"}
    res = authorized_client.post("/posts/", json=post_data)
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.published == True

def test_unauthorized_create_posts(client, test_user, test_posts):
    post_data = {"title": "title 1", "content": "content 1"}
    res = client.post("/posts/", json=post_data)
    assert res.status_code == 401

# Delete Post
def unauthorized_delete_post(client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/100")
    assert res.status_code == 404

def test_delete_post_not_owner(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 401

# Update Post
def test_unauthorized_update_posts(client, test_posts, test_user):
    post_data = {"title": "updated title", "content": "updated content", "published": False}
    res = client.put(f"/posts/{test_posts[0].id}", json=post_data)
    assert res.status_code == 401

def test_update_post(authorized_client, test_posts, test_user):
    post_data = {"title": "updated title", "content": "updated content", "published": False}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=post_data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == post_data['title']
    assert updated_post.content == post_data['content']
    assert updated_post.published == post_data['published']

def test_update_post_not_exist(authorized_client, test_posts, test_user):
    post_data = {"title": "updated title", "content": "updated content", "published": False}
    res = authorized_client.put(f"/posts/100", json=post_data)
    assert res.status_code == 404

def test_update_post_not_owner(authorized_client, test_posts, test_user):
    post_data = {"title": "updated title", "content": "updated content", "published": False}
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=post_data)
    assert res.status_code == 401

