from flask import json
import lazop
import requests
import time
import random
from PIL import Image
import io

# Constants for ERPNext API
ERP_URL = "https://nhom5mishttt1.erpnext.com/api/resource/Item"
API_KEY = "be7e8cde34b9838"
API_SECRET = "a5b0cda96eb5f61"  

# Constants for Lazada API
LAZADA_URL = "https://api.lazada.sg/rest"  # Replace with the actual Lazada API URL
LAZADA_APP_KEY = "130979"  # Lazada app key
LAZADA_APP_SECRET = "vUb59TVCQ5XVZKIWrwtEvLsWubTo1aZn"  # Lazada app secret
LAZADA_ACCESS_TOKEN = "50000201d25ujOaccsBLyvfnmOo1gqV9gXDvx1992c6a2iNt0porVX7xft5x4Fwy"  # Lazada access token

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

# Function to upload image from URL to Lazada with resizing
def upload_image_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_data = response.content
        
        # Open the image using Pillow
        image = Image.open(io.BytesIO(image_data))
        
        # Resize the image to 330x330 pixels
        image = image.resize((330, 330), Image.LANCZOS)

        # Save the resized image to a byte stream
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)

        client = lazop.LazopClient(LAZADA_URL, LAZADA_APP_KEY, LAZADA_APP_SECRET)
        request = lazop.LazopRequest('/image/upload')
        request.add_file_param('image', ('image.png', image_bytes))  # Set the image file name
        # Execute the image upload request
        response = client.execute(request, LAZADA_ACCESS_TOKEN)

        # Check the upload response
        if 'data' in response.body and 'image' in response.body['data']:
            print("Image uploaded successfully:", response.body['data']['image']['url'])
            return response.body['data']['image']['url']
        else:
            print("Image upload failed:", response.body)
            return None
    else:
        print("Failed to download image from ERPNext:", response.status_code)
        return None

# Function to send product data to Lazada
def send_to_lazada(item):
    client = lazop.LazopClient(LAZADA_URL, LAZADA_APP_KEY, LAZADA_APP_SECRET)
    request = lazop.LazopRequest('/product/create')

    # Upload image and get the uploaded image URL
    uploaded_image_url = upload_image_from_url(item.get("image"))
    base_price = item.get("valuation_rate", 10.0)
    adjusted_price = base_price * 10 
    # Lazada payload mapped from ERPNext item fields
    print(adjusted_price)
    payload = {
        "Request": {
            "Product": {
                "PrimaryCategory": "10002065",  # Adjust with the correct category ID
                "Images": {"Image": [uploaded_image_url] if uploaded_image_url else []},
                "Attributes": {
                    "name": item.get("item_name", "No Name"),
                    "description": item.get("description", "No Description"),
                    "brand": "No Brand",
                    "model": "No Model",
                    "waterproof": "Waterproof",
                    "warranty_type": "No Warranty",
                    "warranty": "1 Month",  # Ensure this is a valid value
                    "short_description": item.get("description", "No Short Description"),
                    "Hazmat": "None",
                    "material": "Leather", 
                    "laptop_size": "11 - 12 inches", # Ensure this is a valid value
                    "delivery_option_sof": "No",
                    "name_engravement": "Yes", 
                    "gift_wrapping": "Yes",
                    "preorder_enable": "Yes",
                    "preorder_days": "0",
                },
                "Skus": {
                    "Sku": [{
                        "SellerSku": item.get("item_code", "test2023 03"),
                        "quantity": random.randint(20, 99),
                        "price": adjusted_price,
                        "special_from_date": "2022-06-20 17:18:31", 					
                        "special_to_date": "2025-03-15 17:18:31", 
                        "package_height": "10",  # Default value; update if available in ERPNext
                        "package_length": "10",  # Default value; update if available in ERPNext
                        "package_width": "10",   # Default value; update if available in ERPNext
                        "package_weight": random.randint(1, 200),
                        "package_content": item.get("description", "Product content"),
                        "Images": {"Image": [uploaded_image_url] if uploaded_image_url else []}
                    }]
                }
            }
        }
    }

    request.add_api_param('payload', json.dumps(payload))
    response = client.execute(request, LAZADA_ACCESS_TOKEN)
    print("Response Type:", response.type)
    print("Response Body:", response.body)

# Function to check and send product data
def check_items():
    items = get_items()
    
    for item in items:
        item_id = item.get("name")
        # Retrieve detailed information of each product
        item_details = get_item_details(item_id)
        if item_details:
            send_to_lazada(item_details)
            print(f"Product {item_id} sent to Lazada.")
        else:
            print(f"Failed to send product {item_id}.")

if __name__ == "__main__":
    while True:
        check_items()
        time.sleep(10)
