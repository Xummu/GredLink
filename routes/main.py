import os
from datetime import timezone,datetime
from urllib import request
from extensions import db

from flask import Blueprint, redirect, url_for, render_template, current_app, flash,request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from models.carousel import Carousel
from models.favorite_job import FavoriteJob
from models.news import News
from models.job import Job
from models.viewed_job import ViewedJob
from models.chat import ChatRelation,Message

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/home')
def home():
    carousels = Carousel.query.all()
    news_list = News.query.order_by(News.created_at.desc()).all()
    if current_user.is_authenticated:
        return render_template('home.html', role=current_user.role, images=carousels, news_list=news_list)
    else:
        return render_template('home.html', images=carousels,news_list=news_list)


@main_bp.route('/home/new_detail/<int:news_id>')
def new_detail(news_id):
    news =News.query.get_or_404(news_id)
    return render_template('new_detail.html',news=news)

@main_bp.route('/user')
@login_required
def user_profile():
    return render_template('user.html',role=current_user.role)

@main_bp.route('/user/favorites')
@login_required
def user_favorites():
    favorites = FavoriteJob.query.filter_by(user_id=current_user.id).all()
    jobs = [fav.job for fav in favorites if fav.job is not None]
    return render_template('like.html',jobs=jobs)

@main_bp.route('/user/resume')
@login_required
def user_resume():
    return render_template('aicv.html')
@main_bp.route('/user/scan')
def user_scan():
    return render_template('sscan.html')

# @main_bp.route('/message')
# @login_required
# def message():
#     if current_user.is_authenticated:
#         return render_template('message.html', role=current_user.role)
#     else:
#         return render_template('message.html')

@main_bp.route('/search')
def search():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    if current_user.is_authenticated:
        return render_template('search.html',role=current_user.role,jobs=jobs)
    else:
        return render_template('search.html',jobs=jobs)

@main_bp.route('/search/search_detail/<int:job_id>')
def search_detail(job_id):

    job = Job.query.get_or_404(job_id)

    existing =ViewedJob.query.filter_by(user_id=current_user.id,job_id=job_id).first()
    if existing:
        existing.viewed_at = datetime.now(timezone.utc)
    else:
        db.session.add(ViewedJob(user_id=current_user.id,job_id=job_id))
    db.session.commit()


    return render_template('search_detail.html',job=job)

@main_bp.route('/profile_edit',methods=['GET','POST'])
@login_required
def profile_edit():
    if request.method == 'POST':
        current_user.real_name=request.form.get('real_name')
        current_user.email = request.form.get('email')

        avatar_file = request.files.get('avatar')
        if avatar_file and avatar_file.filename:
            filename = secure_filename(avatar_file.filename)
            path = os.path.join('uploads/avatars', filename)


            full_path = os.path.join(current_app.static_folder,path)

            os.makedirs(os.path.dirname(full_path),exist_ok=True)

            avatar_file.save(full_path)
            current_user.avatar = path.replace("\\", "/")

        db.session.commit()
        flash('정보가 수정되었습니다.', 'success')
        return redirect(url_for('main.profile_edit'))
    return render_template('profile_edit.html')

@main_bp.route('/recent_jobs')
@login_required
def recent_jobs():
    recent =(
        db.session.query(Job)
        .join(ViewedJob,Job.id==ViewedJob.job_id)
    .filter(ViewedJob.user_id == current_user.id)
    .order_by(ViewedJob.viewed_at.desc())
    .limit(10)
    .all()
    )
    return render_template('see_post.html',jobs=recent)

@main_bp.route('/recent_jobs/<int:job_id>/toggle',methods=['POST'])
@login_required
def toggle_favorite(job_id):
    favorite = FavoriteJob.query.filter_by(user_id=current_user.id,job_id=job_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash('즐겨찾기에서 제거되었습니다.','info')
    else:
        new_fav = FavoriteJob(user_id=current_user.id,job_id=job_id)
        db.session.add(new_fav)
        db.session.commit()
        flash('즐겨찾기에 추가되었습니다.','success')
    return redirect(request.referrer or url_for('main.search'))