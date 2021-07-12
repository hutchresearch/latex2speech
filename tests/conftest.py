import pytest

# from app import application as flask_app
from app.application import application

@pytest.fixture
def app():
    yield flask_app

# @pytest.fixture
# def client(app):
#     return app.test_client()