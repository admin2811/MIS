import requests
import lazop

# Bước 1: Định nghĩa URL và thông tin xác thực
url = 'https://api.lazada.sg/rest'  # URL cho môi trường sản xuất
app_key = '130979'                   # Thay bằng App Key của bạn
app_secret = 'vUb59TVCQ5XVZKIWrwtEvLsWubTo1aZn'  # Thay bằng App Secret của bạn
access_token = '50000201d25ujOaccsBLyvfnmOo1gqV9gXDvx1992c6a2iNt0porVX7xft5x4Fwy'  # Mã truy cập hợp lệ cho người dùng

# Tạo client và yêu cầu Lazada
client = lazop.LazopClient(url, app_key, app_secret)
order_request = lazop.LazopRequest('/orders/get', 'GET')

# Thiết lập các tham số truy vấn
order_request.add_api_param('created_after', '2024-11-04T00:00:00+08:00')
order_request.add_api_param('status', 'unpaid')
order_request.add_api_param('sort_direction', 'DESC')
order_request.add_api_param('sort_by', 'updated_at')
order_request.add_api_param('offset', '1')
order_request.add_api_param('limit', '10')

# Thực hiện yêu cầu và lấy dữ liệu đơn hàng từ Lazada
order_response = client.execute(order_request, access_token)

# URL của webhook
webhook_url = 'https://ducminh.app.n8n.cloud/webhook-test/6ed29d47-1ec5-4ea4-8775-4ee7292867d7'  # Thay bằng URL của webhook của bạn

# Kiểm tra dữ liệu phản hồi từ đơn hàng
if order_response.body['code'] == '0':  # Kiểm tra nếu không có lỗi trong phản hồi
    orders = order_response.body['data']['orders']  # Lấy danh sách đơn hàng
    
    for order in orders:
        order_id = order['order_number']  # Lấy order_id để truy vấn items

        # Thực hiện yêu cầu API để lấy thông tin item của từng đơn hàng
        item_request = lazop.LazopRequest('/order/items/get', 'GET')
        item_request.add_api_param('order_id', order_id)
        item_response = client.execute(item_request, access_token)

        # Kiểm tra và in ra phản hồi từ API lấy items
        if item_response.body['code'] == '0':  # Kiểm tra nếu không có lỗi trong phản hồi
            # Kiểm tra nếu 'data' là danh sách và có ít nhất một phần tử
            if isinstance(item_response.body['data'], list) and len(item_response.body['data']) > 0:
                order['items'] = item_response.body['data']  # Thêm thông tin items vào đơn hàng
            else:
                print(f"Unexpected data format for items in order {order_id}. Response: {item_response.body}")
                order['items'] = []  # Gán giá trị rỗng nếu không có dữ liệu items phù hợp
        else:
            print(f"Failed to fetch items for order {order_id}. Response:", item_response.body)
            order['items'] = []  # Gán giá trị rỗng nếu không lấy được items

    # Gửi toàn bộ dữ liệu đơn hàng kèm items đến webhook
    try:
        headers = {'Content-Type': 'application/json'}
        webhook_response = requests.post(webhook_url, json=order_response.body, headers=headers)

        if webhook_response.status_code == 200:
            print("Data sent to webhook successfully!")
        else:
            print(f"Failed to send data. Status code: {webhook_response.status_code}")
            print(f"Response: {webhook_response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

else:
    print("Failed to fetch orders. Response:", order_response.body)
