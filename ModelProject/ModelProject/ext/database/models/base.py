from pond5.ext.database import db
from flask import abort
from datetime import datetime

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(
        db.DateTime(),
        nullable=False,
        default=datetime.now,
        server_default=db.func.now())
    updated_at = db.Column(db.DateTime(),
        nullable=False,
        default=datetime.now,
        server_default=db.func.now(),
        server_onupdate=db.func.now())


    @classmethod
    def create(model, data):
        item = model(**data)
        try:
            
            db.session.add(item)
            db.session.commit()
            return item
        except Exception as e:
            db.session.rollback()


    @classmethod
    def delete_by_id(model, id):
        item = model.query.get(id) or abort(404, "item not found")
        try:
            db.session.delete(item)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()



    @classmethod
    def update_by_id(model, id, data):
        try:
            query = model.query.filter(model.id == id)
            if data:
                query.update(data)
                db.session.commit()
                item = query.first()            
                return item
        except Exception as e:
            db.session.rollback()



    @classmethod
    def get_by_id(model, id):
        data = model.query.get(id) or abort(404, "item not found")
        return data


    @classmethod
    def get_all(model):
        return model.query.all()

    @classmethod
    def get_list(model, args):
        args = dict(args)
        
        query = model.filters(args, model.query)
        data = query.all()
        return {
            "data": data,
            "meta": {}
        }, 200

    @classmethod
    def filters(model, args, query):

        filter_args = args.copy()

        if len(filter_args) < 1:
            return query

        filters = []
        for arg in args:
            attr = model.get_attr(arg)
            value = args[arg]
            filters.append(attr == value)

        return query.filter(*filters)

