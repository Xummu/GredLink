from gredlink_app import create_app
from extensions import db
from models.user import User



app = create_app()
with app.app_context():
    user = User(username='testuser')
    user.set_password('1234')
    db.session.add(user)
    db.session.commit()
    print("complete!")