from flask import Blueprint, jsonify, request
from .models import Employee
from mqtt_local import mqtt_client
from db import db

employee_bp = Blueprint("employee", __name__)


# GET method for api calling
@employee_bp.route('/fetch', methods=["GET"])
def get_data():
    try:
        # from mqtt_local import mqtt_client
        allemp = Employee.query.all()
        emp_list = [{'emp_id': emp.emp_id, 'emp_name': emp.emp_name} for emp in allemp]
        mqtt_client.publish("store_msg", "Fetched all the employees")
        return jsonify(emp_list)
    except Exception as e:
        return jsonify({"message": "Failed to fetch employees", "error":str(e)}), 400


#Post method for postman usage
@employee_bp.route("/create", methods=["POST"])
def fun_create():
    try:
        # from mqtt_local import mqtt_client
        if request.method == "POST":
            data = request.json
            emp_id = data['emp_id']
            emp_name = data['emp_name']
            print(f"Publishing to flask/mqtt/create/employee")
            mqtt_client.publish('flask/mqtt/create/employee', f"{emp_id},{emp_name}")
        return jsonify({"message": "Employee sent for creation successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to created employee"}, 400)
            

#Update method for postman usage
@employee_bp.route("/update/<int:emp_id>" , methods=['PUT']  )
def put_data(emp_id):
    # from mqtt_local import mqtt_client
    if request.method == 'PUT':
        try:
            data = request.json
            emp_id = data.get('emp_id')
            emp_name = data.get('emp_name')
            print('Publishing to flask/mqtt/update/employee')
            mqtt_client.publish('flask/mqtt/update/employee', f"{emp_id},{emp_name}")
            return {"message": "Employee sent for updation successfully"}, 200
        except Exception as e:
            print(f"There is an error: {e}")
            return {"message": "Failed to update employee"}, 400


# Delete using postman api
@employee_bp.route("/delete/<int:sno>", methods=['DELETE'])
def delete_data(sno):
    # from mqtt_local import mqtt_client
    try:
        print("Publishing to flask/mqtt/delete/employee")
        mqtt_client.publish('flask/mqtt/delete/employee', f"{sno},")
        return {"message": "Todo sent for deletion successfully"}, 200
    except Exception as e:
        return {"message": "Failed to delete employee"}, 400