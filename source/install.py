import os
import time
import requests

APPDATA = os.getenv('APPDATA').replace("\\", "/")
STARTUP = APPDATA + "/Microsoft/Windows/Start Menu/Programs/Startup"

words = {
    "dl_process": {"ru": "Начинаем скачивание...", "en": "Start downloading..."},
    "dl_process_error": {"ru": "Не удалось скачать, проверьте соединение с интернетом", "en": "Download error, check enternet connection"},
    "i_process": {"ru": "Установка пакета...", "en": "Installing package..."},
    "i_process_error": {"ru": "Запустите программу от имени администратора", "en": "Run app as administrator"},
    "success": {"ru": "Спасибо за установку!", "en": "Thanks for installing!"}
}


def main():
    print("[+] Hello, User!")
    lang = str(input("[>] Choose language [RU|EN]: "))

    if lang.upper() == "RU" or lang.upper() == "RUSSIAN":
        lang_key = "ru"
    else:
        lang_key = "en"

    try:
        print(f"[+] {words['dl_process'][lang_key]}")
        updater = requests.get("https://github.com/cxldxice/DotaPresence/blob/main/builds/DotaPrsenceUpdater.exe?raw=True").content
    except Exception as e:
        print(e)
        print(f"[-] {words['dl_process_error'][lang_key]}")

        input("[!] Press enter to exit")
        return

    try:
        print(f"[+] {words['i_process'][lang_key]}")
        with open(STARTUP + "/DotaPresenceUpdater.exe", "wb") as updater_path:
            updater_path.write(updater)
        
    except:
        print(f"[-] {words['i_process_error'][lang_key]}")

        input("[!] Press enter to exit")
        return

    os.system(STARTUP + "/DotaPresenceUpdater.exe")
    print(f"[+] {words['success'][lang_key]}")
    input("[!] Press enter to exit")
    return


main()