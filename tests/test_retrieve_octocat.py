"""Test cases for GET requests sent to the api.octocat API endpoint."""
from http import HTTPStatus

from tests.util import (
    ADMIN_EMAIL,
    EMAIL,
    DEFAULT_CAT_NAME,
    DEFAULT_URL,
    DEFAULT_AGE,
    login_user,
    create_octocat,
    retrieve_octocat,
)


def test_retrieve_octocat_non_admin_user(client, db, admin, user):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json

    access_token = response.json["access_token"]
    response = create_octocat(client, access_token)
    assert response.status_code == HTTPStatus.CREATED

    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json

    access_token = response.json["access_token"]
    response = retrieve_octocat(client, access_token, octocat_name=DEFAULT_CAT_NAME)
    assert response.status_code == HTTPStatus.OK

    assert "name" in response.json and response.json["name"] == DEFAULT_CAT_NAME
    assert "url" in response.json and response.json["url"] == DEFAULT_URL
    assert "age" in response.json and response.json["age"] == DEFAULT_AGE


def test_retrieve_octocat_does_not_exist(client, db, user):
    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json

    access_token = response.json["access_token"]
    response = retrieve_octocat(client, access_token, octocat_name=DEFAULT_CAT_NAME)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert (
        "message" in response.json
        and f"{DEFAULT_CAT_NAME} not found in database" in response.json["message"]
    )
