import pytest


from unittest.mock import patch, MagicMock
from Employee.models import Employee
from Todo.models import Todo
from db import db
from flask import Flask
from pytest_mock_resources import create_mysql_fixture
from sqlalchemy.orm import scoped_session, sessionmaker

@pytest.fixture
def new_todo():
    return Todo(title="new_todo", desc="new_desc")


@pytest.fixture
def new_emp():
    return Employee(emp_id = 1, emp_name = "alice")


@pytest.fixture
def client():
    mock_mqtt_client = MagicMock()
    with patch ('paho.mqtt.client.Client', return_value = mock_mqtt_client):
        from app import app
        with app.test_client() as test_app_client:
            yield (test_app_client, mock_mqtt_client)


mysql = create_mysql_fixture(db.Model, session = None)
@pytest.fixture
def dbsession(mysql):
    Session = sessionmaker(bind=mysql)
    session = scoped_session(Session)
    yield session
    session.close()


@pytest.fixture
def mock_app(dbsession):
    mock_app = MagicMock(spec = Flask)
    yield mock_app