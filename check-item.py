import requests
import time

# Các thông tin cần thiết để kết nối API của ERPNext
ERP_URL = "https://nhom5mishttt1.erpnext.com/api/resource/Item"
API_KEY = "be7e8cde34b9838"
API_SECRET = "a5b0cda96eb5f61"
# Webhook URL của Make
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/hbfxle1fqesvwdycyklkeeommf3u19ej"  # Thay bằng Webhook URL thực tế

# Hàm lấy danh sách sản phẩm từ ERPNext
def get_items():
    response = requests.get(ERP_URL, auth=(API_KEY, API_SECRET))
    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])[:10]
    else:
        print("Failed to retrieve items:", response.status_code)
        return []

# Hàm lấy thông tin chi tiết của một sản phẩm cụ thể
def get_item_details(item_id):
    item_details_url = f"{ERP_URL}/{item_id}"
    response = requests.get(item_details_url, auth=(API_KEY, API_SECRET))
    if response.status_code == 200:
        item_details = response.json()
        return item_details.get("data", {})
    else:
        print(f"Failed to retrieve details for item {item_id}:", response.status_code)
        return {}

# Hàm gửi dữ liệu từng sản phẩm một tới webhook của Make
def send_to_make(item_details):
    try:
        response = requests.post(MAKE_WEBHOOK_URL, json=item_details)
        if response.status_code == 200:
            print("Data sent successfully to Make Webhook")
        else:
            print(f"Failed to send data to Make Webhook: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to Make Webhook: {str(e)}")

# Hàm kiểm tra các sản phẩm và gửi thông tin chi tiết từng sản phẩm tới webhook của Make
def check_items():
    items = get_items()
    
    for item in items:
        item_id = item.get("name")
        # Lấy thông tin chi tiết của sản phẩm
        item_details = get_item_details(item_id)
        print(f"Item ID: {item_id}")
        print("Item Details:", item_details)
        
        # Gửi thông tin chi tiết từng sản phẩm tới webhook của Make
        send_to_make(item_details)
        print("-----------------------------")

if __name__ == "__main__":
    while True:
        check_items()
        time.sleep(10)  # Kiểm tra mỗi 60 giây
