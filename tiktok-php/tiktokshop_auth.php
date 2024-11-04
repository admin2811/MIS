<?php
    require './vendor/autoload.php';
    use EcomPHP\TiktokShop\Client;
    $app_key = "6e7f2agu74oh6";
    $app_secret = 'a4a0da173ecaa41462d44ef695aa96d63304c25a';

    $client = new Client($app_key, $app_secret);
    $auth = $client->auth();
    $_SESSION['state'] = $state = bin2hex(random_bytes(20)); // Tạo trạng thái bảo mật

    // Tạo URL xác thực để chuyển hướng người dùng
    $authUrl = $auth->createAuthRequest($state, true);

    // Chuyển hướng người dùng tới trang xác thực
    header('Location: ' . $authUrl);
    exit;
?>