from extensions import db
from datetime import datetime,timezone

class FavoriteJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'),nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='favorite_jobs')
    job = db.relationship('Job', backref='favorite_jobs')