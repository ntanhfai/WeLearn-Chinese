# import bs4 as bs
# import ntanh

# from ntanh.ParamsBase import tactParametters
# import requests

# APP_NAME = "WeLearn"
# print(bs.__version__)

# class Parameters(tactParametters):
#     def __init__(self, ModuleName="TACT"):
#         super().__init__(saveParam_onlyThis_APP_NAME=False)
#         self.AppName = APP_NAME
#         # self.Ready_to_run = False # Nếu bắt buộc phải config thì đặt cái này = False, khi nào user chỉnh sang True thì mới cho chạy
#         self.HD = {
#             "Mô tả": "Chương trình này nhằm dạy học từ mới tiếng Trung theo các đoạn hội thoại trong wechat mà mình tham gia vào nhóm",
#             "Supported1": "'https://hanzii.net/search/word/{word}?hl=vi', key: 'hanzii.net'",
#             "Supported2": "'https://hsk.academy/vi/characters/{word}', key: 'hsk.academy'",
#         }
#         self.translate_urls = [
#             "https://hanzii.net/search/word/{word}?hl=vi",
#             "https://hsk.academy/vi/characters/{word}",
#         ]
#         self.translate_urls_including_keycheck = "hsk.academy"
#         self.load_then_save_to_yaml(file_path=f"{APP_NAME}.yml", ModuleName=ModuleName)
#         # ===================================================================================================
#         self.in_var = 1

# mParams = Parameters(APP_NAME)
# # mDir = "."
# # mParams.fnFIS(mDir=mDir, exts=("*.jpg", "*.png"))
# # mParams.ta_print_log("hello")
# # mParams.get_Home_Dir()

# def getTranslator(word=''):
#     url='https://hanzii.net/search/word/{word}?hl=vi'
#     for  mUrl in mParams.translate_urls:
#         if mParams.translate_urls_including_keycheck in mUrl:
#             url = mUrl
#     thisUrl=url.format(word=word)
#     print(f'Translate URL: {thisUrl}') 
#     url_link = requests.get(thisUrl, timeout=5)
#     soup = bs.BeautifulSoup(url_link.text, "lxml")
#     if mParams.translate_urls_including_keycheck in ['hanzii.net']:
#         titles = soup.find_all(".simple-tradition-wrap")

#         # display content
#         for data in titles:
#             print(data.get_text())
#         pass 

# from playwright.sync_api import sync_playwright 
# def translate_v2(word):
#     url = "https://hanzii.net/search/word/{word}?hl=vi"
#     for mUrl in mParams.translate_urls:
#         if mParams.translate_urls_including_keycheck in mUrl:
#             url = mUrl
#     thisUrl = url.format(word=word)
#     thisUrl = "https://dictionary.writtenchinese.com/#sk=%E7%94%B5%E5%BD%B1&svt=pinyin"
#     print(f"Translate URL: {thisUrl}")
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()
#         page.goto(thisUrl)
#         content = page.content()  # Lấy HTML sau khi trang đã tải và chạy JS
#         browser.close()

#         # Phân tích nội dung với BeautifulSoup
#         soup = bs.BeautifulSoup(content, "html.parser")
#         with open('text.txt', 'w', encoding="utf-8") as f:
#             f.write(soup.prettify())
#         # print(soup.prettify())
#         # print(soup.find_all("h3", class_="subtitle is-5 is-inline"))
#         Div_content=soup.find_all("div", class_="content")
#         print("Nghia:=====================")
#         print(Div_content[0])
#         print("Vi du:=====================")
#         print(Div_content[3])
#         pass
# import requests
# from bs4 import BeautifulSoup


# def translate_v3(word):
#     try:
#         # Tạo URL với từ cần tra
#         url = f"https://dictionary.writtenchinese.com/#sk={word}&svt=pinyin"
#         response = requests.get(url, timeout=2)

#         # Kiểm tra phản hồi HTTP
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, "lxml")
#             # Tìm bảng chứa nội dung (kiểm tra lại id thực tế nếu cần)
#             table_content = soup.find("table", id="bothTable")

#             if table_content:
#                 # Trả về nội dung bảng hoặc xử lý thêm
#                 return table_content.text.strip()
#             else:
#                 return "Không tìm thấy nội dung trong từ điển."
#         else:
#             return f"Lỗi HTTP: {response.status_code}"
#     except requests.exceptions.RequestException as e:
#         return f"Lỗi kết nối: {e}"


# if __name__ == '__main__':
#     # Sử dụng hàm
#     result = translate_v2("电影")
#     print(result)
#     # translate_v3("电话")

# """
# #bothTable > tbody > tr > td.with-icon.pinyin.div-mandarin.mandarin-blk > div > span


# """
# "/html/body/div[2]/section/div/div[3]/div/div[4]/div/div[1]/table/tbody/tr/td[2]/div/span"
