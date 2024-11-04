import requests

# Thông tin xác thực
username = 'user'  # Thay bằng tên đăng nhập của bạn
password = 'Ducminhxp.tp2811'  # Thay bằng mật khẩu ứng dụng của bạn

# URL API để lấy danh sách sản phẩm
url = "https://63httt1nhom5mis.id.vn/wp-json/wp/v2/product"

# Gửi yêu cầu GET với xác thực Basic Auth
response = requests.get(url, auth=(username, password))

# Kiểm tra xem yêu cầu có thành công hay không
if response.status_code == 200:
    products = response.json()  # Lấy dữ liệu JSON từ phản hồi
    for product in products:
        print(product)  # In ra từng sản phẩm
else:
    print(f"Yêu cầu thất bại với mã lỗi: {response.status_code}")
