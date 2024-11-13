from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

# controllers/auth_controller.py


bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Tạo người dùng mới
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for("auth.login"))
    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Tìm người dùng trong cơ sở dữ liệu
        user = User.query.filter_by(username=username).first()

        # Nếu người dùng không tồn tại, trả về thông báo lỗi
        if user is None:
            print(f"User: {username}, Pass:{password}, Hash Pass:User not found")
            flash("Invalid username or password.")
            return render_template("login.html")

        # Kiểm tra mật khẩu nếu người dùng tồn tại
        # print(
        #     f"User: {username}, Pass:{password}, Hash Pass:\n{generate_password_hash(password)}"
        # )

        if user.check_password(password):
            login_user(user)
            return redirect(url_for("vocab.view_vocab"))

        flash("Invalid username or password.")

    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
