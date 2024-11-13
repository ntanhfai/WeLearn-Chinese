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
from googletrans import Translator
from pypinyin import pinyin, Style
import pinyin as transpinyin
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
