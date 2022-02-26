import  subprocess
from pathlib import Path



def extract_wifi_passwords(encode = "cp866"):
    """Extracting Windows Wi-Fi passwords into .txt file"""
    profiles_data = subprocess.check_output('netsh wlan show profiles').decode(encode, "ignore").split('\n')
    profiles = [i.split(':')[1].strip() for i in profiles_data if 'All User Profile' in i or "Все профили пользователей" in i]

    for profile in profiles:
        try:
            profile_info = subprocess.check_output(f'netsh wlan show profile "{profile}" key=clear').decode(encode, "ignore").split('\n')
            try:
                password = [i.split(':')[1].strip() for i in profile_info if 'Key Content' in i or  "Содержимое ключа" in i][0]
            except IndexError:
                password = None
            txt = f'Profile: {profile}\nPassword: {password}\n{"#" * 20}\n\n'
        except:
            txt = f"Profile '{profile}' not found\n{'#' * 20}\n\n"
        finally:
            with open(file='wifi_passwords.txt', mode='r', encoding='utf-8') as f:
                fl = f.read()
                if txt in fl:
                    continue
            with open(file='wifi_passwords.txt', mode='a', encoding='utf-8') as file:
                file.write(txt)
            


def main():
    try:
        extract_wifi_passwords("cp866")
    except:
        extract_wifi_passwords("cp1251")
if __name__ == '__main__':
    main()