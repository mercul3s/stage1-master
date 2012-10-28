"""
model.py
"""
import sqlite3
import datetime

TASK_COLS = ['id', 'title', 'created_at', 'completed_at', 'user_id']


def connect_db():
    return sqlite3.connect("tipsy.db")

class User(object):
    # def __init__(self, user_id, email, password, name):
    #     self.id = user_id
    #     self.email = email
    #     self.password = password
    #     self.name = name
    COLS = ['id', 'email', 'password', 'username']
    TABLE_NAME = 'Users'

    def new(cls, db, email, password, name):
        vals = [email, password, name]
        return insert_into_table(db, cls.TABLE_NAME, cls.COLS, vals)

    @classmethod
    def authenticate(cls, db, email, password):
        c = db.cursor()
        query = """SELECT * from %s WHERE email=? AND password=?"""%(cls.TABLE_NAME)
        c.execute(query, (email, password))
        result = c.fetchone()
        if result:
            return cls(*result)
            # the above is equivalent to return cls(result[0], result[1], result[2], result[3])
            # fields = ["id", "email", "password", "username"]
            # return make_user(result)
        else:
            return None

# class Task(object):
#     def __init__(self, title, user_id):
#         pass

# '''
# User Functions
# '''

# takes in returned database row, returns dictionary with headers as keys
def make_user(row):
    return User(row[0], row[1], row[2], row[3])


def get_user(db, user_id):
    return get_from_table_by_id(db, 'Users', user_id, make_user)

# def new_user(db, email, password, name):
#     vals = [email, password, name]
#     return insert_into_table(db, 'Users', USER_COLS, vals)


'''
Task Functions
'''
# takes in returned database row, returns dictionary with headers as keys
def make_task(row):
    columns = ["id", "title", "created_at", "completed_at", "user_id"]
    return dict(zip(columns, row))

def get_task(db, task_id):
    return get_from_table_by_id(db, 'Tasks', task_id, make_task)

def new_task(db, title, user_id):
    vals = [title, datetime.datetime.now(), None, user_id]
    return insert_into_table(db, 'Tasks', TASK_COLS, vals)

def complete_task(db, task_id):
    """Mark the task with the given task_id as being complete."""
    c = db.cursor()
    query = """UPDATE Tasks SET completed_at=DATETIME('now') WHERE id=?"""
    res = c.execute(query, (task_id,))
    if res:
        db.commit()
        return res.lastrowid
    else:
        return None

def get_tasks(db, user_id=None):
    """Get all the tasks matching the user_id, getting all the tasks in the system if the user_id is not provided. Returns the results as a list of dictionaries."""
    c = db.cursor()
    if user_id:
        query = """SELECT * from Tasks WHERE user_id = ?"""
        c.execute(query, (user_id,))
    else:
        query = """SELECT * from Tasks"""
        c.execute(query)
    tasks = []
    rows = c.fetchall()
    for row in rows:
        task = make_task(row)
        tasks.append(task)
    return tasks

def delete_task(db, task_id):
    c=db.cursor()
    query="""DELETE FROM Tasks WHERE id = ?"""
    c.execute(query,(task_id, ))
    db.commit()
    print "Task ID is: ", task_id
    #return 'Task Deleted'

'''
Common Functions
'''

def get_from_table_by_id(db, table_name, query_id, make_dict):
    c = db.cursor()
    query_template = """SELECT * FROM %s WHERE id = ?"""
    query = query_template%table_name
    c.execute(query, (query_id,))
    result = c.fetchone()
    if result:
        return make_dict(result)
    return None

def insert_into_table(db, table_name, columns, values):  
    sub_values = ['NULL'] + ['?'] * (len(columns) - 1)
    join_sub_values = ", ".join(sub_values)        
    c = db.cursor()                                     
    query_template = """INSERT INTO %s VALUES (%s)"""   
    query = query_template%(table_name, join_sub_values)                                                
    res = c.execute(query, tuple(values))           
    if res:
        db.commit()
        return res.lastrowid

