import re
from datetime import datetime as dt
from flask import Flask, render_template, redirect, session, flash, request
from mysqlconnection import MySQLConnector

REGEX_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


app = Flask(__name__)
app.secret_key = "secret:"
mysql = MySQLConnector(app, 'flask_review')

@app.route('/')
def index():
    if 'user_id' in session:
        all_users = mysql.query_db('select * from users')
        return render_template('index.html', template_all_users=all_users)
    return render_template('index.html')

@app.route('/login_and_registration')
def login_reg():
    return render_template('login_reg.html')

@app.route('/register', methods=['POST'])
def register():
    success = True

    server_email = request.form['html_email']
    server_username = request.form['html_username']
    server_password = request.form['html_password']
    server_confirm = request.form['html_confirm']

    # do some validation on the input
    if server_confirm != server_password:
        flash('passwords do not match')
        success = False

    if REGEX_EMAIL.search(server_email) is None:
        flash("Email is not valid")
        success = False

    if success:
        sql_parameters = {
            'server_email': server_email,
            'sql_username': server_username,
            'sql_password': server_password,
            'created_at': dt.now(),
            'updated_at': dt.now()
        }

        sql_insert_user = 'insert into users(email, username, password, created_at, updated_at) values (:server_email, :sql_username, :sql_password, :created_at, :updated_at)'

        user_id_from_db = mysql.query_db(sql_insert_user, sql_parameters)
        
        print "-----------------------"
        print user_id_from_db
        print "-----------------------"

        session['user_id'] = user_id_from_db
        session['user_email'] = server_email
        session['user_name'] = server_username


        return redirect('/')
    else:
        flash('Invalid registration')
        return redirect('/login_and_registration')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/edit/<user_id>')
def edit(user_id):
    sql_parameters = {
        'user_id': user_id
    }

    sql_find_user_by_id = 'select * from users where id = :user_id'
    
    result = mysql.query_db(sql_find_user_by_id, sql_parameters)
    if len(result) == 1:
        user = result[0]
        return render_template('edit.html' , user = user)
    else:
        flash('invalid operation SON!')
        return redirect('/')

@app.route('/update_user', methods=['POST'])
def update_user():
    success = True

    server_id = request.form['html_id']
    server_email = request.form['html_email']
    server_username = request.form['html_username']
    server_password = request.form['html_password']
    server_confirm = request.form['html_confirm']

    # do some validation on the input
    if server_confirm != server_password:
        flash('passwords do not match')
        success = False

    if REGEX_EMAIL.search(server_email) is None:
        flash("Email is not valid")
        success = False

    
    if success:
        sql_parameters = {
            'server_email': server_email,
            'sql_username': server_username,
            'sql_password': server_password,
            'updated_at': dt.now(),
            'user_id': server_id
        }

        sql_update_user = 'update users set username = :sql_username,  password = :sql_password, email = :server_email,  updated_at = :updated_at where id = :user_id'

        user_id_from_db = mysql.query_db(sql_update_user, sql_parameters)
        return redirect('/')
    else:
        flash('FIX YER DATA SON!')
        return redirect('/edit/{}'.format(server_id))


app.run(debug=True)
