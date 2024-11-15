from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def translate_v3(word):
    try:
        # Tạo URL với từ cần tra
        thisUrl = f"https://dictionary.writtenchinese.com/#sk={word}&svt=pinyin"
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(thisUrl)

            # Đợi bảng "bothTable" tải
            page.wait_for_selector("table#bothTable", timeout=10000)
            content = page.content()  # Lấy HTML sau khi trang đã tải và chạy JS
            browser.close()

            # Phân tích nội dung với BeautifulSoup
            soup = BeautifulSoup(content, "lxml")
            table_content = soup.find(
                "table", {"class": "table cstm-table", "id": "bothTable"}
            )

            if table_content:
                # Tạo dictionary để lưu kết quả
                result = {}

                # Lấy "Simplified Chinese" từ <span data-sc="电"> và <span data-sc="影">
                simplified_chinese = "".join(
                    [
                        char.get("data-sc")
                        for char in table_content.select("td.symbol-wrap span[data-sc]")
                    ]
                )
                result["Simplified Chinese"] = simplified_chinese

                # Lấy "Pinyin" và liên kết âm thanh
                pinyin_text = "".join(
                    [
                        char.text
                        for char in table_content.select(
                            "td.with-icon.pinyin div.link-wrap a span.char"
                        )
                    ]
                )
                audio_url = table_content.select_one(
                    "td.with-icon.pinyin div.mandarin-inner span.icon-icon7"
                )["onclick"]
                audio_url = audio_url.split("'")[1]  # Trích xuất URL âm thanh
                result["Pinyin"] = f"{pinyin_text}, {audio_url}"

                # Lấy "English Definition for Chinese Text"
                english_definition = table_content.select_one(
                    "td.txt-cell"
                ).text.strip()
                result["English Definition for Chinese Text"] = english_definition

                # Lấy "Traditional Chinese" từ <span data-tc="電"> và <span data-tc="影">
                traditional_chinese = "".join(
                    [
                        char.get("data-tc")
                        for char in table_content.select("td.word span[data-tc]")
                    ]
                )
                result["Traditional Chinese"] = traditional_chinese

                return result
            else:
                return "Không tìm thấy nội dung trong từ điển."

    except Exception as e:
        return f"Lỗi kết nối hoặc xử lý: {e}"


# Sử dụng hàm
result = translate_v3("电影")
print(result)
