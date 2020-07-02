from app import app
from models import db, connect_db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'

connect_db(app)
db.drop_all()
db.create_all()

new_user = User(first_name="Marco", last_name="Herrera", image_url='https://img.webmd.com/dtmcms/live/webmd/consumer_assets/site_images/article_thumbnails/slideshows/dog_breed_health_issues_slideshow/1800x1200_dog_breed_health_issues_slideshow.jpg')
db.session.add(new_user)
db.session.commit()
new_post = Post(title="First Post",content="stuff", user_id='1')
db.session.add(new_post)
db.session.commit()