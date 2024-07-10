from db import db

#My database relationship is multiple todo's can be done by single employee
# one (employee) to many (todo's)

class Employee(db.Model):
    __tablename__ = "employee"
    emp_id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(50), nullable=False)
    #employee can do multiple todo
    todos = db.relationship('Todo', backref='employee')
    def __repr__(self):
        return f"<Employee {self.emp_name}>"    
