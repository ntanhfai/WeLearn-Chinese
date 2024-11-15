import requests
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

            # Đợi thẻ <table> với id "bothTable" xuất hiện trong tối đa 10 giây
            page.wait_for_selector("table#bothTable", timeout=10000)

            content = page.content()  # Lấy HTML sau khi trang đã tải và chạy JS
            browser.close()

            # Phân tích nội dung với BeautifulSoup
            soup = BeautifulSoup(content, "lxml")

            # Tìm thẻ <table> với class và id cụ thể
            table_content = soup.find(
                "table", {"class": "table cstm-table", "id": "bothTable"}
            )

            if table_content:
                # Trả về nội dung bảng hoặc xử lý thêm
                with open('text1.txt', 'w', encoding="utf-8") as f:
                    f.write(f'{table_content}')
                return table_content.text.strip()
            else:
                return "Không tìm thấy nội dung trong từ điển."

    except Exception as e:
        return f"Lỗi kết nối hoặc xử lý: {e}"


# Sử dụng hàm
result = translate_v3("电影")
print(result)

# import requests
# from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright

# def translate_v3(word):
#     try:
#         # Tạo URL với từ cần tra
#         thisUrl = f"https://dictionary.writtenchinese.com/#sk={word}&svt=pinyin"
#         with sync_playwright() as p:
#             browser = p.chromium.launch()
#             page = browser.new_page()
#             page.goto(thisUrl)
#             content = page.content()  # Lấy HTML sau khi trang đã tải và chạy JS
#             browser.close()

#             # Phân tích nội dung với BeautifulSoup
#             soup = BeautifulSoup(content, "lxml")

#             with open('text.txt', 'w', encoding="utf-8") as f:
#                 f.write(soup.prettify())
#             # Tìm thẻ <table> với class và id cụ thể
#             table_content = soup.find(
#                 "table", {"class": "table cstm-table", "id": "bothTable"}
#             )

#             if table_content:
#                 # Trả về nội dung bảng hoặc xử lý thêm
#                 with open('text1.txt', 'w', encoding="utf-8") as f:
#                     f.write(table_content)
#                 return table_content.text.strip()
#             else:
#                 return "Không tìm thấy nội dung trong từ điển."

#     except requests.exceptions.RequestException as e:
#         return f"Lỗi kết nối: {e}"


# # Sử dụng hàm
# result = translate_v3("电影")
# print(result)
