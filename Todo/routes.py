from flask import Blueprint, jsonify, request
import json
todo_bp = Blueprint("todo_bp", __name__)


# GET method for api calling
@todo_bp.route('/fetch', methods=["GET"])
def get_data():
    try:
        from mqtt_local import mqtt_client as CLIENT
        from Todo.models import Todo
        allTodo = Todo.query.all()
        todo_list = [{'sno': todo.sno, 'title': todo.title, 'desc': todo.desc} for todo in allTodo]
        CLIENT.publish("store_msg", "Fetched all the todo's")
        return jsonify(todo_list)
    except Exception as e:
        return jsonify({"message": "Failed to fetch todo's", "error":str(e)}), 400




#Post method for postman usage
@todo_bp.route("/create", methods=["POST"])
def fun_create():
    try:
        # print("check->> in create route")
        from mqtt_local import mqtt_client as CLIENT
        # from mqtt_local import init_mqtt
        import time
        data = request.json
        title = data['title']
        desc = data['desc']
        # print(f"Routes-->>Publishing to flask/mqtt/create/todo")
        CLIENT.publish('flask/mqtt/create/todo', f"{title},{desc}")
        # print("Routes-->> after publishing payload to the topic check")
        return {"message": "Todo sent to creation successfully"}, 200
    except Exception as e:
        return jsonify({"message": "Failed to create todo", "error":str(e)}), 400

            
#Update method for postman usage
@todo_bp.route("/update/<int:sno>" , methods=['PUT']  )
def put_data(sno):
    try:
        from mqtt_local import mqtt_client as CLIENT
        data = request.json
        title = data.get('title')
        desc = data.get('desc')
        # can be used if else here
        employee_id = data.get('employee_id')
        print('Publishing to flask/mqtt/update/todo')
        CLIENT.publish('flask/mqtt/update/todo', f"{title},{desc},{sno},{employee_id}")
        return {"message": "Todo sent for updation successfully"}, 200
    except Exception as e:
        print(f"There is an error: {e}")
        return {"error": "There is an error, please check the update code"}, 400

# Delete using postman api
@todo_bp.route("/delete/<int:sno>", methods=['DELETE'])
def delete_data(sno):
    try:
        from mqtt_local import mqtt_client as CLIENT
        import time
        # time.sleep(2)
        CLIENT.publish('flask/mqtt/delete/todo', f"{sno},")
        return {"message": "Todo published for deletion"}, 200
    except Exception as e:
        return {"message": "Failed to delete Todo"}, 400


#todo assigned to employees
@todo_bp.route("/employeeTodo/<int:employee_id>", methods=['GET'])
def emp_tasks(employee_id):
    try:
        from mqtt_local import mqtt_client as CLIENT
        from Todo.models import Todo
        empTodos = Todo.query.filter_by(employee_id = employee_id).all()
        temp = []
        for item in empTodos:
            temp.append({
                # 'sno':item.sno,
                'title':item.title,
                'desc':item.desc,
                # 'employee_id':item.employee_id
            })
        CLIENT.publish("store_msg", f"Fetched all the todo's of employee {employee_id}")
        return jsonify(temp)
    except:
        return {"message": "Failed to fetch employee's Todo"}, 400