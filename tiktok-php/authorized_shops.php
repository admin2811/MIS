<?php
require 'vendor/autoload.php';  // Nạp các thư viện đã cài đặt qua Composer
use EcomPHP\TiktokShop\Client;

$app_key = "6e7f2agu74oh6";
$app_secret = 'a4a0da173ecaa41462d44ef695aa96d63304c25a';

$client = new Client($app_key, $app_secret);

// Thiết lập access token cho client
$client->setAccessToken('ROW_2vewiAAAAAA2O5HWnTBgNbw3V2VcY_s-ffcvF5R0B_yIuGBqqRWJqramLcDVmfvorftDhA7ziDN-Hg06s7cTCrkYpmubRiSMo-VtYAJ-QayTwA3KQHzs0serQaYaVXOBq3POSwUTJIm4yuOQmuQb2S4ro9wiGu-M6tK2RpM1w88hEKjRtYWdOA'); // Thay thế 'your_access_token' với token đã lấy

// Lấy danh sách các cửa hàng được ủy quyền
$authorizedShopList = $client->Authorization->getAuthorizedShop();

// In danh sách các cửa hàng
foreach ($authorizedShopList as $shop) {
    echo "Shop ID: " . $shop['shop_id'] . "<br>";
    echo "Cipher: " . $shop['cipher'] . "<br><br>";
}
?>
