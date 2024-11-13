@REM pip install Flask-Migrate
@REM from flask_migrate import Migrate
@REM migrate = Migrate(app, db)

@REM  # Chỉ chạy lần đầu tiên nếu bạn chưa khởi tạo migrations
@REM flask db init     
@REM flask db migrate -m "Add pinyin_text column to vocab table"
@REM flask db upgrade


@REM Cách 2: Xóa và tạo lại cơ sở dữ liệu (chỉ nên dùng nếu chưa có dữ liệu quan trọng)
@REM Nếu bạn không cần giữ dữ liệu hiện có, bạn có thể xóa và tạo lại cơ sở dữ liệu:

@REM Xóa file cơ sở dữ liệu SQLite hiện tại.

@REM Mở Python shell và chạy lại các lệnh để tạo cơ sở dữ liệu và bảng mới:

@REM python
@REM Copy code
@REM flask shell
@REM from app import db
@REM db.create_all()
@REM exit()