from unittest import TestCase
from app import app
from flask import request, jsonify
from models import db, connect_db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
db.drop_all()
        

class FlaskTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        db.create_all()
        self.client = app.test_client()
        app.config['TESTING'] = True
        new_user = User(first_name="Marco", last_name="Herrera")
        db.session.add(new_user)
        db.session.commit()
        new_post = Post(title="First Post",content="stuff", user_id='1')
        db.session.add(new_post)
        db.session.commit()

    def tearDown(self):
        """ clean up after each test """
        db.drop_all()

    def test_get_users(self):
        """ route to users page show all users """

        response= self.client.get('/users')
        self.assertIn(b'Marco Herrera',response.data)

    def test_get_create_user_form(self):
        """ test that new user form is rendered """

        response = self.client.get('/users/new')
        self.assertIn(b'First Name:',response.data)
        self.assertIn(b'Last Name:',response.data)
        self.assertIn(b'Image URL:',response.data)

    def test_creating_user(self):
        """ test that user is created and added to user """
        form={'first_name':'Alex', 'last_name':'Herrera', 'img_url':''}
        self.client.get('/', follow_redirects= True)
        response=self.client.post('/users/new', data=form, follow_redirects=True )
        
        self.assertIn(b'Alex Herrera', response.data)
        self.assertIn(b'User Added',response.data)

    def test_user_page(self):
        """test that user page shows info """

        response = self.client.get('/users/1')
        self.assertIn(b'Marco Herrera', response.data)
        self.assertIn(b'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1200px-No_image_available.svg.png',response.data )
        self.assertIn(b'First Post',response.data)

    def test_edit_user_page(self):
        """test edit user info page"""

        response = self.client.get('/users/1/edit')
        self.assertIn(b'First Name:', response.data)
        self.assertIn(b'Last Name:', response.data)
        self.assertIn(b'Image URL', response.data)
        self.assertIn(b'Marco', response.data)
        self.assertIn(b'Herrera', response.data)
        self.assertIn(b'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1200px-No_image_available.svg.png',response.data )

    def test_edit_user(self):
        """ test that user is created and added to user """

        form={'first_name':'Alex', 'last_name':'Bob', 'img_url':'https://static01.nyt.com/images/2019/06/17/science/17DOGS/17DOGS-superJumbo.jpg'}
        response=self.client.post('/users/1/edit', data=form, follow_redirects=True )
        
        self.assertIn(b'Alex Bob', response.data)
        self.assertIn(b'User Edited', response.data)

    def test_delete_user(self):
        """test user deleted """

        response = self.client.get('/users')
        self.assertIn(b'Marco Herrera', response.data)
        response = self.client.post('/users/1/delete',follow_redirects=True)
        self.assertNotIn(b'Marco Herrera',response.data)

    # Posts test

    def test_post_form(self):
        """ test new post form """

        response=self.client.get('/users/1/posts/new')
        self.assertIn(b'Title:',response.data)
        self.assertIn(b'Content:',response.data)

    def test_create_post(self):
        """ test create new post """

        form={'title':'Test Post', 'content':'second post as test'}
        response=self.client.post('/users/1/posts/new', data=form, follow_redirects=True )
        self.assertIn(b'Test Post',response.data)
        self.assertIn(b'second post as test', response.data)

    def test_post_page(self):
        """ test post info page """

        response = self.client.get('/posts/1')
        self.assertIn(b'First Post',response.data)
        self.assertIn(b'stuff', response.data)

    def test_edit_post_page(self):
        """ test page to edit post """
        
        response = self.client.get('/posts/1/edit')
        self.assertIn(b'Title:',response.data)
        self.assertIn(b'Content:',response.data)
        self.assertIn(b'First Post',response.data)
        self.assertIn(b'stuff', response.data)

    def test_edit_post(self):
        """ test edit post """

        form={'title':'Edited Post', 'content':'new content'}
        response=self.client.post('/posts/1/edit', data=form, follow_redirects=True )
        self.assertIn(b'Edited Post',response.data)
        self.assertIn(b'new content', response.data)

    def test_delete_post(self):
        """ test deleting post """

        response = self.client.get('/users/1')
        self.assertIn(b'First Post', response.data)
        response = self.client.post('/posts/1/delete')
        self.assertNotIn(b'First Post',response.data)