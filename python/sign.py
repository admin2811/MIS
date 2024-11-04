import hashlib
import hmac

def sign(secret, api, parameters):
    # Sắp xếp các tham số theo thứ tự bảng chữ cái
    sort_dict = sorted(parameters)
    
    # Kết hợp endpoint API và các tham số thành một chuỗi duy nhất
    parameters_str = "%s%s" % (
        api,
        str().join('%s%s' % (key, parameters[key]) for key in sort_dict)
    )

    # Tạo chữ ký với thuật toán HMAC SHA256
    h = hmac.new(secret.encode("utf-8"), parameters_str.encode("utf-8"), digestmod=hashlib.sha256)
    
    # Trả về chữ ký đã mã hóa dạng chữ in hoa
    return h.hexdigest().upper()

# Thông tin để tạo chữ ký
app_secret = 'vUb59TVCQ5XVZKIWrwtEvLsWubTo1aZn'  # Thay thế bằng App Secret của bạn
api_path = '/products/get'  # Đường dẫn endpoint API bạn muốn truy cập
parameters = {
    'app_key': '130979',  # Thay thế bằng App Key của bạn
    'sign_method': 'sha256',
    'timestamp': '2024-10-26T00:00:00+0800',  # Đảm bảo timestamp có định dạng hợp lệ
    'access_token': '50000200536ViLeqMDQjJFnxOqgA1otGJxfRvkfceuBswVGH19f9ec2dfYJvnNYD',  # Thay thế bằng Access Token của bạn
    'filter': 'live',
    'limit': '10'
}

# Gọi hàm để tạo chữ ký
signature = sign(app_secret, api_path, parameters)
print("Signature:", signature)
