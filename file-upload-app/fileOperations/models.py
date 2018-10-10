from database import db


class File(db.Model):
    """Modal to Store a File metadata """
    __tablename__ = 'filemetadata'
    name = db.Column(db.String(100), primary_key=True)
    md5 = db.Column(db.String(100))

    def __init__(self, md5, name):
        self.name = name
        self.md5 = md5
