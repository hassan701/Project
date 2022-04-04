from lib2to3.pgen2.pgen import DFAState
from multiprocessing import Manager
from random import randrange
from turtle import position
from flask import Blueprint, jsonify, render_template, flash, request, session
from flask_login import login_required, current_user
from .models import Offices, Employee, Customer, Order,Supplier,Inventory,Shipment, User
from flask_sqlalchemy import *
from werkzeug.security import check_password_hash, generate_password_hash
import json
from datetime import datetime, timedelta

from. import db



views = Blueprint('views',__name__)



@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        c_name = request.form.get('c_name')
        c_email = request.form.get('c_email')
        device = request.form.get('device')
        details = request.form.get('details')
        indate = datetime.strptime((request.form.get('date').replace("T", "-").replace(":", "-")),'%Y-%m-%d-%H-%M')
        exdate = datetime.strptime((request.form.get('e_date').replace("T", "-").replace(":", "-")),'%Y-%m-%d-%H-%M')
        customer = Customer.query.filter_by(email=c_email).first()
        if not customer:
            name = c_name.split(' ')
            new_customer = Customer(email=c_email, first_name=name[0], last_name=name[1])
            db.session.add(new_customer)
            db.session.commit()
            customer =  Customer.query.filter_by(email=c_email).first()
        new_order = Order(custmerID=customer.id, employeeID=current_user.id, device=device,details=details,indate=indate,exdate=exdate)
        db.session.add(new_order)
        db.session.commit()


    fields= ['id','device','details']
    
    employ = check_employee()
    if employ:
        i = Employee.query.filter_by(email=current_user.email).first()
        o = db.session.query( Order, Customer, Employee)\
                    .join(Customer, Customer.id == Order.custmerID)\
                    .join(Employee, Employee.id == Order.employeeID)\
                    .filter( Order.employeeID==i.id)
    else:
        i = Customer.query.filter_by(email=current_user.email).first()
        o = db.session.query( Order, Customer, Employee)\
                    .join(Customer, Customer.id == Order.custmerID)\
                    .join(Employee, Employee.id == Order.employeeID)\
                    .filter( Order.custmerID==i.id)

    return render_template("home.html", user = current_user,Employee=employ, orders=o)

@views.route('/data', methods=['GET','POST'])
def data():
    employ = check_employee()
    if request.method == 'POST':
        i_name = request.form.get('i_name')
        amount = request.form.get('amount')
        supplier = request.form.get('SupplierID')
        stock = request.form.get('stock')
        i = Inventory.query.filter_by(name=i_name).first()
        if not i:
            new_item = Inventory(name=i_name, amount=amount, supplierId=supplier,stock=True if stock=='on' else False)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added to Inventory', category='sucess')
        else:
            flash('Item already in inventory', category='error')
    inventories = db.session.query(Inventory, Supplier)\
                    .join(Supplier, Supplier.id == Inventory.supplierId).all()
    Shipments = db.session.query(Shipment, Inventory, Supplier)\
                    .join(Supplier, Supplier.id == Shipment.supplierId)\
                    .join(Inventory, Inventory.id == Inventory.id).all()
    acess = acess_data()
    return render_template("data.html",user = current_user,access =acess,Employee=employ,inventory=inventories,shipment=Shipments)

@views.route('/employee', methods=['GET','POST'])
def employee():
    employ = check_employee()
    i = Employee.query.filter_by(email=current_user.email).first()
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        phone = request.form.get('phone')
        position = request.form.get('position')
        if not employ:
            new_employee = Employee(first_name=first_name, last_name=last_name, phone=phone,email=email, position=position, office=i.office)
            db.session.add(new_employee)
            db.session.commit()
            flash('Employee added to the data base', category='sucess')
        else:
            flash('Employee already in the data base', category='error')
    list = db.session.query(Employee, Offices)\
                    .join(Employee, Employee.office == Offices.id)\
                    .filter(Employee.office==i.office).all()
    acess = acess_employee()
    return render_template("employee.html",user = current_user,access =acess,Employee=employ, employees=list)

@views.route('/profile', methods=['GET','POST'])
def profile():
    employ = check_employee()
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        phone = request.form.get('phone')
        c_email = request.form.get('c_email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if check_password_hash(current_user.password, password1):
            c = Customer.query.filter_by(email=current_user.email).first()
            c.phone = phone
            c.email = c_email
            c.first_name = f_name
            c.last_name = l_name
            current_user.first_name = f_name
            current_user.last_name = l_name
            current_user.phone = phone
            current_user.email = c_email
            if(password2!=password1 and password2!=""):
                current_user.password = generate_password_hash(password2, method='sha256')
            db.session.commit()
            flash('Profile updated', category='sucess')
        else:
            flash('Wrong password', category='error')

    return render_template("profile.html",user = current_user, Employee=employ)

@views.route('/delete_order', methods=['POST'])
def delete_order():
    order = json.loads(request.data)
    orderID= order['orderid']
    order = Order.query.get(orderID)
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({})

@views.route('/delete_item', methods=['POST'])
def delete_item():
    item = json.loads(request.data)
    itemId= item['itemId']
    item = Inventory.query.get(itemId)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({})

@views.route('/delete_employee', methods=['POST'])
def delete_employee():
    employee = json.loads(request.data)
    employeeId= employee['employId']
    employee = Inventory.query.get(employeeId)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({})

def check_employee():
    Euser = Employee.query.filter_by(email=current_user.email).first()
    if Euser:
        return True
    else:
        return False

def acess_data():
    Euser = Employee.query.filter_by(email=current_user.email).first()
    if Euser.position=="Manager" or Euser.position=="Logistics":
        return True
    else:
        return False

def acess_employee():
    Euser = Employee.query.filter_by(email=current_user.email).first()
    if Euser.position=="Manager" or Euser.position=="HR":
        return True
    else:
        return False