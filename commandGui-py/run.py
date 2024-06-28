import os
import sys
import random
import requests
import subprocess
from scripts import characters


data = []
random_number = random.randint(27, 35)


def run_script(script_path):
    python_cmd = sys.executable
    subprocess.run([python_cmd, script_path])


def download_and_handle(url, selected_item_text):
    try:
        print('Loading Get Seclists...')
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"./outputSeclists/{selected_item_text}.txt", "wb") as f:
                f.write(response.content)
            print('⇢⇢⇢ Get Seclist Success ⇠⇠⇠')
        else:
            print('Get Api Error...')
    except Exception as e:
        print('Get Seclists Error...')


def print_banner():
    banner = [characters.T, characters.O, characters.O, characters.L, characters.S,
              characters.space, characters.S, characters.A, characters.I, characters.N, characters.T]
    final = []
    print('\r')
    init_color = 36
    txt_color = init_color
    cl = 0

    for charset in range(0, 3):
        for pos in range(0, len(banner)):
            for i in range(0, len(banner[pos][charset])):
                clr = f'\033[38;5;{txt_color}m'
                char = f'{clr}{banner[pos][charset][i]}'
                final.append(char)
                cl += 1
                txt_color = txt_color + 36 if cl <= 3 else txt_color

            cl = 0
            txt_color = init_color
        init_color += random_number
        if charset < 2:
            final.append('\n   ')
    print(f"   {''.join(final)}")
    print(f'⇢⇢⇢ © OutLand. All rights reserved. Version 1.0 ⇠⇠⇠\n                 Tele:@outland1231')


def print_menu():
    print("❍❍❍ MENU ❍❍❍")
    print("1. Show menu.")
    print("2. Get Proxys-Socks Free!")
    print("3. Check Proxys-Socks Free!")
    print("4. Get Seclists Free!")
    print("99. Exit.")
    option = int(input("Choise one options (1-4)⇥⇥⇥⇥: "))
    handle_option(option)

def print_menu_seclists():
    print('⁍⁍⁍ MENU SECLISTS ⁌⁌⁌')
    print("1. ignis-1K.")
    print("2. ignis-10K.")
    print("3. ignis-100K.")
    print("4. ignis-1M.")
    print("5. ignis-10M.")
    print("99. Go back menu!")
    condition = int(input("Choise one payload (1-5)⌱⌱⌱⌱: "))
    match condition:
        case 1:
            download_and_handle(
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Pwdb-Public/Wordlists/ignis-1K.txt", 'ignis-1K')
        case 2:
            download_and_handle(
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Pwdb-Public/Wordlists/ignis-10K.txt", 'ignis-10K')
        case 3:
            download_and_handle(
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Pwdb-Public/Wordlists/ignis-100K.txt", 'ignis-100K')
        case 4:
            download_and_handle(
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Pwdb-Public/Wordlists/ignis-1M.txt", 'ignis-1M')
        case 5:
            download_and_handle(
                "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Pwdb-Public/Wordlists/ignis-10M.txt", 'ignis-10M')
        case 99:
            ''


def handle_option(option):
    match option:
        # case 1:
        #     filename = input("Import List Group (.txt): ")
        #     if os.path.exists(filename):
        #         with open(filename, 'r', encoding='utf-8') as file:
        #             content = file.read()
        #             data = content
        #         print(f"Content of {filename}:\n{content}:\n{data}")
        #     else:
        #         print(f"File {filename} does not exist.")
        #         print_menu()
        case 1:
            ''
        case 2:
            print('⇢⇢⇢ Loading Get Proxys... ⇠⇠⇠')
            script_path = os.path.join("scripts", "getproxy.py")
            run_script(script_path)
            print('⇢⇢⇢ Success download lists Proxy ⇠⇠⇠')
        case 3:
            print('⇢⇢⇢ Loading Checker Proxys... ⇠⇠⇠')
            script_path = os.path.join("scripts", "checkproxy.py")
            run_script(script_path)
            print('⇢⇢⇢ Success Checker lists Proxy ⇠⇠⇠')
        case 4:
            print_menu_seclists()
        case 99:
            print("⇢⇢⇢ Goodbye! ⇠⇠⇠")
            exit()
        case _:
            print("Option not valid.")


def main():
    print_banner()
    while True:
        try:
            print_menu()
        except ValueError:
            print("Please input number valid!")


if __name__ == "__main__":
    main()
