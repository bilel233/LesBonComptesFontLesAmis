import pytest
from ..app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "DATABASE": 'mongodb+srv://BilelMajdoub:Mongodb1998%40@bdd.uquucse.mongodb.net/api'
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
