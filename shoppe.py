import hmac
import hashlib

def generate_sign(secret_key, params):
    # Sắp xếp tham số theo thứ tự
    sorted_params = sorted(params.items())
    # Tạo chuỗi tham số để ký
    base_string = '&'.join(f"{key}={value}" for key, value in sorted_params)
    # Tính chữ ký
    sign = hmac.new(secret_key.encode(), base_string.encode(), hashlib.sha256).hexdigest()
    return sign

# Định nghĩa secret_key và các tham số
secret_key = "YOUR_SECRET_KEY"  # Thay thế bằng secret key của bạn
params = {
    "partner_id": 1,
    "shop_id": 126190,  
    "timestamp": 1729675336,  # Thay thế bằng timestamp hiện tại
    "access_token": "c09222e3fc40ffb25fc947f738b1abf1",
    "language": "zh-hans"
}

# Gọi hàm và in chữ ký
signature = generate_sign(secret_key, params)
print("Chữ ký:", signature)
