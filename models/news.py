from extensions import db
from datetime import datetime

class News(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    author = db.relationship("User", backref=db.backref("news_list",lazy=True))

    def __repr__(self):
        return f'<News {self.title}>'

