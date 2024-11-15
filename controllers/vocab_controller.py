from flask import Blueprint, redirect, render_template, url_for
from models import ExampleLink, Vocab, db, Example
from random import sample
from flask import Blueprint, redirect, url_for
from flask_login import login_required, current_user

bp = Blueprint("vocab", __name__, url_prefix="/vocab")


# controllers/vocab_controller.py
from flask import Blueprint, render_template, request
from services.text_processing import analyze_text  # Giả sử bạn có một hàm xử lý văn bản


# @bp.route("/vocab", methods=["GET", "POST"])
# def view_vocab():
#     if request.method == "POST":
#         text_input = request.form.get("text_input")
#         if text_input:
#             # Xử lý văn bản đã nhập
#             processed_text = analyze_text( text_input )  # Hàm này có thể là từ services.text_processing
#     vocab_list = Vocab.query.all()
#     return render_template("vocab.html", vocab_list=vocab_list)
@bp.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))


@bp.route("/learned", methods=["GET", "POST"])
@login_required
def view_vocab_learned():
    # Truy xuất danh sách từ vựng và các ví dụ liên quan
    vocab_list = (
        Vocab.query.filter_by(user_id=current_user.id)
        .filter(Vocab.difficulty < 0)
        .options(db.joinedload(Vocab.example_links).joinedload(ExampleLink.example))
        .all()
    )
    # Chọn ngẫu nhiên 3 ví dụ nếu có hơn 3 ví dụ
    for vocab in vocab_list:
        if len(vocab.example_links) > 3:
            vocab.example_links = sample(vocab.example_links, 3)

    return render_template("vocab_mobile.html", vocab_list=vocab_list, PageTitle='Vocabulary learned')


@bp.route("/", methods=["GET", "POST"])
@login_required
def view_vocab():     
    if request.method == "POST":
        text_input = request.json.get("text_input")
        if text_input:
            print("Xử lý: " + text_input)
            # Xử lý văn bản đã nhập và thêm từ vựng cùng ví dụ
            analyze_text(text_input, current_user)

    # Truy xuất danh sách từ vựng và các ví dụ liên quan
    vocab_list = (
        Vocab.query.filter_by(user_id=current_user.id).filter(Vocab.difficulty >= 0)
        .options(db.joinedload(Vocab.example_links).joinedload(ExampleLink.example))
        .all()
    )
    # Chọn ngẫu nhiên 3 ví dụ nếu có hơn 3 ví dụ
    for vocab in vocab_list:
        if len(vocab.example_links) > 3:
            vocab.example_links = sample(vocab.example_links, 3)

    return render_template("vocab_mobile.html", vocab_list=vocab_list, PageTitle="Vocabulary")


@bp.route("/update_difficulty", methods=["POST"])
def update_difficulty():
    if request.method == "POST":
        vocab_id = request.args.get("vocab_id")
        new_difficulty = request.form.get("difficulty")
        vocab = Vocab.query.get(vocab_id)

        if vocab:
            if new_difficulty == "-2":
                # Xóa các ExampleLink liên quan trước khi xóa Example
                for example_link in vocab.example_links:
                    db.session.delete(example_link)

                db.session.commit()  # Thực hiện commit trước khi xóa Example

                # Xóa các Example
                for example_link in vocab.example_links:
                    db.session.delete(example_link.example)

                db.session.delete(vocab)  # Cuối cùng, xóa từ vựng
                db.session.commit()
                return redirect(url_for("vocab.view_vocab"))
            else:
                vocab.difficulty = int(new_difficulty)
                db.session.commit()
    return redirect(url_for("vocab.view_vocab"))


# Bạn có thể thêm một route xử lý văn bản nữa nếu cần thiết
@bp.route("/process_text", methods=["POST"])
def process_text_input():
    text_input = request.json.get("text_input")
    if text_input:
        print("Xử lý: " + text_input)
        new_words, NwordAdded = analyze_text(text_input, current_user)
        return {"Numbers of words": NwordAdded, "Words": new_words}

