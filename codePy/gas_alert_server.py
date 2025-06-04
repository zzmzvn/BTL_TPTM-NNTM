from flask import Flask, request, jsonify
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage  # Để nhúng hình ảnh

app = Flask(__name__)

# Thông tin Email
EMAIL_SENDER = "nvp24123@gmail.com"
EMAIL_PASSWORD = "eyyv sgfj mgfe uhar"
EMAIL_RECEIVER = "nguyenvuphuc413@gmail.com"

# Gửi Email HTML với logo
def send_html_email(gas_value):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    threshold = 500
    subject = "⚠️ CẢNH BÁO KHÍ GAS - Nồng độ vượt ngưỡng!"

    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 20px;
                background-color: #fff;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .header img {{
                width: 120px;
                border-radius: 10px;
            }}
            .header h2 {{
                color: red;
                margin-top: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}
            table, th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
            }}
            .warning {{
                color: #e67e22;
                font-weight: bold;
                margin-top: 20px;
            }}
            .footer {{
                font-size: 12px;
                color: gray;
                margin-top: 30px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="cid:logo_image" alt="Logo hệ thống" />
                <h2>⚠️ CẢNH BÁO KHÍ GAS</h2>
            </div>
            <p>Hệ thống phát hiện nồng độ khí gas vượt mức an toàn.</p>
            <table>
                <tr>
                    <th>Nồng độ đo được</th><td><strong>{gas_value}</strong></td>
                </tr>
                <tr>
                    <th>Ngưỡng an toàn</th><td>{threshold}</td>
                </tr>
                <tr>
                    <th>Thời gian</th><td>{now}</td>
                </tr>
            </table>
            <p class="warning">⚠️ Vui lòng kiểm tra khu vực ngay lập tức!</p>
            <div class="footer">
                Hệ thống Cảnh báo khí gas – ESP32<br>
                Email kỹ thuật: support@yourdomain.com
            </div>
        </div>
    </body>
    </html>
    """

    # Tạo email
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    msg_alternative = MIMEMultipart("alternative")
    msg.attach(msg_alternative)

    msg_alternative.attach(MIMEText("Cảnh báo khí gas", "plain"))
    msg_alternative.attach(MIMEText(html_content, "html"))

    # Đính kèm logo
    with open("logo.png", "rb") as img_file:
        logo = MIMEImage(img_file.read())
        logo.add_header("Content-ID", "<logo_image>")
        logo.add_header("Content-Disposition", "inline", filename="logo.png")
        msg.attach(logo)

    # Gửi email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

# Route nhận POST từ ESP32
@app.route("/alert", methods=["POST"])
def alert():
    data = request.get_json()
    gas_value = data.get("gas_value")
    if gas_value:
        send_html_email(gas_value)
        return jsonify({"message": "Email sent"}), 200
    return jsonify({"error": "Missing gas value"}), 400

# Chạy server Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
