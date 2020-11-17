import json
from datetime import datetime
from flask import Response
from sqlalchemy.exc import SQLAlchemyError
from .config import Connection

conn = Connection()
app = conn.app
db = conn.db
manager = conn.manager

# This File handles all models from application. That's the database definition,
# all changes here reflect to your real database, so make sure everything it's

class Client(db.Model):
    
    __tablename__ = "Client"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=False, unique=False, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), index=False, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, index=False, unique=False, nullable=True,
                           default=datetime.now)
    updated_at = db.Column(db.DateTime, index=False, unique=False, nullable=True,
                           default=datetime.now)    
     
class Product(db.Model):
    __tablename__ = "Product"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), index=False, unique=True, nullable=False)
    price = db.Column(db.Numeric(10, 2), index=True, unique=True, nullable=False)
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, index=False, unique=False, nullable=True,
                            default=datetime.now)
    updated_at = db.Column(db.DateTime, index=False, unique=False, nullable=True,
                            default=datetime.now)


class Order(db.Model):
    __tablename__ = "Order"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'))
    order_quantity = db.Column(db.Integer)
    order_value = db.Column(db.Numeric(10, 2), index=False, unique=False, 
                            nullable=False)
    created_at = db.Column(db.DateTime, index=False, unique=False, nullable=True,
                            default=datetime.now)
    updated_at = db.Column(db.DateTime, index=False, unique=False, nullable=True,
                            default=datetime.now)


if __name__ == '__main__':
    manager.run()
