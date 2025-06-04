# 🚨 Hệ Thống Cảnh Báo Khí Gas - ESP32 & Flask Server

![Logo](https://github.com/zzmzvn/BTL_TPTM-NNTM/blob/main/codePy/logo.png)

Dự án này giúp giám sát nồng độ khí gas trong môi trường bằng cảm biến kết nối với ESP32. Khi nồng độ vượt ngưỡng, ESP32 sẽ gửi dữ liệu đến một server Flask, nơi sẽ xử lý và gửi cảnh báo qua email có chèn logo của hệ thống.

---

## 📁 Cấu trúc dự án

```
├── Gas.ino                # Chương trình Arduino chạy trên ESP32
├── gas_alert_server.py    # Server Flask nhận dữ liệu và gửi email
├── logo.png               # Logo được nhúng trong email
└── README.md              # Tài liệu mô tả dự án
```

---

## 🔧 Phần cứng cần thiết

- ESP32 Dev Module
- Cảm biến khí gas MQ-5
- Relay 2 kênh
- Quạt 12V (tùy chọn để làm mát khi phát hiện khí)
- Nguồn 5V/12V tùy cấu hình

---

## ⚙️ Phần mềm sử dụng

- [Arduino IDE](https://www.arduino.cc/en/software) để nạp mã cho ESP32
- Python 3 + Flask để chạy server
- Thư viện Python:
  - `Flask`
  - `smtplib`, `email` (thư viện chuẩn Python)

---

## 🔌 Hướng dẫn cài đặt và chạy

### 1. ESP32

- Nạp file `Gas.ino` lên ESP32 bằng Arduino IDE
- Điều chỉnh SSID, PASSWORD Wi-Fi và địa chỉ IP server Flask trong code nếu cần

### 2. Server Flask

#### Cài đặt thư viện:
```bash
pip install flask
```

#### Chạy server:
```bash
python gas_alert_server.py
```

#### Cập nhật thông tin email trong file `gas_alert_server.py`:
```python
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"
```

📌 **Lưu ý:** Bạn cần tạo App Password trong Gmail nếu bật xác thực 2 bước.

---

## 📤 Gửi dữ liệu từ ESP32

ESP32 sẽ gửi HTTP POST request tới:

```
http://<IP_SERVER>:5000/alert
```

Với dữ liệu dạng JSON như sau:
```json
{
  "gas_value": 730
}
```

---

## ✉️ Email cảnh báo

Email cảnh báo sẽ bao gồm:
- Logo hệ thống (`logo.png`)
- Thời gian phát hiện khí gas
- Nồng độ đo được
- Ngưỡng an toàn
- Cảnh báo khẩn cấp bằng HTML

---

## 🛡️ Bảo mật

- Sử dụng App Password thay vì mật khẩu Gmail thật
- Không chia sẻ file có chứa thông tin tài khoản khi công khai dự án
- Có thể triển khai xác thực cho API hoặc giới hạn IP để bảo vệ server

---

## 📸 Hình ảnh minh hoạ

<img src="soDo.png" width="200"/>

---

## 👨‍💻 Tác giả

- Nguyễn Vũ Phúc  
- Email: nguyenvuphuc413@gmail.com  
- Trường Đại học Đại Nam – [daihocdainam.edu.vn](https://dainam.edu.vn)

---
