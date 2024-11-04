import lazop

# client = lazop.LazopClient("https://api.lazada.com/rest", "130979", "vUb59TVCQ5XVZKIWrwtEvLsWubTo1aZn")
# request = lazop.LazopRequest("/category/tree/get", "GET")

client = lazop.LazopClient("https://api.lazada.com/rest", "130979", "vUb59TVCQ5XVZKIWrwtEvLsWubTo1aZn")
request = lazop.LazopRequest('/category/tree/get','GET')
request.add_api_param('language_code', 'en_US')
response = client.execute(request)
print(response.type)
print(response.body)