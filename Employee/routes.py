from flask import Blueprint, jsonify, request
from .models import Employee
from mqtt_local import mqtt_client
from db import db

employee_bp = Blueprint("employee", __name__)


# GET method for api calling
@employee_bp.route('/fetch', methods=["GET"])
def get_data():
    try:
        # allemp = Employee.query.all()
        allemp = db.session.query(Employee).all()
        emp_list = [{'emp_id': emp.emp_id, 'emp_name': emp.emp_name} for emp in allemp]
        mqtt_client.publish("store_msg", "Fetched all the employees")
        return jsonify({"message":emp_list}), 200
    except Exception as e:
        print(f"checking in the fetch routen exception\n {e}")
        return jsonify({"message": "Failed to fetch employees", "error":str(e)}), 400


#Post method for postman usage
@employee_bp.route("/create", methods=["POST"])
def fun_create():
    try:
        data = request.json
        emp_id = data['emp_id']
        emp_name = data['emp_name']
        print(f"a)Publishing to flask/mqtt/create/employee")
        mqtt_client.publish('flask/mqtt/create/employee', f"{emp_id},{emp_name}")
        return jsonify({"message": "Employee sent for creation successfully"}), 200
    except Exception as e:
        print(f"Emp/route/create -->>There is an error: {e}")
        return jsonify({"message": "Failed to create employee", "error":str(e)}), 400


#Update method for postman usage
@employee_bp.route("/update/<int:emp_id>" , methods=['PUT']  )
def put_data(emp_id):
    try:
        data = request.json
        emp_id = data.get('emp_id')
        emp_name = data.get('emp_name')
        print('b)Publishing to flask/mqtt/update/employee')
        mqtt_client.publish('flask/mqtt/update/employee', f"{emp_id},{emp_name}")
        return {"message": "Employee sent for updation successfully"}, 200
    except Exception as e:
        print(f"Emp/route/update -->>There is an error: {e}")
        return jsonify({"message": "Failed to update employee", "error":str(e)}), 400


# Delete using postman api
@employee_bp.route("/delete/<int:sno>", methods=['DELETE'])
def delete_data(sno):
    try:
        print("c)Publishing to flask/mqtt/delete/employee")
        mqtt_client.publish('flask/mqtt/delete/employee', f"{sno},")
        return {"message": "Employee sent for deletion successfully"}, 200
    except Exception as e:
        print(f"Emp/route/delete -->>There is an error: {e}")
        return jsonify({"message": "Failed to delete employee", "error":str(e)}), 400