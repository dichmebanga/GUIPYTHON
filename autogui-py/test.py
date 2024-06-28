import httpx
import concurrent.futures

# Danh sách proxy có thể là HTTP hoặc SOCKS
proxies_list = [
    'socks5://94.23.220.136:59732',
    'socks5://37.18.73.60:5566',
]

# Danh sách các URL để kiểm tra
urls_to_check = [
    'https://www.google.com',
    'https://api.github.com',
    'https://httpbin.org/get'
]

def check_proxy(proxy, url):
    if proxy.startswith('http://') or proxy.startswith('https://'):
        proxies = {
            'http://': proxy,
            'https://': proxy,
        }
    elif proxy.startswith('socks4://') or proxy.startswith('socks5://'):
        proxies = {
            'all://': proxy,
        }
    else:
        print('Định dạng proxy không hợp lệ')
        return False

    try:
        with httpx.Client(proxies=proxies, timeout=3) as client:  # Giảm timeout xuống 3 giây
            response = client.get(url)
            print(f'Response from {url}:', response)
            return response.status_code == 200
    except httpx.ProxyError as e:
        print(f'Lỗi proxy ({proxy}) với URL ({url}):', e)
    except httpx.TimeoutException as e:
        print(f'Lỗi thời gian chờ ({proxy}) với URL ({url}):', e)
    except Exception as e:
        print(f'Lỗi khác ({proxy}) với URL ({url}):', e)
    return False

def check_all_proxies():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_proxy = {
            executor.submit(check_proxy, proxy, url): (proxy, url)
            for proxy in proxies_list
            for url in urls_to_check
        }

        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy, url = future_to_proxy[future]
            try:
                result = future.result()
                if result:
                    print(f'Proxy {proxy} hoạt động tốt với URL {url}')
                else:
                    print(f'Proxy {proxy} không hoạt động với URL {url}')
            except Exception as e:
                print(f'Lỗi khi kiểm tra proxy {proxy} với URL {url}: {e}')

# Gọi hàm kiểm tra tất cả các proxy
check_all_proxies()
