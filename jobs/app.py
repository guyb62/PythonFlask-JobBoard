from flask import Flask, render_template, g
import sqlite3

PATH = 'db/jobs.sqlite' # constant

app = Flask(__name__)
def open_connection():
    connection = getattr(g, '_connection', None) # returns the class attribute '_connection' form object g with a default None
    if connection is None:
        #connection = g._connection = sqlite3.connect(PATH)
        connection, g._connection = sqlite3.connect(PATH)

    connection.row_factory = sqlite3.Row
    return connection

# query db
def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)

    if commit is True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall() # ternary if

    cursor.close()
    return results

@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()

@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')