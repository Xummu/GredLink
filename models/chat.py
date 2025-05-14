from extensions import db
from datetime import datetime, timezone

class ChatRelation(db.Model):
    __tablename__ = 'chat_relation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    buser_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'),nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', foreign_keys=[user_id],backref='user_chats')
    buser = db.relationship('User', foreign_keys=[buser_id],backref='buser_chats')

    job = db.relationship('Job',backref='chat_relations')
    messages = db.relationship('Message', backref='chat', cascade='all, delete-orphan')


class Message(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat_relation.id'),nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    sender = db.relationship('User', foreign_keys=[sender_id])
