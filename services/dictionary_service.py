# def get_word_meaning(word):
#     """
#     Hàm giả lập để tra nghĩa của từ. Thay bằng API từ điển thực tế nếu có.
#     """
#     # Giả lập nghĩa cho từ
#     meaning_dict = {
#         "项目": "project",
#         "解决方案": "solution",
#         "技术服务": "technical service",
#         "人力": "manpower",
#         # Thêm các từ khác vào từ điển giả lập hoặc gọi API tra nghĩa thực tế
#     }
#     return meaning_dict.get(word, "N/A")

from googletrans import Translator
# from googletrans import Translator
# from pypinyin import pinyin, Style
# import pinyin as transpinyin
from xpinyin import Pinyin
p = Pinyin()
def get_word_meaning(word, src="zh-cn", dest="vi", splitter='-'):
    """
    Hàm dịch từ sử dụng Google Translate.
    """
    # Khởi tạo translator
    translator = Translator()

    pinyin_text = ""
    meaning = ""
    # Lấy Pinyin
    try:
        # pinyin_result = pinyin(word, style=Style.FINALS)
        pinyin_text = p.get_pinyin(word, tone_marks="marks", splitter=splitter)
        # Ghép các âm tiết Pinyin lại thành chuỗi
        # pinyin_text = " ".join([syllable[0] for syllable in pinyin_result])

        # Dịch từ sang tiếng Anh (hoặc ngôn ngữ khác nếu cần)
        try:
            translation = translator.translate(word, src=src, dest=dest)
            meaning = translation.text
        except Exception as e:
            print("Lỗi khi dịch từ:", e)

    except Exception as e:
        print("Lỗi khi lấy Pinyin:", e)

    return pinyin_text.strip(), meaning
import requests
from bs4 import BeautifulSoup
import time


def translate_v3(word):
    try:
        url = f"https://vtudien.com/trung-viet/dictionary/nghia-cua-tu-{word}"
        # print(url)

        headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" }

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
                    Pinyin = str(table_content.find("td", id="C_C"))

                    # Lưu HTML vào file
                    with open("table.html", "w", encoding="utf-8") as f:
                        f.write(table_html)

                    return {
                        "status": "success",
                        "content": table_html,
                        "pinyin": Pinyin,
                        # "audio": f"https://vtudien.com/doc/trung/{word}.mp3",
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


def get_word_meaning_v2(word, src="zh-cn", dest="vi", splitter='-'):
    # Kiểm tra kết quả
    # print('New word:', word)
    result = translate_v3(word)
    if result["status"] == "success":
        # print("Nội dung từ điển:", result["content"])
        return result["pinyin"], result["content"]

    else:
        print("Lỗi:", result["message"])
        return get_word_meaning(word)
