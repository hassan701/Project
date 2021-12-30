from flask import Blueprint

auth = Blueprint('auth',__name__)

@auth.route("hello")
def home():
    return "<h1>TEST</h1>"