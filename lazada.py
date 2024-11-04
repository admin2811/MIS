# Import các thư viện cần thiết
from lazop import LazopClient, LazopRequest

# Thông tin ứng dụng và API
url = 'https://api.lazada.vn/rest'  # Đây là URL API cho Lazada
appkey = '130979'  # Thay thế bằng App Key của bạn
appSecret = 'vUb59TVCQ5XVZKIWrwtEvLsWubTo1aZn'  # Thay thế bằng App Secret của bạn
access_token = '50000201101yh13031719bdZ0FTFJvZtQddDdy3OT1iFkRpwhv0HhYmQqpwo5MRq'  # Thay thế bằng Access Token của bạn

# Tạo đối tượng LazopClient
client = LazopClient(url, appkey, appSecret)

# Tạo yêu cầu API để lấy danh sách sản phẩm
request = LazopRequest('/products/get', 'GET')

# Thêm các tham số cho yêu cầu
request.add_api_param('filter', 'live')  # Lọc sản phẩm đang hoạt động
request.add_api_param('limit', '10')  # Giới hạn số sản phẩm trả về là 10

# Thực thi yêu cầu và lấy phản hồi
response = client.execute(request, access_token)

# Kiểm tra và in kết quả
print("Response Type:", response.type)  # Kiểu phản hồi (thành công hay lỗi)
print("Response Body:", response.body)  # Nội dung phản hồi chứa dữ liệu sản phẩm
