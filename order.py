import requests

# Cấu hình thông tin
ERP_URL = "https://nhom5mishttt1.erpnext.com/api/resource/Sales%20Order"
API_KEY = "0eee8d643967486"
API_SECRET = "a65782bb947905c"  # Thay bằng API secret từ ERPNext

# Đặt tiêu đề cho yêu cầu HTTP
headers = {
    "Authorization": f"token {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json"
}

# Tham số fields dưới dạng chuỗi JSON hợp lệ
fields = '["name", "customer", "transaction_date", "delivery_date", "grand_total", "status", "items"]'

# Thêm tham số fields vào params
params = {
    "fields": fields
}

# Gửi yêu cầu GET để lấy danh sách các Sales Order với nhiều thuộc tính hơn
response = requests.get(ERP_URL, headers=headers, params=params)

# Kiểm tra kết quả
if response.status_code == 200:
    sales_orders_list = response.json()
    print("Danh sách Sales Order:", sales_orders_list)
else:
    print("Lỗi khi lấy danh sách Sales Order:", response.status_code, response.json())
