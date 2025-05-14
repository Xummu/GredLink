from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from sqlalchemy.orm import relationship

from extensions import db
from models.chat import ChatRelation,Message
from models.job import Job

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/list')
@login_required
def chat_list():
    relationship = ChatRelation.query.filter(
        (ChatRelation.user_id == current_user.id)|(ChatRelation.buser_id == current_user.id)
    ).all()

    chat_entries = []
    for relation in relationship:
        if current_user.id == relation.buser_id:
            partner = relation.user
        else:
            partner = relation.buser
        chat_entries.append({'chat':relation,'partner':partner})
    role =getattr(current_user,'role',None)
    return render_template("message.html",chat_list=chat_entries,role=role)

@chat_bp.route('/<int:chat_id>',methods=['GET','POST'])
@login_required
def chat_room(chat_id):
    chat = ChatRelation.query.get_or_404(chat_id)


    if current_user.id not in [chat.user_id, chat.buser_id]:
        flash('접근 권한이 없습니다.','danger')
        return redirect(url_for('chat.chat_list'))

    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            message = Message(
                chat_id=chat.id,
                sender_id=current_user.id,
            content=content)
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('chat.chat_room',chat_id=chat.id))

    messages = Message.query.filter_by(chat_id=chat.id).order_by(Message.timestamp.asc()).all()
    return render_template('chat.html',chat=chat,messages=messages)

@chat_bp.route('/start/<int:job_id>')
@login_required
def start_job(job_id):
    job = Job.query.get_or_404(job_id)

    existing = ChatRelation.query.filter_by(user_id=current_user.id, job_id=job_id).first()
    if existing:
        return redirect(url_for('chat.chat_room',chat_id=existing.id,job=job))

    new_chat = ChatRelation(
        user_id=current_user.id,
        buser_id=job.buser.id,
        job_id=job_id
    )
    db.session.add(new_chat)
    db.session.commit()
    return redirect(url_for('chat.chat_room',chat_id=new_chat.id,job=job))

