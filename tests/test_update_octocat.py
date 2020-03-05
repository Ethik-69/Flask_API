"""Test cases for GET requests sent to the api.octocat API endpoint."""
from http import HTTPStatus

from tests.util import (
    ADMIN_EMAIL,
    DEFAULT_CAT_NAME,
    login_user,
    create_octocat,
    retrieve_octocat,
    update_octocat,
)

UPDATED_URL = "http://test.fr"
UPDATED_AGE = 10


def test_update_octocat(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json

    access_token = response.json["access_token"]
    response = create_octocat(client, access_token)
    assert response.status_code == HTTPStatus.CREATED

    response = update_octocat(
        client,
        access_token,
        octocat_name=DEFAULT_CAT_NAME,
        url=UPDATED_URL,
        age=UPDATED_AGE,
    )
    print(f"---------------{response.json}")
    assert response.status_code == HTTPStatus.OK

    response = retrieve_octocat(client, access_token, octocat_name=DEFAULT_CAT_NAME)
    assert response.status_code == HTTPStatus.OK
    assert "name" in response.json and response.json["name"] == DEFAULT_CAT_NAME
    assert "age" in response.json and response.json["age"] == UPDATED_AGE
    assert "url" in response.json and response.json["url"] == UPDATED_URL
