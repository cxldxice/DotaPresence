import threading
import time
from pypresence import Presence
import pymem

from heroes_names_dict import heroes_names_dict
import server


# проверка открыта ли дота
def is_open():
    try:
        pymem.Pymem("dota2.exe")
        return True

    except pymem.exception.ProcessNotFound:
        return False


def main():
    server_thread = threading.Thread(target=server.polling)
    server_thread.daemon = True  # если мейн поток закроется то и этот поток завершит работу
    server_thread.start()  # run server on 127.0.0.1:6768

    # time.sleep(100000)

    # засунул в отдл поток чтобы сделаьб проверку
    # если даты к примеру нету минуты там то прекращать пресенс
    # чтобы получить дату data = server.data["dota"]
    # также дату json можно смотрететь в рил тайм по http://127.0.0.1:6768/debug

    rpc = Presence(client_id="894510564817121301", pipe=0)
    rpc.connect()

    start_time = time.time()

    while True:
        is_open = dota_is_open()
        data = server.get_data()
        is_closed = server.get_connection_status()

        print(is_open, is_closed, len(data), data.keys())

        # Проверка на нахождение пользователя в игре(в запросе 5 элементов)
        if is_open and not is_closed and len(data) > 3:
            # Получение имени текущего героя
            current_hero_name = heroes_names_dict[data['hero']['name']]
            current_game_map = ''

            # Вычисление режима игры
            if data['map']['name'] == 'hero_demo_main':
                current_game_map = 'Testing hero ' + current_hero_name
            elif data['map']['name'] == 'start':
                current_game_map = 'Playing game for ' + current_hero_name
            else:
                current_game_map = data['map']['name']

            # Обновление статуса
            rpc.update(
                large_image=data['hero']['name'], large_text=current_hero_name,
                small_image=str(data['hero']['level']), small_text="Level " + str(data['hero']['level']),
                state=str(data["player"]["kills"]) + "/" + str(data["player"]["deaths"]) + "/" + str(
                    data["player"]["assists"]) + "; GPM/XPM: " + str(data["player"]["gpm"]) + "/" + str(
                    data["player"]["xpm"]),
                details="Now: " + current_game_map,
                start=int(start_time)
            )
            time.sleep(15)
            continue

        # Проверка на нахождение пользователя в меню(запрос пустой, но соединение не закрыто)
        if is_open and not is_closed:
            rpc.update(
                # large_image="logo", large_text="Dota 2",
                details="Main menu",
                start=int(start_time)
            )
            time.sleep(15)
        else:
            # Обновление таймера в жидании запуска
            start_time = time.time()
            time.sleep(60)


if __name__ == "__main__":
    main()
