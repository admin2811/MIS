const express = require('express');
const fetch = require('node-fetch');
const cookieParser = require('cookie-parser');
const cors = require('cors');

const app = express();
app.use(cookieParser());
app.use(cors());

// Khai báo CLIENT_KEY và CLIENT_SECRET
const CLIENT_KEY = '6e35vp6j6of8m'; // Client key của bạn
const CLIENT_SECRET = 'd429c4717f4f486ed025e25b58111065833649d8'; // Client secret của bạn
const REDIRECT_URI = 'http://localhost:5000/callback'; // Địa chỉ callback

// Bước 1: Chuyển hướng tới trang xác thực của TikTok
app.get('/oauth', (req, res) => {
    const csrfState = Math.random().toString(36).substring(2);
    res.cookie('csrfState', csrfState, { maxAge: 60000 });

    let url = 'https://www.tiktok.com/v2/auth/authorize/';
    url += `?client_key=${CLIENT_KEY}`;
    url += '&scope=user.info.basic';
    url += '&response_type=code';
    url += `&redirect_uri=${encodeURIComponent(REDIRECT_URI)}`;
    url += `&state=${csrfState}`;

    res.redirect(url);
});

// Bước 2: Xử lý callback
app.get('/callback', async (req, res) => {
    const { code, state } = req.query;

    // Kiểm tra CSRF
    const csrfState = req.cookies.csrfState;
    if (csrfState !== state) {
        return res.status(403).send('CSRF verification failed.');
    }

    try {
            console.log('Request URL:', 'https://auth.tiktok-shops.com/api/v2/token/get');
            console.log('Request Body:', `client_key=${CLIENT_KEY}&client_secret=${CLIENT_SECRET}&code=${code}&grant_type=authorization_code&redirect_uri=${encodeURIComponent(REDIRECT_URI)}`);

            const tokenResponse = await fetch('https://auth.tiktok-shops.com/api/v2/token/get', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `client_key=${CLIENT_KEY}&client_secret=${CLIENT_SECRET}&code=${code}&grant_type=authorization_code&redirect_uri=${encodeURIComponent(REDIRECT_URI)}`,
            });

            const responseBody = await tokenResponse.text(); // Đọc phản hồi dưới dạng văn bản
            console.log('Raw Response:', responseBody); // Ghi lại phản hồi thô


        const tokenData = JSON.parse(responseBody); // Chuyển đổi sang JSON

        // Kiểm tra xem mã thông báo có tồn tại không
        if (tokenData && tokenData.access_token) {
            console.log('Access Token:', tokenData.access_token);
            // Chuyển hướng hoặc thông báo cho người dùng
            res.send('Login successful! Token received.');
        } else {
            res.status(400).send('Failed to retrieve access token. Response: ' + responseBody);
        }
    } catch (error) {
        console.error('Error fetching token:', error);
        res.status(500).send('Error retrieving token: ' + error.message);
    }
});

// Bước 3: Chạy server
app.listen(process.env.PORT || 5000, () => {
    console.log('Server is running on port 5000');
});
