import requests
import time

# Các thông tin cần thiết để kết nối API của ERPNext
ERP_URL = "https://nhom5mishttt1.erpnext.com/api/resource/Item"
API_KEY = "0eee8d643967486"
API_SECRET = "b68e75acb918e60"

# Hàm lấy danh sách sản phẩm từ ERPNext
def get_items():
    response = requests.get(ERP_URL, auth=(API_KEY, API_SECRET))
    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])
    else:
        print("Failed to retrieve items:", response.status_code)
        return []

# Hàm lấy thông tin tồn kho cho một sản phẩm
def get_item_quantity(item_code):
    # Lấy danh sách tồn kho
    items = get_items()
    
    for item in items:
        if item.get("item_code") == item_code:
            return item.get("qty", 0)  # Lấy số lượng tồn kho cho item_code

    return None

# Hàm kiểm tra thông tin tồn kho cho từng sản phẩm
def check_stock_quantity():
    items = get_items()
    
    for item in items:
        item_code = item.get("item_code")
        qty = get_item_quantity(item_code)
        print(f"Item Code: {item_code}, Quantity: {qty}")
        print("-----------------------------")

if __name__ == "__main__":
    while True:
        check_stock_quantity()
        time.sleep(10)  # Kiểm tra mỗi 10 giây
