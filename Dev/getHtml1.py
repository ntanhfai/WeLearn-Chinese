import requests
from lxml import html


def translate_v3(word):
    try:
        # Tạo URL với từ cần tra
        url = (
            f"https://vtudien.com/trung-viet/dictionary/nghia-cua-tu-{word}"
        )
        print(url)
        response = requests.get(url, timeout=2)

        # Kiểm tra phản hồi HTTP
        if response.status_code == 200:
            # Parse nội dung HTML bằng lxml
            tree = html.fromstring(response.content)

            # Tìm bảng bằng XPath (kiểm tra lại XPath cụ thể)
            table_content = tree.xpath('//table[@id="bothTable"]')

            if table_content:
                # Lấy nội dung văn bản trong bảng
                return table_content[0].text_content().strip()
            else:
                return "Không tìm thấy nội dung trong từ điển."
        else:
            return f"Lỗi HTTP: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Lỗi kết nối: {e}"


# Sử dụng hàm
result = translate_v3("电影")
print(result)
