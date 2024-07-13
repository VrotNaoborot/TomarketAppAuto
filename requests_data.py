import json, requests, random
from getuseragent import UserAgent


def generate_headers(access_token=None):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en,en-US;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://mini-app.tomarket.ai',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://mini-app.tomarket.ai/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Android WebView";v="126"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': 'Android',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'x-requested-with': 'org.telegram.messenger.web'
    }
    if access_token is not None:
        headers['authorization'] = access_token

    ua = UserAgent("android")
    useragent = random.choice(ua.list)
    headers['user-agent'] = useragent
    return headers


def login_api(query_data, proxy=None, access_token=None):
    """Выполняет вход/регистрацию, получает новый токен."""
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/login'
    try:
        data = json.dumps({
            "init_data": query_data,
            "invite_code": "",
            "is_bot": False
        })

        headers = generate_headers(access_token)

        if proxy is None:
            response = requests.post(url, headers=headers, data=data)
        else:
            response = requests.post(url, headers=headers, data=data, proxies=proxy)

        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError as j:
        print(f"Ошибка при декодировании JSON ответа: {j}")
        return None, -1
    except requests.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")
        return None, -1
    except requests.RequestException as req_err:
        print(f"Ошибка запроса: {req_err}")
        return None, -1
    except Exception as ex:
        print(f"Неизвестная ошибка: {ex}")
        return None, -1


# ежедневки
def daily_claim(access_token, proxy=None):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/daily/claim'
    headers = generate_headers(access_token)
    data = {"game_id": "fa873d13-d831-4d6f-8aee-9cff7a1d0db1"}

    try:
        if proxy is None:
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.post(url, headers=headers, json=data, proxies=proxy)
            response.raise_for_status()

        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"Не удалось декодировать ответ.")
        return None, -1
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None, -1


def user_balance(access_token, proxy=None):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/balance'
    headers = generate_headers(access_token)

    try:
        if proxy is None:
            response = requests.post(url, headers=headers)
        else:
            response = requests.post(url, headers=headers, proxies=proxy)
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON-формата")
        return None, -1
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None, -1


def start_farming(access_token, proxy=None):
    """Собираем помидорки раз в час"""
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/farm/start'
    headers = generate_headers(access_token)
    data = {"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"}

    try:
        if proxy is None:
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.post(url, headers=headers, json=data, proxies=proxy)
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON-формата")
        return None, -1
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None, -1


def claim_farming(access_token, proxy=None):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/farm/claim'
    headers = generate_headers(access_token)
    data = {"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"}
    try:
        if proxy is None:
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.post(url, headers=headers, json=data, proxies=proxy)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON-формата")
        return None, -1
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None, -1


def start_game(access_token, proxy=None):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/play'
    headers = generate_headers(access_token)
    data = {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d"}
    try:
        if proxy is None:
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.post(url, headers=headers, json=data, proxies=data)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON-формата")
        return None, -1
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None, -1


def claim_game(access_token, point, proxy=None):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/game/claim'
    headers = generate_headers(access_token)
    data = {"game_id": "59bcd12e-04e2-404c-a172-311a0084587d", "points": point}
    try:
        if proxy is None:
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.post(url, headers=headers, json=data, proxies=proxy)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON-формата")
        return None, -1
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None, -1


def invite_code(access_token, proxy=None):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/inviteCode'
    headers = generate_headers(access_token)
    try:
        if proxy is None:
            response = requests.post(url, headers=headers)
        else:
            response = requests.post(url, headers=headers, proxies=proxy)
        response.raise_for_status()
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON-формата")
        return None, -1
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None, -1


def farm_info(access_token, proxy=None):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/farm/info'
    headers = generate_headers(access_token)
    data = {"game_id": "53b22103-c7ff-413d-bc63-20f6fb806a07"}
    try:
        if proxy is None:
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.post(url, headers=headers, json=data, proxies=proxy)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON-формата")
        return None, -1
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None, -1


def tasks_list(access_token, proxy=None):
    url = 'https://api-web.tomarket.ai/tomarket-game/v1/tasks/list'
    headers = generate_headers(access_token)
    data = {"language_code": "ru"}
    try:
        if proxy is None:
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.post(url, headers=headers, json=data, proxies=proxy)
        response.raise_for_status()
        return response.json(), response.status_code
    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON-формата")
        return None, -1
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None, -1