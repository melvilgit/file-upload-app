from database import db
from sqlalchemy.dialects.mysql import INTEGER

class File(db.Model):
    """Modal to Store a File metadata """
    __tablename__ = 'filemetadatas'
    name = db.Column(db.String(100), primary_key=True)
    md5 = db.Column(db.String(100))
    map = db.Column(db.String(100))

    def __init__(self, md5, name,map):
        self.name = name
        self.md5 = md5
        self.map = map
