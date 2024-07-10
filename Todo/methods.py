import logger

def create_data(client, userdata, message):
    try:
        from app import app,db
        from Todo.models import Todo
        with app.app_context():
            payload = message.payload.decode("utf-8")
            temp = payload.split(',')
            title = temp[0]
            desc = temp[1]
            todo = Todo(title = title, desc = desc)
            db.session.add(todo)
            db.session.commit()
            client.publish("store_msg", f"Task created successfully with id: {todo.sno}")
    except Exception as e:
        client.publish("on_publish", "\nTask creation failed")
        logger.error(f"Failed to create task: {e}")


# this method includes both employee assigning to todo, and each toso update
def update_data(client, userdata, message):
    from app import app, db
    from Todo.models import Todo
    try:
        with app.app_context():
            payload = message.payload.decode("utf-8")
            temp = payload.split(',')
            title = temp[0]
            desc = temp[1]
            sno = int(temp[2])
            employee_id = "None"
            if(temp[3] != "None"):
                employee_id = int(temp[3])
            todo = Todo.query.filter_by(sno=sno).first()
            if(employee_id != "None"):
                todo.employee_id = employee_id
                client.publish("store_msg", f"Todo assigned suceessfully for employee:{employee_id}")
            else:
                todo.title = title
                todo.desc = desc
                # print(f"\ncheck -> {todo.title}, {todo.desc}\n")
                client.publish("store_msg", f"Task updated successfully for id: {sno}")
            db.session.commit()  # No need to add the todo again, just commit changes
    except Exception as e:
            client.publish("store_msg", f"Updation of task failed for task")
            logger.error(f"Failed to update todo: {e}")


def delete_data(client, userdata, message):
    print("methods --> entered in deleted call back method")
    from app import app,db
    from Todo.models import Todo
    try:
        with app.app_context():
            payload = message.payload.decode("utf-8")
            temp = payload.split(',')
            sno = int(temp[0])
            todo = Todo.query.filter_by(sno=sno).first()
            db.session.delete(todo)
            db.session.commit()
            client.publish("store_msg", f"Task deleted successfully for id: {sno}")
    except Exception as e:
        payload = message.payload.decode("utf-8")
        temp = payload.split(',')
        sno = int(temp[0])
        logger.error(f"Failed to delete task for id: {sno}\n {e}")