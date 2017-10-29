from flask import flash, render_template, redirect, request, url_for 
from sqlalchemy.exc import SQLAlchemyError
from models import Attachment, Category, IssueHistory, Issue, Role, Status, User
from app import app
from app.database import db


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('/admin_page/admin_page.html')


@app.route('/user_page')
def user_page():
    users = db.session.query(User).all()
    return render_template('admin_page/user_page.html', users=users)


@app.route('/user_form', methods=['GET', 'POST'])
def user_form():
    if request.method == 'GET' and request.args.get('id') is None:
        return render_template('admin_page/user_form.html')

    elif request.method == 'POST':
        data = request.form.to_dict()
        newuser = User(name=data['user_name'], alias=data['user_alias'], email=data['user_email'],
                       password=None, role_id=data['user_role'], avatar=None, delete_date=None)
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('user_page'))


@app.route('/user_edit', methods=['GET', 'POST'])
def user_edit():
    if request.method == 'GET':
        user = db.session.query(User).get(request.args.get('id'))
        return render_template('admin_page/user_form.html', user=user)

    elif request.method == 'POST':
        data = request.form.to_dict()

        user = db.session.query(User).get(data.get('user_id'))
        user.name = data['user_name']
        user.alias = data['user_alias']
        user.role_id = data['user_role']
        if data['user_delete_date']:
            user.delete_date = data['user_delete_date']
        else:
            user.delete_date = None

        db.session.commit()
        return redirect(url_for('user_page'))


@app.route('/user_sort_page', methods=['GET', 'POST'])
def user_sort_page():
    data = None
    users = None

    if request.method == 'GET':
        users = db.session.query(User).all()

    if request.method == 'POST':
        data = request.form.to_dict()

    if data:
        if 'delete_date_checkbox' in data and 'role_checkbox' in data:
            users = db.session.query(User) \
                .order_by(User.role_id, User.delete_date).all()

        elif 'delete_date_checkbox' in data:
            users = db.session.query(User) \
                .order_by(User.delete_date).all()

        elif 'role_checkbox' in data:
            users = db.session.query(User) \
                .order_by(User.role_id).all()
        else:
            users = db.session.query(User) \
                .order_by(User.role_id).all()

    return render_template('admin_page/user_sort_page.html', users=users)