from extensions import db
from datetime import datetime,timezone

class News(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    image_path = db.Column(db.String(255), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    author = db.relationship("User", backref=db.backref("news_list",lazy=True))

    def __repr__(self):
        return f'<News {self.title}>'

