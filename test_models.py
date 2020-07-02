from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = True

db.drop_all()
db.create_all()

class ModelsTestCases(TestCase):
    """ Test for all models in blogly """

    def setUp(self):
        """ clean up existing opjects """
        Post.query.delet()
        User.query.delete()
        

    def tearDown(self):
        """ clean up any fouled transaction """
        db.session.rollback()

    def test_get_full_name(self):
        """ Test getting full name of a user """
        new_user=User(first_name="Marco",last_name= "Herrera")
        self.assertEqual(new_user.get_full_name, "Marco Herrera")