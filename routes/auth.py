from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and not user.is_delete and user.check_password(password):
            login_user(user)

            #根据身份跳转
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'buser':
                return redirect(url_for('buser.dashboard'))
            else:
                return redirect(url_for('main.home',role=current_user.role))

        flash('아이디 또는 비밀번호가 틀렸습니다.','danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@auth_bp.route('/id_search', methods=['GET', 'POST'])
def id_search():
    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form.get('contact')
        flash("ID찾기 미완성",'info')
    return render_template('id_search.html')


@auth_bp.route('/pass_reset', methods=['GET', 'POST'])
def pass_reset():
    if request.method == 'POST':
        contact = request.form.get('contact')
        flash('임시 비밀번호 기능은 아직 구현되지 않았습니다.','info')
    return render_template('pass_reset.html')