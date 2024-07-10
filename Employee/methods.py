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
            print(f"checking row ->{emp} \n {emp_id}, {emp_name}")
            db.session.add(emp)
            db.session.commit()
            client.publish("store_msg", f"employee created successfully with id: {emp.emp_id}")
    except Exception as e:
        client.publish("store_msg", f"Employee creation failed")
        logger.error(f"Failed to create employee: {e}")
        


def update_data(client, userdata, message):
    from app import app
    from db import db
    try:
        with app.app_context():
            from Employee.models import Employee
            payload = message.payload.decode("utf-8")
            temp = payload.split(',')
            emp_id = int(temp[0])
            emp_name = temp[1]
            emp = Employee.query.filter_by(emp_id=emp_id).first()
            emp.emp_id = emp_id
            emp.emp_name = emp_name
            db.session.commit()
            client.publish("store_msg", f"Employee updated suceessfully for id:{emp_id}")
    except Exception as e:
        payload = message.payload.decode("utf-8")
        temp = payload.split(',')
        client.publish("store_msg", f"Failed to update Employee for id:{temp[0]}")
        logger.error(f"Failed to create employee: {e}")
        
            
def delete_data(client, userdata, message):
    try:
        from app import app
        from db import db
        from Employee.models import Employee
        with app.app_context():
            payload = message.payload.decode("utf-8")
            temp = payload.split(',')
            emp_id = int(temp[0])
            emp = Employee.query.filter_by(emp_id=emp_id).first()
            db.session.delete(emp)
            db.session.commit()
            client.publish("store_msg", f"Employee deleted successfully for id: {emp_id}")
    except Exception as e:
        logger.error("store_msg", f"Filed to deleted Employee")