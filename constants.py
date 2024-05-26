GOLD_PRICE_API_URL = "https://services.bullionstar.com/spot-chart/getChart?product=false&productId=0&productTo=false&productIdTo=0&fromIndex=XAU&toIndex={currency}&period={period}&width=600&height=300&timeZoneId=Asia%2FSaigon&weightUnit=tr_oz&{time_range}"
GOLD_PRICE_API_HEADERS = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en,vi-VN;q=0.9,vi;q=0.8,en-US;q=0.7",
    "origin": "https://www.bullionstar.com",
    "priority": "u=1, i",
    "referer": "https://www.bullionstar.com/",
    "requestid": "cbc2a1df-5acf-4b2b-81cd-fd64db4d1cde",
    "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
}
