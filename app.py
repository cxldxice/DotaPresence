import threading
import time

import pymem

import server


#проверка открыта ли дота
def is_open():
    try:
        pymem.Pymem("dota2.exe")
        return True

    except pymem.exception.ProcessNotFound:
        return False


def main():
    server_thread = threading.Thread(target=server.polling)
    server_thread.daemon = True #если мейн поток закроется то и этот поток завершит работу 
    server_thread.start() #run server on 127.0.0.1:6768

    #засунул в отдл поток чтобы сделаьб проверку
    #если даты к примеру нету минуты там то прекращать пресенс 
    #чтобы получить дату data = server.data["dota"]
    #также дату json можно смотрететь в рил тайм по http://127.0.0.1:6768/debug

    time.sleep(99999) #чтобы не закр мейн поток


if __name__ == "__main__":
    main()


