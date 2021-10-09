import json
import os
import os.path
import shutil
import time
import requests

APPDATA = os.getenv('APPDATA').replace("\\", "/")
STARTUP = APPDATA + "/Microsoft/Windows/Start Menu/Programs/Startup"
PROJECT = APPDATA + "/DotaPresence"


def main():
    try:
        update = False
    
        current_version = requests.get("https://github.com/cxldxice/DotaPresence/blob/main/app.info?raw=True").json()
        
        if os.path.exists(PROJECT):
            try:
                with open(PROJECT + "app.info", "r") as meta:
                    local_version = json.load(meta)["version"]

                if local_version < current_version["version"]:
                    update = True
            except:
                update = True

            shutil.rmtree(PROJECT)
            os.mkdir(PROJECT)
        else:
            os.mkdir(PROJECT)
            update = True

        if update:
            app = requests.get(f"https://github.com/cxldxice/DotaPresence/blob/main/builds/{current_version}/DotaPresence.exe?raw=True").content

            with open(PROJECT + "/DotaPresence.exe", "wb") as app_path:
                app_path.write(app)
            with open(PROJECT + "/app.info", "w") as info_path:
                json.dump(info_path, current_version)

        os.system(f'"{PROJECT + "/DotaPresence.exe"}"')
              
    except Exception as e:
        print(e)


    return


main()