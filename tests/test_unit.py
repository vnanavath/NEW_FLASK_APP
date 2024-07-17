

def test_todo(new_todo):
    assert new_todo.title == "new_todo"
    assert new_todo.desc == "new_desc"

def test_employee(new_emp):
    assert new_emp.emp_id == 1
    assert new_emp.emp_name == "alice"