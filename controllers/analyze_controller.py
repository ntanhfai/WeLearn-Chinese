from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from services.text_processing import analyze_text

bp = Blueprint("analyze", __name__, url_prefix="/analyze")


@bp.route("/")
@login_required
def analyze():
    text = """
    阿太为omniverse项目提供解决方案技术服务，占用着AI团队的人力。请在11月13日前进行Esign立案。
    如果没有及时立案，你就无法获得该专案对应的价值，即无法获得对应的绩效奖金。
    """
    # Gọi hàm phân tích và lưu từ mới cho người dùng hiện tại
    results = analyze_text(text, current_user)
    return render_template("analyze.html", results=results)
