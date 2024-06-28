import requests
import threading
import os
import time
import platform


def test(type):
    filename = f"./outputproxy/{type}.txt"
    if not os.path.exists(filename):
        print(f"Warning: Proxy file '{filename}' not found. Skipping {type} proxy check.")
        return  # Early exit if file is missing

    with open(filename, "r") as f:
        data = f.read().split("\n")

    print('> {} {} proxies will be checked'.format(len(data), type))

    if os.path.exists(f"{type}_checked.txt"):
        try:
            if platform.system() == 'Windows':
                os.system('del ./outputproxy/{}_checked.txt'.format(type))
            else:  # Assuming it's Linux
                os.system('rm ./outputproxy/{}_checked.txt'.format(type))
        except:
            pass

    def process(i):
        try:
            requests.get("https://icanhazip.com/", proxies={type: f"{type}://{i}"}, timeout=20)
        except:
            pass
        else:
            with open(f"./outputproxy/{type}_checked.txt", "a+") as f:
                f.write(i + "\n")

    for i in data:
        threading.Thread(target=process, args=(i,)).start()

    while threading.active_count() > 1:
        time.sleep(1)


if __name__ == '__main__':
    test('socks4')
    test('socks5')
    test('http')
    # test('https')
