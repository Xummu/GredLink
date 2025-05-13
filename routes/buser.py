
from flask import Blueprint,render_template,request,redirect,url_for,current_app,flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models.job import Job
from extensions import db

buser_bp =Blueprint('buser',__name__)


def buser_required(func):
    from functools import wraps
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'buser':
            flash('관리자만 접근 가능합니다.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return decorated_view

@buser_bp.route('/buser/dashboard')
@login_required
@buser_required
def dashboard():
    return render_template('buser/buser.html')

@buser_bp.route('/buser/job_post',methods=['GET','POST'])
@login_required
@buser_required
def job_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        location = request.form.get('location')
        salary = request.form.get('salary')
        image = request.files.get('image')

        if not title or not content:
            flash('제목과 설명을 필수입니다.', 'warning')
            return redirect(url_for('buser.job_post'))

        image_path = None
        if image and image.filename:
            filename =secure_filename(image.filename)
            upload_dir = os.path.join(current_app.static_folder,'uploads/jobs')
            os.makedirs(upload_dir,exist_ok=True)
            relative_path = os.path.join('uploads/jobs',filename)
            image.save(os.path.join(current_app.static_folder,relative_path))
            image_path = relative_path.replace('\\','/')

        job = Job(title=title,content=content,location=location,salary=salary,image_path=image_path,buser_id=current_user.id)
        db.session.add(job)
        db.session.commit()
        flash('채용공고가 등록되었습니다.', 'success')
        return redirect(url_for('buser.job_post'))

    job_list = Job.query.filter_by(buser_id=current_user.id).order_by(Job.created_at.desc()).all()
    return render_template('buser/job_post.html',job_list=job_list)

@buser_bp.route('/buser/job_delete/<int:job_id>',methods=['POST'])
@login_required
@buser_required
def job_delete(job_id):
    job=Job.query.get_or_404(job_id)
    if job.buser_id != current_user.id:
        flash('삭제 권한이 없습니다.', 'danger')
        return redirect(url_for('buser.job_post'))
    db.session.delete(job)
    db.session.commit()
    flash('체용공고가 삭제되었습니다.', 'info')
    return redirect(url_for('buser.job_post'))

@buser_bp.route('/buser/job_edit/<int:job_id>',methods=['GET','POST'])
@login_required
@buser_required
def job_edit(job_id):
    job=Job.query.get_or_404(job_id)
    if job.buser_id != current_user.id:
        flash('수정 권한이 없습니다.','danger')
        return redirect(url_for('buser.job_post'))

    if request.method == 'POST':
        job.title = request.form.get('title')
        job.content = request.form.get('content')
        job.location = request.form.get('location')
        job.salary = request.form.get('salary')

        image = request.files.get('image')
        if image and image.filename:
            filename =secure_filename(image.filename)
            upload_dir = os.path.join(current_app.static_folder,'uploads/jobs')
            os.makedirs(upload_dir,exist_ok=True)
            relative_path = os.path.join('uploads/jobs',filename)
            image.save(os.path.join(current_app.static_folder,relative_path))
            job.image_path = relative_path.replace('\\','/')

        db.session.commit()
        flash('채용공고가 수정되었습니다.', 'success')
        return redirect(url_for('buser.job_post'))

    return render_template('buser/job_edit.html',job=job)