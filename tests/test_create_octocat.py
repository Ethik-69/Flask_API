"""Unit tests for POST requests sent to api.octocat_list API endpoint."""
from http import HTTPStatus

import pytest

from tests.util import (
    EMAIL,
    ADMIN_EMAIL,
    FORBIDDEN,
    DEFAULT_CAT_NAME,
    login_user,
    create_octocat,
)


@pytest.mark.parametrize("octocat_name", ["abc123", "octocat-name", "new_octocat1"])
def test_create_octocat_valid_name(client, db, admin, octocat_name):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json

    access_token = response.json["access_token"]
    response = create_octocat(client, access_token, octocat_name=octocat_name)
    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"

    success = f"New octocat added: {octocat_name}."
    assert "message" in response.json and response.json["message"] == success

    location = f"http://localhost/api/v1/octocats/{octocat_name}"
    assert "Location" in response.headers and response.headers["Location"] == location


def test_create_octocat_already_exists(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json

    access_token = response.json["access_token"]
    response = create_octocat(client, access_token)
    assert response.status_code == HTTPStatus.CREATED

    response = create_octocat(client, access_token)
    assert response.status_code == HTTPStatus.CONFLICT

    name_conflict = f"Octocat name: {DEFAULT_CAT_NAME} already exists, must be unique."
    assert "message" in response.json and response.json["message"] == name_conflict


def test_create_octocat_no_admin_token(client, db, user):
    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json

    access_token = response.json["access_token"]
    response = create_octocat(client, access_token)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "message" in response.json and response.json["message"] == FORBIDDEN
