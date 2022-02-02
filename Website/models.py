from. import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.Integer, unique=True)

class Offices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String)
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.Integer, unique=True)
    address = db.Column(db.String, unique=True)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.Integer, unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    position = db.Column(db.String)
    office = db.Column(db.Integer, db.ForeignKey('offices.id'))
    

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.Integer, unique=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    custmerID = db.Column(db.Integer, db.ForeignKey('customer.id'))
    employeeID = db.Column(db.Integer, db.ForeignKey('employee.id'))
    device = db.Column(db.String)
    indate = db.Column(db.DateTime(timezone=True), default=func.now())
    exdate = db.Column(db.DateTime(timezone=True), default=func.now.timedelta(days=7))
    details = db.Column(db.String)
    status = db.Column(db.String)


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String(150), unique=True)
    phone = db.Column(db.Integer, unique=True)
    address = db.Column(db.String, unique=True)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    amount = db.Column(db.Integer)
    supplierId = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    stock = db.Column(db.Boolean)


class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemid = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    name = db.Column(db.String(150), unique=True)
    amount = db.Column(db.Integer)
    indate = db.Column(db.DateTime(timezone=True), default=func.now())
    supplierId = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    exdate = db.Column(db.DateTime(timezone=True), default=func.now.timedelta(days=30))