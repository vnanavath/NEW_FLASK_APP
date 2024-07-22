import logger


def create_data(client, userdata, message):
    from app import app
    from db import db
    from Todo.models import Todo
    try:
        with app.app_context():
            payload = message.payload.decode("utf-8")
            temp = payload.split(',')
            title = temp[0]
            desc = temp[1]
            todo = Todo(title = title, desc = desc)
            db.session.add(todo)
            db.session.commit()
            client.publish("store_msg", f"Todo created successfully with id: {todo.sno}")
    except Exception as e:
        print(e)
        client.publish("store_msg",f"Failed to create todo")


# this method includes both employee assigning to todo, and each toso update
def update_data(client, userdata, message):
    from app import app
    from db import db
    from Todo.models import Todo
    try:
        with app.app_context():
            payload = message.payload.decode("utf-8")
            # print(f"\n1)checking update_fun using testing\n")
            temp = payload.split(',')
            # print(f"\n2)checking update_fun using testing\n")
            title = temp[0]
            desc = temp[1]
            # print(f"3)methods -->>{title} and {desc}")
            # print(f"4)checking type of sno -->>{type(temp[2])} ")
            sno = int(temp[2])
            # print(f"5)checking type of sno -->>{type(sno)} ")
            # print(f"\n6)checking update_fun using testing\n")
            employee_id = "None"
            if(temp[3] != "None"):
                # print(f"\n7)checking update_fun using testing\n")
                employee_id = int(temp[3])
            # print(f"\n8)checking update_fun using testing\n")
            # todo = Todo.query.filter_by(sno=sno).first()
            todo = db.session.query(Todo).filter_by(sno=sno).one()

            # print(f"\n9)before update in upd_fun -> {todo.title}, {todo.desc}\n")
            if(employee_id != "None"):
                # print(f"\n10)checking update_fun using testing\n")
                todo.employee_id = employee_id
                # client.publish("store_msg", f"Todo assigned suceessfully for employee:{employee_id}")
            else:
                # print(f"\n11)checking update_fun using testing\n")
                todo.title = title
                todo.desc = desc
                # print(f"\n12)check -> {todo.title}, {todo.desc}\n")
            db.session.commit()  # No need to add the todo again, just commit changes
            client.publish("store_msg", f"Task updated successfully for id: {sno}")
    except Exception as e:
        # print(f"\n13)checking update_fun using testing")\
        print(e)
        client.publish("store_msg",f"Failed to update todo")


def delete_data(client, userdata, message):
    from app import app
    from db import db
    from Todo.models import Todo
    try:
        with app.app_context():
            payload = message.payload.decode("utf-8")
            temp = payload.split(',')
            sno = int(temp[0])
            # todo = Todo.query.filter_by(sno=sno).first()
            todo = db.session.query(Todo).filter_by(sno=sno).one()
            db.session.delete(todo)
            db.session.commit()
            client.publish("store_msg", f"Task deleted successfully for id: {sno}")
    except Exception as e:
        print(e)
        client.publish("store_msg",f"Failed to delete todo")