# WeLearn Chinese
Phần mềm tên là __WeLearn Chinese__ Chơi chữ từ WeChat và "learn" để gợi nhớ cách học qua tin nhắn, cũng có thể hiểu là chúng ta cùng học tiếng Trung.

# Giới thiệu

Dựng một trang web học tiếng Trung từ tin nhắn WeChat qua Flask tích hợp các tính năng sau:

### 1. **Tải lên và quản lý đoạn tin nhắn**
   - **Chức năng tải lên**: Người dùng có thể tải lên file/đoạn text chứa các đoạn tin nhắn (có thể là đoạn chat, file văn bản, JSON, v.v.).
   - **Phân tách tin nhắn**: Xử lý file để tách tin nhắn thành từng câu, đoạn, hoặc phiên thoại để tiện học.

### 2. **Hiển thị từ mới và cung cấp nghĩa**
   - **Phân tích từ mới**: Hệ thống có thể xác định các từ mà người dùng chưa biết, dựa trên danh sách từ vựng hoặc từ điển tùy chỉnh.
   - **Tra nghĩa và ví dụ**: Cung cấp nghĩa và ví dụ của từ đó để người học hiểu cách dùng.
   - **Hiển thị từ vựng và cách viết từ đó**: Hiển thị cách viết động, có hỗ trợ tự viết bằng tay (Tham khảo: https://toihoctiengtrung.com/hsk-2/2)

### 3. **Phát âm và luyện nghe**
   - **Phát âm từ hoặc câu**: Kết hợp API như Google Text-to-Speech hoặc Baidu để phát âm các từ hoặc câu tiếng Trung.
   - **Hướng dẫn phát âm**: Đưa ra cách đọc theo phiên âm Pinyin và có thể thêm chức năng điều chỉnh tốc độ để luyện nghe.

### 4. **Tính năng tra cứu ngữ pháp và ngữ cảnh**
   - **Giải thích cấu trúc câu**: Cung cấp giải thích về ngữ pháp trong từng câu (nếu có).
   - **Hiển thị ngữ cảnh sử dụng**: Đưa ra ví dụ về ngữ cảnh hoặc tình huống sử dụng các cụm từ để người học hiểu ngữ cảnh.

### 5. **Đánh dấu và theo dõi từ đã học**
   - **Đánh dấu từ vựng đã biết hoặc từ khó**: Cho phép người học đánh dấu từ họ đã học, từ đang gặp khó khăn hoặc tạo danh sách từ vựng yêu thích.
   - **Theo dõi tiến độ học từ**: Thống kê các từ đã học và từ cần ôn tập lại, tạo ra một bản đồ tiến độ học.

### 6. **Mini-quizzes hoặc bài tập ngắn**
   - Tạo các bài kiểm tra ngắn hoặc trò chơi từ vựng để người học ôn lại các từ đã học từ các đoạn tin nhắn.

### 7. (còn gì nữa nhỉ)

### Code Flask ban đầu có thể bao gồm:
   - **Form tải lên file** (HTML + Flask).
   - **API phát âm từ hoặc câu** (kết nối với dịch vụ Text-to-Speech).
   - **API lấy nghĩa và ví dụ** (kết nối từ điển, ví dụ là Pleco hoặc CC-CEDICT).
   - **Cơ sở dữ liệu từ vựng và tiến độ** (SQLite hoặc PostgreSQL) để lưu trữ dữ liệu học.

# Tài liệu tham khảo

- [Hoa ngữ tầm nhìn Việt](https://drive.google.com/drive/folders/1ek4UdptV19vpd57PSUko6basm8C95dDE)
- translator: https://drive.google.com/file/d/1WAHPg7PlOrnHNMbK_m_Q-ymbUhRn0CbH/view
- HSK https://toihoctiengtrung.com/hsk
- Cách viết chữ Hán: https://toihoctiengtrung.com/hsk-2/2



