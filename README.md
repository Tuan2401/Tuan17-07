Mục tiêu:
Xây dựng một ứng dụng web có khả năng:
        
        Mã hóa file dữ liệu với thuật toán AES.
        
        Giải mã file dữ liệu đã mã hóa.
        
        Cho phép người dùng nhập khóa tùy ý (bất kỳ độ dài).
        
        Hỗ trợ tải file lên và tải file kết quả xuống.
        
        Cung cấp giao diện thân thiện, chuyên nghiệp bằng Bootstrap.

Các chức năng chính:
        Chức năng	                     Mô tả
        
        Upload file	                      Người dùng chọn file từ máy và tải lên trang web.
        
        Nhập khóa	                      Người dùng nhập chuỗi bất kỳ để làm khóa mã hóa/giải mã.
        
        Mã hóa file                           Dùng AES (EAX mode) để mã hóa nội dung file với khóa đã xử lý.
        
        Giải mã file	                      Dùng AES để giải mã file đã mã hóa trước đó.
        
        Tải kết quả	                      Sau khi xử lý, cung cấp liên kết tải file kết quả về.
 TỔNG KẾT
        Thành phần	                     Công nghệ sử dụng
        
        Backend	                              Python (Flask)
        
        Mã hóa	                              PyCryptodome (AES EAX)
        
        Hash key	                      hashlib (SHA-256)
        
        Giao diện	                      HTML + Bootstrap 5
        
        Tính năng	                      Upload, Mã hóa, Giải mã, Tải xuống
