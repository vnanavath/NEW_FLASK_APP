# import threading
import pymysql # type: ignore
import mqtt_local


from mysql_configeration import MysqlConfig
from flask import Flask, render_template, request, redirect, jsonify, Blueprint
from datetime import datetime, timezone
from flask_migrate import Migrate
from db import db
from flask_cors import CORS
from Todo.routes import todo_bp
from Employee import routes


app = Flask(__name__, instance_relative_config=True)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = MysqlConfig().SQLALCHEMY_DATABASE_URI
db.init_app(app)


print("Starting app")


migrate = Migrate()
migrate.init_app(app, db)


mqtt_local.init_mqtt()
@app.route('/', methods=['GET'])
def home():
    # from Todo.models import Todo
    # allTodo = Todo.query.all()
    # return render_template("index.html", allTodo = allTodo)
    return "Hello World!"


app.register_blueprint(routes.employee_bp, url_prefix="/employee")


app.register_blueprint(todo_bp, url_prefix="/todo")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader = False)