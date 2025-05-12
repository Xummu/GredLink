from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(255), default='img/icon.png')
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user') # 'admin','buser','user'
    is_delete = db.Column(db.Boolean, default=False) #삭제표기
    real_name = db.Column(db.String(64), nullable=False) #이름
    phone = db.Column(db.String(20), nullable=False) #전화번호


    def set_password(self, password):
        self.password_hash = generate_password_hash(password,method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return not self.is_delete