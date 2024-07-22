import json
from Employee.models import Employee
from Todo.models import Todo
from unittest.mock import patch, MagicMock


import Employee.methods as e_methods
import Todo.methods as t_methods




def test_api(client,dbsession):
    test_client, mock_mqtt_client = client


    response = test_client.get('/')  # Simulate a GET request to the home route
    assert response.status_code == 200  # Check that the response status code is 200
    assert response.data.decode() == "Hello World!"  # Check the response data


    response = test_client.post("/todo/create", json = {"title":"pytest", "desc":"learning"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Todo sent to creation successfully"}


    response = test_client.put("/todo/update/1", json = {"title":"update_pytest", "desc":"update_learning"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Todo sent for updation successfully"}


    response = test_client.delete("/todo/delete/1")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Todo published for deletion"}


    response = test_client.post("/employee/create", json = {"emp_name":"alice", "emp_id":1})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Employee sent for creation successfully"}


    response = test_client.put("/employee/update/1", json = {"emp_name":"update_alice", "emp_id":1})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Employee sent for updation successfully"}


    response = test_client.delete("/employee/delete/1", json = {"emp_name":"alice", "emp_id":1})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Employee sent for deletion successfully"}


    '''Testing Employee get'''
    emp1 = Employee( emp_id = 1, emp_name = "vikas")
    emp2 = Employee(emp_id = 2, emp_name = "rathod")
    dbsession.add(emp1)
    dbsession.add(emp2)
    dbsession.commit()
    with patch("app.db.session", new = dbsession), patch("mqtt_local.mqtt_client", return_value = mock_mqtt_client):
        response = test_client.get("/employee/fetch", json = {})
    assert response.status_code == 200
    assert response.get_json() == {"message":[{"emp_id":1,"emp_name":"vikas"}, {"emp_id":2,"emp_name":"rathod"}]}


    '''Testing Todo get'''
    todo1 = Todo(sno = 1, title = "title1", desc = "description1", employee_id = 1)
    todo2 = Todo(sno = 2, title = "title2", desc = "description2", employee_id = 1)
    dbsession.add(todo1)
    dbsession.add(todo2)
    dbsession.commit()
    with patch("app.db.session", new = dbsession), patch("mqtt_local.mqtt_client", return_value = mock_mqtt_client):
        response = test_client.get("/todo/fetch", json = {})
    assert response.status_code == 200
    assert response.get_json() == {"message":[{"title" : "title1", "desc" : "description1"}, {"title" : "title2", "desc" : "description2"}]}


    '''Testing fetching all the todos of a employee'''
    with patch("app.db.session", new = dbsession), patch("mqtt_local.mqtt_client", return_value = mock_mqtt_client):
        response = test_client.get("/todo/employeeTodo/1", json = {})
    assert response.status_code == 200
    assert response.get_json() == {"message":[{"title" : "title1", "desc" : "description1"}, {"title" : "title2", "desc" : "description2"}]}

    




    '''down the mqtt client and test the exception'''
    mock_mqtt_client.publish.side_effect = RuntimeError("MQTT client is down")


    response = test_client.post("/todo/create", json = {"title":"new_title", "desc":"new_desc"})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Failed to create todo", "error":"MQTT client is down"}


    response = test_client.put("/todo/update/1", json = {"title":"update_title", "desc":"update_desc"})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Failed to update todo", "error":"MQTT client is down"}


    response = test_client.delete("/todo/delete/1", json = {})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Failed to delete todo", "error":"MQTT client is down"}


    response = test_client.post("/employee/create", json = {"emp_name":"alice", "emp_id":1})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Failed to create employee", "error":"MQTT client is down"}


    response = test_client.put("/employee/update/1", json = {"emp_name":"update_alice", "emp_id":1})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Failed to update employee", "error":"MQTT client is down"}


    response = test_client.delete("/employee/delete/1", json = {})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Failed to delete employee", "error":"MQTT client is down"}


    '''Testing get when mqtt client is down'''
    with patch("app.db.session", new = dbsession):
        response = test_client.get("/todo/fetch", json = {})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Failed to fetch todo's", "error":"MQTT client is down"}


    with patch("app.db.session", new = dbsession):
        response = test_client.get("/todo/employeeTodo/1", json = {})
    assert response.status_code == 400
    assert response.get_json() == {"message":"Failed to fetch employee's Todo", "error":"MQTT client is down"}


    with patch("app.db.session", new = dbsession):
        response = test_client.get("/employee/fetch", json = {})
    assert response.status_code == 400
    assert response.get_json() == {"message": "Failed to fetch employees", "error":"MQTT client is down"}




# #Testing methods
def test_todo_create_data(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    # message.payload.decode.return_value = json.dumps({'title': 'Alice', 'desc': 'Hello'})
    message.payload.decode.return_value = "Alice,Hello"
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        t_methods.create_data(client, None, message)
    new_todo = dbsession.query(Todo).filter_by(title='Alice').first()
    assert new_todo.title == "Alice"
    assert new_todo.desc == "Hello"
    client.publish.assert_called_with("store_msg", f"Todo created successfully with id: {new_todo.sno}")

def test_todo_create_data_exceptoin(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    message.payload.decode.return_value = "Hello"
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        t_methods.create_data(client, None, message)
    client.publish.assert_called_with("store_msg", f"Failed to create todo")



def test_todo_update_data(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    todo = Todo(title = 'title', desc = 'description')
    dbsession.add(todo)
    dbsession.commit()
    sno = str(todo.sno)
    employee_id = None
    payload = "updated_title,updated_description," + sno +","+ "None"
    # message.payload.decode.return_value = "updated_title, updated_description,{sno},{employee_id}"
    message.payload.decode.return_value = payload
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        t_methods.update_data(client, None, message)
    updated_todo = dbsession.query(Todo).filter_by(sno=todo.sno).one()
    assert updated_todo.title == "updated_title"
    assert updated_todo.desc == "updated_description"
    client.publish.assert_called_with("store_msg", f"Task updated successfully for id: {sno}")


def test_todo_update_data_when_assiging_to_employee(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    todo = Todo(title = 'title', desc = 'description')
    emp = Employee(emp_id = 1, emp_name = "vikas")
    dbsession.add_all({todo,emp})
    dbsession.commit()
    sno = str(todo.sno)
    employee_id = 1
    payload = "title,description,"+str(sno)+","+str(employee_id)
    message.payload.decode.return_value = payload
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        t_methods.update_data(client, None, message)
    updated_todo_with_employee = dbsession.query(Todo).filter_by(sno=todo.sno).one()
    assert updated_todo_with_employee.title == "title"
    assert updated_todo_with_employee.desc == "description"
    assert updated_todo_with_employee.employee_id == 1
    client.publish.assert_called_with("store_msg", f"Task updated successfully for id: {sno}")




def test_todo_update_data_exceptoin(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    todo = Todo(title = 'title', desc = 'description')
    dbsession.add(todo)
    dbsession.commit()
    sno = str(todo.sno)
    employee_id = None
    payload = "updated_title,updated_description,"+","+ "None"
    message.payload.decode.return_value = payload
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        t_methods.update_data(client, None, message)
    client.publish.assert_called_with("store_msg", f"Failed to update todo")



def test_todo_delete_data(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    todo = Todo(title = "title", desc = "description")
    dbsession.add(todo)
    dbsession.commit()
    message.payload.decode.return_value = str(todo.sno)
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        t_methods.delete_data(client, None, message)
    deleted_todo = dbsession.query(Todo).filter_by(sno=todo.sno).first()
    assert deleted_todo is None
    client.publish.assert_called_with("store_msg", f"Task deleted successfully for id: {todo.sno}")


def test_todo_delete_data_exception(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    todo = Todo(title = "title", desc = "description")
    dbsession.add(todo)
    dbsession.commit()
    message.payload.decode.return_value = str(13)
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        t_methods.delete_data(client, None, message)
    client.publish.assert_called_with("store_msg",f"Failed to delete todo")


'''Testing the methods of the employee'''
def test_employee_create_data(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    # message.payload.decode.return_value = json.dumps({'title': 'Alice', 'desc': 'Hello'})
    message.payload.decode.return_value = "1,vikas"
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        e_methods.create_data(client, None, message)
    new_emp = dbsession.query(Employee).filter_by(emp_id=1).first()
    assert new_emp.emp_id == 1
    assert new_emp.emp_name == "vikas"
    client.publish.assert_called_with("store_msg", f"employee created successfully with id: {new_emp.emp_id}")


def test_employee_create_data_exception(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    message.payload.decode.return_value = "vikas"
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        e_methods.create_data(client, None, message)
    client.publish.assert_called_with("store_msg", f"Failed to create employee")


def test_employee_update_data(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    emp = Employee(emp_id = 1, emp_name = 'rathod')
    dbsession.add(emp)
    dbsession.commit()
    message.payload.decode.return_value = "1,vikas"
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        e_methods.update_data(client, None, message)
    updated_emp = dbsession.query(Employee).filter_by(emp_id=1).one()
    assert updated_emp.emp_id == emp.emp_id
    assert updated_emp.emp_name == "vikas"
    client.publish.assert_called_with("store_msg", f"Employee upated successfully for id {emp.emp_id}")


def test_employee_update_data_exception(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    message.payload.decode.return_value = "vikas"
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        e_methods.update_data(client, None, message)
    client.publish.assert_called_with("store_msg", f"Failed to update employee")



def test_employee_delete_data(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    emp = Employee(emp_id = 1, emp_name = 'rathod')
    dbsession.add(emp)
    dbsession.commit()
    message.payload.decode.return_value = str(emp.emp_id)
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        e_methods.delete_data(client, None, message)
    deleted_emp = dbsession.query(Employee).filter_by(emp_id=emp.emp_id).first()
    assert deleted_emp is None
    client.publish.assert_called_with("store_msg", f"Employee deleted successfully for id: {emp.emp_id}")


def test_employee_delete_data_exception(dbsession, mock_app):
    client = MagicMock()
    message = MagicMock()
    emp = Employee(emp_id = 1, emp_name = 'rathod')
    dbsession.add(emp)
    dbsession.commit()
    message.payload.decode.return_value = str(12)
    with patch('app.db.session', new = dbsession), patch('app.app', return_value=mock_app):
        e_methods.delete_data(client, None, message)
    client.publish.assert_called_with("store_msg", f"Filed to delete Employee")


'''Testing Employee Model'''
def test_employee_model(dbsession, mock_app):
    emp = Employee(emp_id = 1, emp_name = 'rathod')
    dbsession.add(emp)
    dbsession.commit()
    assert repr(emp) == "<Employee rathod>"


'''Testing Todo Model'''
def test_todo_model(dbsession, mock_app):
    todo = Todo(title = 'title', desc = 'rathod')
    dbsession.add(todo)
    dbsession.commit()
    assert repr(todo) == f"<Todo {todo.sno} - {todo.title, todo.desc}>"