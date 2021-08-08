from NewOne.ext.database import db
from NewOne.ext.database.models.user import User


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Cleans database"""
    db.drop_all()


def populate_db():
    """Populate db with sample data"""
    data = [
        User(username="Joao Silva", email="joao.silva@gmail.com"),
        User(username="Ana Maria", email="ana.maria@gmail.com"),
    ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return User.query.all()
