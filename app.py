from genericpath import exists
import os
from flask import Flask, render_template
from flask_login import LoginManager
from config import Config

from models import db, User
from flask import Flask, redirect, url_for
from flask_login import current_user
from controllers import (
    upload_controller,
    analyze_controller,
    vocab_controller,
    tts_controller,
    auth_controller,
)
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
print("Xin chào !")
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
db_path = os.path.join('instance', 'learning_chinese.db')
createUsersList=[{'username':'ta','password':'123','email':'nt.anh.fai@gmail.com'},
                 {'username':'test1','password':'test','email':'test1@gmail.com'},
                 {'username':'test2','password':'test','email':'test2@gmail.com'},
                 {'username':'test3','password':'test','email':'test3@gmail.com'},
                 ]
# Tạo cơ sở dữ liệu nếu chưa tồn tại
with app.app_context():
    if not os.path.exists(db_path):
        db.create_all()
        # Tạo người dùng mới
        for mUser in createUsersList:

            user = User(username=mUser["username"], email=mUser["email"])
            user.set_password(mUser["password"])
            db.session.add(user)

        db.session.commit()
from flask_migrate import Migrate

migrate = Migrate(app, db)


# Cài đặt Flask-Login
# login_manager = LoginManager(app)
# login_manager.login_view = "auth.login"


# from flask_login import LoginManager, login_user
from models import User

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Đăng ký các blueprint
app.register_blueprint(upload_controller.bp)
app.register_blueprint(analyze_controller.bp)
app.register_blueprint(vocab_controller.bp)
app.register_blueprint(tts_controller.bp)
app.register_blueprint(auth_controller.bp)

@app.route("/")
def home():
    # Kiểm tra nếu người dùng đã đăng nhập, chuyển hướng đến trang chính
    if current_user.is_authenticated:
        return redirect(url_for("vocab.view_vocab"))
        # return render_template("toihoctiengtrung_com.html")
    # Nếu chưa đăng nhập, chuyển hướng đến trang đăng nhập
    return redirect(url_for("auth.login"))


if __name__ == "__main__":
    # Đường dẫn tới cơ sở dữ liệu
    app.run(debug=True, host="0.0.0.0", port=5566)
