import json
from urllib import response
from app import schemas
import pytest


def test_get_all_posts(client):
    response = client.get("/posts/")
    #print(response.json())
    assert response.status_code == 200


def test_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    #print(response.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert response.status_code == 200

def test_get_absent_post(client, test_posts):
    response = client.get(f"/posts/9993929292929")
    assert response.status_code == 404


# @pytest.mark.parametrize("title, content, published, status_code",[
#     ("first title", "arbitory content", True, 201)
# ])
def test_create_post(authorized_client, test_user):
    response = authorized_client.post("/posts/", json={
            "title": "first title",
            "content" : "first content",
            "owner_id" : test_user["id"]
        })
   #print(response.json())
    assert response.json().get("title")== "first title"
    assert response.status_code == 201


def test_unauthorized_delete(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_absent_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/9993929292929")
    assert response.status_code == 404

def test_delete(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[2].id}")
    #print(response.json())
    assert response.status_code == 403


def test_unauthorized_update(client, test_user, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_update_absent_post(authorized_client, test_posts):
    data = {
        "title" : "updated test data",
        "content" : "updated test content",
        "id" : test_posts[0].id
    }
    response = authorized_client.put(f"/posts/9993929292929", json=data)
    assert response.status_code == 404


def test_update_post(authorized_client, test_user, test_posts):

    data = {
        "title" : "updated test data",
        "content" : "updated test content",
        "id" : test_posts[0].id
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**response.json())
    print(response.json())
    assert response.status_code == 200
    assert updated_post.title == data["title"]

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title" : "updated test data",
        "content" : "updated test content",
        "id" : test_posts[2].id
    }
    response = authorized_client.put(f"/posts/{test_posts[2].id}", json=data)
    print(response.json())
    assert response.status_code == 403