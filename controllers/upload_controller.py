from flask import Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_required
from services.text_processing import process_text_file

bp = Blueprint("upload", __name__, url_prefix="/upload")


@bp.route("/file", methods=["POST"])
@login_required
def upload_file():
    if "file" not in request.files:
        flash("No file part")
        return redirect(url_for("upload.upload_page"))

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("upload.upload_page"))

    # Lưu file tạm thời và xử lý
    file_path = f"/tmp/{file.filename}"
    file.save(file_path)

    # Gọi hàm process_text_file để xử lý file cho người dùng hiện tại
    results = process_text_file(file_path, current_user)

    flash("File processed successfully")
    return redirect(url_for("analyze.analyze"))
