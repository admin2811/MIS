import lazop
import requests
import time

ERP_URL = "https://nhom5mishttt.erpnext.com/api/resource/Item"
API_KEY = "5e87caf557b51ab"
API_SECRET = "8e6da59e4193246"

# Thông tin cấu hình Lazada
url = "https://api.lazada.vn/rest"  # URL API Lazada
appkey = "130979"  # Thay bằng app key của bạn
appSecret = "vUb59TVCQ5XVZKIWrwtEvLsWubTo1aZn"  # Thay bằng app secret của bạn
access_token = "50000201013qqYtaaYFWEnpbT1629d3bepj8ejphMzzCmlShziy0EEakq3DJySVp"  # Thay bằng access token của bạn

# Function to get a list of products from ERPNext
def get_items():
    response = requests.get(ERP_URL, auth=(API_KEY, API_SECRET))
    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])[:10]
    else:
        print("Failed to retrieve items:", response.status_code)
        return []

# Function to get details of a specific product from ERPNext
def get_item_details(item_id):
    item_details_url = f"{ERP_URL}/{item_id}"
    response = requests.get(item_details_url, auth=(API_KEY, API_SECRET))
    if response.status_code == 200:
        item_details = response.json()
        return item_details.get("data", {})
    else:
        print(f"Failed to retrieve details for item {item_id}:", response.status_code)
        return {}

def upload_image_from_url(image_url):
    # Tải ảnh từ ERPNext URL
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content
        
        # Khởi tạo LazopClient và LazopRequest cho API của Lazada
        client = lazop.LazopClient(url, appkey, appSecret)
        request = lazop.LazopRequest('/image/upload')
        
        # Thêm ảnh dưới dạng dữ liệu nhị phân (binary)
        request.add_file_param('image', ('image.png', image_data))  # Đặt tên file cho ảnh
        
        # Thực thi yêu cầu tải lên ảnh
        response = client.execute(request, access_token)
        
        # Kiểm tra kết quả tải lên
        if 'data' in response.body and 'image' in response.body['data']:
            print("Image uploaded successfully:", response.body['data']['image']['url'])
            return response.body['data']['image']['url']
        else:
            print("Image upload failed:", response.body)
            return None
    else:
        print("Failed to download image from ERPNext:", response.status_code)
        return None

def check_items():
    items = get_items()
    
    for item in items:
        item_id = item.get("name")
        # Lấy thông tin chi tiết của sản phẩm
        item_details = get_item_details(item_id)
        # Chỉ lấy trường image
        image_url = item_details.get("image")
        print(f"Item ID: {item_id}")
        print("Image URL:", image_url)

        # Tải ảnh lên Lazada
        if image_url:
            uploaded_image_url = upload_image_from_url(image_url)
            if uploaded_image_url:
                print(f"Uploaded image URL for item {item_id}: {uploaded_image_url}")

if __name__ == "__main__":
    while True:
        check_items()
        time.sleep(10)
