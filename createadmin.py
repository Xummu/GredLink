from gredlink_app import create_app
from models.user import User
from extensions import db


app = create_app()
with app.app_context():
    admin = User(username='admin',role='admin',email="997780644@qq.com",real_name='홍길동',phone='01097882857')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()