from extensions import db
from datetime import datetime,timezone

class ViewedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'),nullable=False)
    viewed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
