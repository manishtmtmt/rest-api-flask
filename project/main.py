from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
@login_required
def user_profile():
    username = current_user.username
    email = current_user.email
    return render_template("user_profile.html", username=username, email=email)
