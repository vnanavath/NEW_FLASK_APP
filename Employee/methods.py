import logger


def create_data(client, userdata, message):
    from app import app
    from db import db
    from Employee.models import Employee
    from Todo.models import Todo
    try:
        with app.app_context():
            payload = message.payload.decode("utf-8")
            temp = payload.split(',')
            emp_id = int(temp[0])
            emp_name = temp[1]
            emp = Employee(emp_id = emp_id, emp_name = emp_name)
            db.session.add(emp)
            db.session.commit()
            client.publish("store_msg", f"employee created successfully with id: {emp.emp_id}")
    except Exception as e:
        print(e)
        client.publish("store_msg",f"Failed to create employee")
        

def update_data(client, userdata, message):
    from app import app
    from db import db
    from Employee.models import Employee
    from Todo.models import Todo
    try:
        with app.app_context():
            payload = message.payload.decode("utf-8")
            temp = payload.split(',')
            emp_id = int(temp[0])
            emp_name = temp[1]
            # emp = Employee.query.filter_by(emp_id=emp_id).first()
            emp = db.session.query(Employee).filter_by(emp_id=emp_id).one()
            emp.emp_id = emp_id
            emp.emp_name = emp_name
            db.session.commit()
            client.publish("store_msg", f"Employee upated successfully for id {emp_id}")
    except Exception as e:
        print(e)
        client.publish("store_msg",f"Failed to update employee")
        
            
def delete_data(client, userdata, message):
    from app import app
    from db import db
    from Employee.models import Employee
    try:
        with app.app_context():
            payload = message.payload.decode("utf-8")
            temp = payload.split(',')
            emp_id = int(temp[0])
            # emp = Employee.query.filter_by(emp_id=emp_id).first()
            emp = db.session.query(Employee).filter_by(emp_id=emp_id).one()
            db.session.delete(emp)
            db.session.commit()
            client.publish("store_msg", f"Employee deleted successfully for id: {emp_id}")
    except Exception as e:
        print(e)
        client.publish("store_msg",f"Filed to delete Employee")
        