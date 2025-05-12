from flask import Flask,render_template
from extensions import db,login_manager,migrate
from config import SQLALCHEMY_DATABASE_URI,SECRET_KEY,SQLALCHEMY_TRACK_MODIFICATIONS
from routes.auth import auth_bp
from models.user import User
from routes.main import main_bp
from routes.admin import admin_bp


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)

    #import config
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=SQLALCHEMY_TRACK_MODIFICATIONS

    #db초기화
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    #login보호
    login_manager.login_view = 'auth.login'

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
