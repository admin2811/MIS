import requests
import lazop
import datetime

# Bước 1: Định nghĩa URL và thông tin xác thực
url = 'https://api.lazada.sg/rest'  # URL cho môi trường sản xuất
app_key = '130979'                   # Thay bằng App Key của bạn
app_secret = 'vUb59TVCQ5XVZKIWrwtEvLsWubTo1aZn'  # Thay bằng App Secret của bạn
access_token = '50000201d25ujOaccsBLyvfnmOo1gqV9gXDvx1992c6a2iNt0porVX7xft5x4Fwy'  # Mã truy cập hợp lệ cho người dùng

# Tạo client và yêu cầu Lazada
client = lazop.LazopClient(url, app_key, app_secret)
request = lazop.LazopRequest('/orders/get', 'GET')

# Thiết lập các tham số truy vấn
request.add_api_param('created_after', '2024-11-04T00:00:00+08:00')
request.add_api_param('status', 'unpaid')
request.add_api_param('sort_direction', 'DESC')
request.add_api_param('sort_by', 'updated_at')
request.add_api_param('offset', '1')
request.add_api_param('limit', '10')

# Thực hiện yêu cầu và lấy dữ liệu từ Lazada
response = client.execute(request, access_token)

# URL của webhook
webhook_url = 'https://ducminh.app.n8n.cloud/webhook-test/6ed29d47-1ec5-4ea4-8775-4ee7292867d7'  # Thay bằng URL của webhook của bạn

# Gửi dữ liệu `response.body` đến webhook bằng POST
try:
    # Định dạng payload cho webhook
    payload = response.body
    headers = {'Content-Type': 'application/json'}  # Thiết lập header cho định dạng JSON

    # Thực hiện yêu cầu POST đến webhook
    webhook_response = requests.post(webhook_url, json=payload, headers=headers)

    # Kiểm tra phản hồi từ webhook
    if webhook_response.status_code == 200:
        print("Data sent to webhook successfully!")
    else:
        print(f"Failed to send data. Status code: {webhook_response.status_code}")
        print(f"Response: {webhook_response.text}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
