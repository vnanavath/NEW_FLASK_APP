import pytest
from app import app, db
from Todo.models import Todo


# @pytest.fixture
# def app_context():
#     with app.app_context():
#         yield


def test_create_data():
    with app.app_context():
        todo = Todo.query.filter_by(sno=121).first()
    assert todo.title == "python"

def test_update_data():
    with app.app_context():
        todo = Todo.query.filter_by(sno=121).first()
    assert todo.title == "python"
def test_delete_data():
    with app.app_context():
        todo = Todo.query.filter_by(sno=130).first()
    assert todo is None