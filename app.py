"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/', methods=['GET', 'POST'])
def start():
    return redirect("/users")

@app.route('/users')
def homepage():
    """ Homepage """
    users = User.query.order_by(User.last_name).all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET'])
def load_create_page():
    """New user info page """
    return render_template('create.html')

@app.route('/users/<bg_color>')
def user_added(bg_color):
    """ Homepage with sucess/error message"""
    users = User.query.order_by(User.last_name).all()
    return render_template('users.html', users=users, bg_color=bg_color)  

@app.route('/users/new', methods=['POST'])
def create_user():
    """ Create the new user """

    url=request.form['img_url']
    try:
        if(len(url)== 0):
            create_new_user=User(first_name = request.form['first_name'], last_name=request.form['last_name'])
        else:
            create_new_user=User(first_name = request.form['first_name'], last_name=request.form['last_name'], image_url=url)
        db.session.add(create_new_user)
        db.session.commit()
        bg_color='success'
        flash("User Added")
    except:
        flash("Error: Could not Create User. Try again")
        bg_color='danger'
    
    return redirect(f'/users/{bg_color}')

@app.route("/users/<int:usr_id>")
def user_info(usr_id):
    """ Show user info and posts"""
    user=User.query.get(usr_id)
    posts=Post.query.filter(Post.user_id==usr_id)
    return render_template('user.html', user=user, posts=posts)

@app.route("/users/<int:usr_id>/edit", methods=['GET'])
def get_edit_user(usr_id):
    """ Edit user info """
    user=User.query.get(usr_id)
    return render_template('edituser.html',user=user)

@app.route("/users/<int:usr_id>/edit", methods=['post'])
def edit_usr(usr_id):
    """ Edit the changed info """
    try: 
        user = User.query.get(usr_id)
        user.first_name = request.form['first_name'] 
        user.last_name=request.form['last_name'] 
        user.image_url=request.form['img_url']
        db.session.commit()
        bg_color='success'
        flash("User Edited")
    except:
        flash("Error: Could not Edit User. Try again")
        bg_color='danger'
    return redirect(f'/users/{bg_color}')

@app.route("/users/<int:usr_id>/delete", methods=['post'])
def delete_usr(usr_id):
    """ Delete user """
    try:
        user=User.query.filter_by(id=f'{usr_id}').first()
        db.session.delete(user)
        db.session.commit()
        bg_color='success'
        flash("User Deleted")
    except:
        flash("Error: Could not Delete User. Try again")
        bg_color='danger'
    return redirect(f'/users/{bg_color}')

# posts routes
@app.route('/users/<usr_id>/posts/new')
def post_form(usr_id):
    """ new post form """
    return render_template('newpost.html', user_id=usr_id)

@app.route('/users/<usr_id>/posts/new', methods=['POST'])
def create_form(usr_id):
    """ Create New Post """
    create_post = Post(title=request.form['title'],content=request.form['content'], user_id=usr_id)
    db.session.add(create_post)
    db.session.commit()
    return redirect(f'/posts/{create_post.id}')

@app.route('/posts/<post_id>')
def post(post_id):
    """ show post """
    post= Post.query.get(post_id)
    return render_template("post.html", post = post)

@app.route('/posts/<post_id>/edit')
def edit_post_info(post_id):
    """ show edit post """
    post= Post.query.get(post_id)
    return render_template("editpost.html", post=post)

@app.route('/posts/<post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """ edit post """
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """ delete post """
    post = Post.query.filter_by(id=post_id).first()
    id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{id}')