"""Global pytest fixtures."""
import pytest

from flask_api import create_app
from flask_api import db as database
from flask_api.models.user import User
from tests.util import EMAIL, ADMIN_EMAIL, PASSWORD


@pytest.fixture
def app():
    """ Create main app """
    app = create_app("testing")
    return app


@pytest.fixture
def db(app, client, request):
    """ Erase then Create DB """
    database.drop_all()
    database.create_all()
    database.session.commit()

    def fin():
        database.session.remove()

    request.addfinalizer(fin)
    return database


@pytest.fixture
def user(db):
    """ Create a test user """
    user = User(email=EMAIL, password=PASSWORD)
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def admin(db):
    """ Create an admin test user """
    admin = User(email=ADMIN_EMAIL, password=PASSWORD, admin=True)
    db.session.add(admin)
    db.session.commit()
    return admin
