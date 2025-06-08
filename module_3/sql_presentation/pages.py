from flask import Blueprint, render_template

bp = Blueprint("pages", __name__)

# Define routes for each page
@bp.route("/")
def home():
    return render_template("pages/home.html")