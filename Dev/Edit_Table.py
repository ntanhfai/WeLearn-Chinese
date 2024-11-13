# Thêm cột vào table:
import sqlite3

# Kết nối tới cơ sở dữ liệu SQLite
conn = sqlite3.connect(r"H:\Projects\Working_Chinese_Learning\instance\flask_app.db")
cursor = conn.cursor()

# Thêm cột 'pinyin_text' vào bảng 'vocab'
try:
    cursor.execute("ALTER TABLE vocab ADD COLUMN pinyin_text TEXT")
    # print("Đã thêm cột 'pinyin_text' vào bảng 'vocab'.")
except sqlite3.OperationalError:
    # print("Cột 'pinyin_text' đã tồn tại hoặc có lỗi khác xảy ra.")
    print('Error')

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()
