"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

connect_db(app)
db.drop_all()
db.create_all()

new_user = User(first_name="Marco", last_name="Herrera")
db.session.add(new_user)
db.session.commit()

@app.route('/')
def start():
    return redirect("/users")

@app.route('/users')
def homepage():
    """ Homepage """
    users = User.query.all()
    return render_template('users.html',users=users)

@app.route('/users/new', methods=['GET'])
def load_create_page():
    return render_template('create.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    url=image_url=request.form['img_url']
    if(len(url)== 0):
        create_new_user=User(first_name = request.form['first_name'], last_name=request.form['last_name'])
    else:
        create_new_user=User(first_name = request.form['first_name'], last_name=request.form['last_name'], image_url=url)
    db.session.add(create_new_user)
    db.session.commit()
    return redirect('/users')

@app.route("/users/<int:usr_id>")
def user_info(usr_id):
    user=User.query.get(usr_id)
    return render_template('user.html', user=user)

@app.route("/users/<int:usr_id>/edit", methods=['GET'])
def get_edit_user(usr_id):
    user=User.query.get(usr_id)
    return render_template('edituser.html',user=user)

@app.route("/users/<int:usr_id>/edit", methods=['post'])
def edit_usr(usr_id):
    user=User.query.get(usr_id)
    user.first_name = request.form['first_name'] 
    user.last_name=request.form['last_name'] 
    user.image_url=request.form['img_url']
    db.session.commit()
    return redirect('/users')

@app.route("/users/<int:usr_id>/delete", methods=['post'])
def delete_usr(usr_id):
    User.query.filter_by(id=usr_id).delete()
    db.session.commit()
    return redirect('/users')