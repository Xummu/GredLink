import os

from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from models.carousel import Carousel
from models.user import User
from extensions import db
from models.news import News

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('관리자만 접근 가능합니다.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return decorated_view

@admin_bp.route('/news_edit', methods=['GET', 'POST'])
@login_required
@admin_required
def news_edit():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('제목과 내용을 모두 입력하세요','warning')
            return redirect(url_for('admin.news_edit'))
        news = News(title=title, content=content,author_id = current_user.id)
        db.session.add(news)
        db.session.commit()
        flash('뉴스가 등록되었습니다.', 'success')
        return redirect(url_for('admin.news_edit'))

    news_list = News.query.order_by(News.timestamp.desc()).all()
    return render_template('admin/news_edit.html', news_list=news_list)
@admin_bp.route('/news_delete/<int:new_id>', methods=['POST'])
@login_required
@admin_required
def news_delete(news_id):
    news = News.query.get_or_404(news_id)
    db.session.delete(news)
    db.session.commit()
    flash('뉴스가 삭제되었습니다','info')
    return redirect(url_for('admin.news_edit'))
@admin_bp.route('/news_edit/<int:news_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def news_update(news_id):
    news = News.query.get_or_404(news_id)

    if request.method == 'POST':
        news.title = request.form['title']
        news.content = request.form['content']

        image = request.files.get('image')
        if image and image.filename:
            filename = secure_filename(image.filename)

            upload_dir = os.path.join(current_app.static_folder, 'uploads/news')
            os.makedirs(upload_dir, exist_ok=True)

            path = os.path.join('uploads/news', filename)
            image.save(os.path.join(current_app.static_folder,path))
            news.image_path = path.replace('\\', '/')

        db.session.add(news)
        flash('뉴수가 수정되었습니다.', 'success')
        return redirect(url_for('admin.news_edit'))

    return render_template('admin/news_edit.html', news=news)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/admin.html')


@admin_bp.route('/user_edit')
@login_required
@admin_required
def user_edit():
    users = User.query.all()
    return render_template('admin/user_edit.html', users=users)

@admin_bp.route('/user_add', methods=['POST'])
@login_required
@admin_required
def user_add():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    real_name = request.form['real_name']
    phone = request.form['phone']
    password_hash = generate_password_hash(password,method='pbkdf2:sha256')
    email = request.form['email']
    new_user = User(username=username,password_hash=password_hash,role=role,real_name=real_name,phone=phone,email=email,avatar='img/icon.png')


    db.session.add(new_user)
    db.session.commit()
    flash('사용자가 성공적으로 추가되었습니다.', 'success')
    return redirect(url_for('admin.user_edit'))

@admin_bp.route('/user_delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    user.is_delete = True
    db.session.commit()
    flash('사용자가 삭제 처리되었습니다.', 'info')
    return redirect(url_for('admin.user_edit'))

@admin_bp.route('/admin/user/update', methods=['POST'])
@login_required
def user_update():
    if current_user.role != 'admin':
        abort(403)

    for user in User.query.all():
        username = request.form.get(f'username_{user.id}')
        role = request.form.get(f'role_{user.id}')
        if username and role:
            user.username = username
            user.role = role
    db.session.commit()
    flash('사용자 정보가 수정되었습니다.')
    return redirect(url_for('admin.user_edit'))

@admin_bp.route('/count')
@login_required
@admin_required
def count():
    user_count = User.query.filter_by(is_delete=False).count()

    visit_count = 123
    return render_template('admin/count.html', user_count=user_count, visit_count=visit_count)


@admin_bp.route('/home_edit',methods=['GET','POST'])
@login_required
@admin_required
def home_edit():
    if request.method == 'POST':
        file = request.files.get('image')
        caption = request.form.get('caption')
        link = request.form.get('link')

        if file:
            filename=file.filename

            relative_path =os.path.join('uploads/carousel',filename)
            relative_path = relative_path.replace("\\", "/")
            abs_path =os.path.join(current_app.root_path,'static',relative_path)

            os.makedirs(os.path.dirname(abs_path),exist_ok=True)
            file.save(abs_path)


            new_carousel = Carousel(image_path=relative_path,caption=caption,link=link)
            db.session.add(new_carousel)
            db.session.commit()
            flash('이미지가 추가되었습니다.', 'success')

        return redirect(url_for('admin.home_edit'))
    carousels = Carousel.query.all()
    return render_template('admin/home_edit.html', images=carousels)


@admin_bp.route('/home_delete/<int:carousel_id>', methods=['POST'])
@login_required
@admin_required
def carousel_delete(carousel_id):
    carousel = Carousel.query.get_or_404(carousel_id)

    full_path = os.path.join(current_app.root_path,'static',carousel.image_path)
    if os.path.exists(full_path):
        os.remove(full_path)

    db.session.delete(carousel)
    db.session.commit()
    flash('이미지가 삭제되었습니다.','info')
    return redirect(url_for('admin.home_edit'))
