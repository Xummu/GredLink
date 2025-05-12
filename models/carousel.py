from extensions import db


class Carousel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255))
    link = db.Column(db.String(255))
    is_active = db.Column(db.Boolean,default=True)

    def __repr__(self):
        return f'<Carousel {self.id}:{self.caption}>'