<?php 
    session_start();
    require './vendor/autoload.php';
    use EcomPHP\TiktokShop\Client;

    $app_key = "6e7f2agu74oh6";
    $app_secret = 'a4a0da173ecaa41462d44ef695aa96d63304c25a';
    $client = new Client($app_key, $app_secret);
    $auth = $client->auth();
    
    // Kiểm tra nếu `code` tồn tại trong URL callback
    if (isset($_GET['code'])) {
        $authorization_code = $_GET['code'];

        // Lấy access token thông qua mã xác thực
        $token = $auth->getToken($authorization_code);

        // Lưu access token và refresh token vào biến hoặc cơ sở dữ liệu
        $access_token = $token['access_token'];
        $refresh_token = $token['refresh_token'];

        // Cấu hình access token cho client
        $client->setAccessToken($access_token);
        echo "Access Token: " . $access_token;
    } else {
        echo "Không tìm thấy mã xác thực!";
    }
    try {
        $authorizedShopList = $client->Authorization->getAuthorizedShop();
    
        // Kiểm tra và in thông tin các shop
        if (!empty($authorizedShopList)) {
            foreach ($authorizedShopList as $shop) {
                $shop_id = $shop['shop_id'] ?? 'Không có shop_id';
                $cipher = $shop['cipher'] ?? 'Không có cipher';
                echo "Shop ID: " . $shop_id . "<br>";
                echo "Cipher: " . $cipher . "<br><br>";
            }
        } else {
            echo "Danh sách cửa hàng được ủy quyền rỗng.";
        }
    } catch (Exception $e) {
        echo "Lỗi khi lấy danh sách cửa hàng: " . $e->getMessage();
    }
?>