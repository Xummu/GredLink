from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/home')
def home():
    return render_template('home.html')

@main_bp.route('/user')
@login_required
def user_profile():
    return render_template('user.html')

@main_bp.route('/user/seen')
@login_required
def user_seen():
    return render_template('see_post.html')

@main_bp.route('/user/favorites')
@login_required
def user_favorites():
    return render_template('like.html')

@main_bp.route('/user/resume')
@login_required
def user_resume():
    return render_template('aicv.html')
@main_bp.route('/user/scan')
def user_scan():
    return render_template('sscan.html')

@main_bp.route('/message')
@login_required
def message():
    return render_template('message.html')

@main_bp.route('/search')
def search():
    return render_template('search.html')

