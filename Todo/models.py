from db import db
from datetime import datetime, timezone
from Employee.models import Employee


class Todo(db.Model): #Defining the schema of the database using class
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.emp_id'))
    # when you want to print the object of this class what do you want to see
    def __repr__(self) -> str:
        return f"<Todo {self.sno} - {self.id, self.title}>"

