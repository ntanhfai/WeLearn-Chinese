import requests
from bs4 import BeautifulSoup
import time


def translate_v3(word):
    try:
        url = f"https://vtudien.com/trung-viet/dictionary/nghia-cua-tu-{word}"
        print(url)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=5)
        response.encoding = "utf-8"

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Kiểm tra div có id="idnghia" - div này luôn tồn tại
            nghia_div = soup.find("div", id="idnghia")

            if nghia_div:
                # Kiểm tra nội dung - nếu từ không tồn tại, thường có thông báo "Không tìm thấy..."
                if "Không tìm thấy" in nghia_div.text:
                    return {
                        "status": "not_found",
                        "message": "Từ không tồn tại trong từ điển",
                    }

                # Nếu tìm thấy từ, tìm table
                table_content = nghia_div.find("table", id="definition_T_cv_id")
                if table_content:
                    table_html = str(table_content)
                    table_html = table_html.replace( 'src="/images', 'src="https://vtudien.com/images' )
                    table_html = table_html.replace( '\xa0', '' )

                    # Lưu HTML vào file
                    with open("table.html", "w", encoding="utf-8") as f:
                        f.write(table_html)

                    return {
                        "status": "success",
                        "content": table_html,
                        "audio": f"https://vtudien.com/doc/trung/{word}.mp3",
                    }
                else:
                    return {
                        "status": "no_table",
                        "message": "Không tìm thấy bảng nghĩa của từ",
                    }
            else:
                return {"status": "error", "message": "Không thể tải nội dung từ điển"}
        else:
            return {"status": "error", "message": f"Lỗi HTTP: {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Lỗi kết nối: {e}"}

# Kiểm tra kết quả
result = translate_v3("电影")
if result["status"] == "success":
    print("Nội dung từ điển:", result["content"])
else:
    print("Lỗi:", result["message"])

# # Sử dụng hàm
# result = translate_v3("电影")
# print(result)

# # Test với từ không tồn tại
# result2 = translate_v3("abcxyz")
# print(result2)
