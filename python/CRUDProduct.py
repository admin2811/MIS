import requests
import time

# URL webhook
webhook_url = 'https://hook.eu2.make.com/1ebqcsfle45cmylql8n5nn5b0ngjwjpl'

# Thời gian chờ giữa các lần yêu cầu (tính bằng giây)
interval = 10  # 60 giây (1 phút)

while True:
    # Thực hiện yêu cầu GET
    response = requests.get(webhook_url)
    if response.status_code == 200:
        if response.headers.get('Content-Type') == 'application/json':
            try:
                # Phân tích phản hồi dưới dạng JSON
                data = response.json()
                print("Dữ liệu JSON lấy được từ webhook:")
                print(data)
            except ValueError:
                print("Không thể phân tích phản hồi dưới dạng JSON.")
        else:
            # Nếu phản hồi không phải JSON, kiểm tra nội dung
            if response.text.strip() != "Accepted":
                print("Phản hồi không phải JSON. Nội dung phản hồi là:")
                print(response.text)
    else:
        print(f"Lỗi khi lấy dữ liệu từ webhook: {response.status_code}")

    # Chờ trong khoảng thời gian đã thiết lập trước khi gửi yêu cầu tiếp theo
    time.sleep(interval)
