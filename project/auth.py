from flask import Blueprint, render_template, request, flash, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user

client = MongoClient("mongodb://localhost:27017")
db = client["FLASK_APPLICATION"]
users_collection = db["users"]

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@auth.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not username or not email or not password:
        flash("Please provide the complete information")
        return redirect(url_for("auth.signup"))

    exists_user = users_collection.find_one({"username": username})

    if exists_user:
        flash("User already exists.")
        return redirect(url_for("auth.signup"))

    user_data = {
        "username": username,
        "email": email,
        "password": generate_password_hash(password, method="pbkdf2:sha256"),
    }

    users_collection.insert_one(user_data)
    return redirect(url_for("auth.login"))


@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Please provide the complete information")
        return redirect(url_for("auth.login"))

    user = User.objects(username=username).first()

    if not user:
        flash("User doesn't exist please signup first")
        return redirect(url_for("auth.login"))

    if not user or not check_password_hash(user.password, password):
        flash("Please provide correct credentials")
        return redirect(url_for("auth.login"))

    login_user(user, remember=False)
    return redirect(url_for("main.user_profile"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
