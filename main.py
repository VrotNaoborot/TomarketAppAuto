import time
import urllib

import requests_data, csv
import json
import random

from validproxy import validproxy
from requests_data import *
from colorama import Fore
from data_worker import DATA_FILE, reader_data
from datetime import datetime


def view_farming(new_token, proxy):
    farming, farming_status = start_farming(new_token, proxy=proxy)
    if farming is not None and farming_status == 200:
        end_time = datetime.fromtimestamp(farming['data']['end_at'])
        finish_farming = end_time - datetime.now()
        count_second_for_finish = int(finish_farming.total_seconds())
        if farming['status'] == 500 and farming['message'] == 'game end need claim':
            print(f"{Fore.CYAN}[ FARMING ] Фарминг закончился.")

        elif farming['status'] == 0 and farming['message'] == '':
            print(f"{Fore.CYAN}[ FARMING ] Начинаем фарминг.")
            return count_second_for_finish
        elif farming['status'] == 500 and farming['message'] == 'game already started':
            print(f"{Fore.CYAN}[ FARMING ] Фарминг уже  начался.")
        else:
            print(f"{Fore.RED}[ FARMING ] Ошибка: {farming}")
    else:
        print(f"{Fore.CYAN}[ FARMING ] Не удалось получить фарминг: {farming}")


def main():
    say_hello()

    data = reader_data()
    if len(data) == 0:
        print(Fore.RED + "Отсутствуют данные для аккаунтов")
        exit()

    print("Проверка прокси")

    # Проверка прокси
    for acc in data:
        proxy_data = acc['proxy']
        if proxy_data == '':
            r = input(
                Fore.RED + f"Аккаунт: {acc['number']}. Отсутствует прокси. Вы хотите продолжить? (y/n):\n").strip().lower()
            if r == 'n':
                exit()
        elif validproxy(acc['proxy']):
            print(Fore.CYAN + f"Аккаунт: {acc['number']}. Прокси валид")
        else:
            print(Fore.RED + f"Аккаунт: {acc['number']}. Прокси не валид")
            exit()
    # Farm
    max_delay = 0
    while True:
        for i, acc in enumerate(data, 1):
            user_data = acc['query'].split('&')[0].split('=')[1]
            user_info = urllib.parse.unquote(user_data)
            user_info = json.loads(user_info)

            username = user_info.get('username', '')
            firstname = user_info.get('first_name', 'Unknown')
            lastname = user_info.get('last_name', '')
            fullname = ', '.join([i for i in [firstname, lastname] if i != ''])

            proxy = None if acc['proxy'] == '' else {'http': acc['proxy'], 'https': acc['proxy']}
            token = None if acc['access_token'] == '' else acc['access_token']

            token, new_token_code = login_api(acc['query'], proxy=proxy, access_token=token)
            # print(f"New token: {new_token}")
            new_token = None
            print(
                Fore.LIGHTBLUE_EX + f"\n\n===== [ {username} ({fullname}) ] =====             ",
                flush=True)
            if token is not None and new_token_code == 200:
                if token['status'] == 0 and token['message'] == '':
                    # Записываем новый полученный токен
                    new_token = token['data']['access_token']
                    acc['access_token'] = new_token
                    print(Fore.CYAN + "[ INFO ] Новый токен получен. Авторизация выполнена.")
                else:
                    print(
                        Fore.RED + f"[ ERROR ] Не удалось получить access_token для аккаунта {acc['number']}. Аккаунт пропущен.\n{'=' * 30}")
                    continue
            else:
                print(
                    Fore.RED + f"[ ERROR ] Не удалось получить access_token для аккаунта {acc['number']}. Аккаунт пропущен.\n{'=' * 30}")
                continue

            time.sleep(2)
            daily, daily_status = daily_claim(new_token, proxy=proxy)
            # print(daily)
            if daily is not None and daily_status == 200:
                day_streak = daily['data']['check_counter']
                point_today = daily['data']['today_points']
                if daily['status'] == 0 and daily['message'] == '':
                    print(f"[ DAILY ] Получено: {point_today}. День: {day_streak}")
                elif daily['status'] == 400 and daily['message'] == 'already_check':
                    print(f"[ DAILY ] День: {day_streak}")
                else:
                    print(f"{Fore.RED}[ DAILY ] Ошибка: {daily}")
            else:
                print(f"{Fore.RED}[ DAILY ] Не удалось получить доступ к daily")

            time.sleep(2)
            invite_code(new_token, proxy)

            time.sleep(2)
            balance_data, balance_status = user_balance(access_token=new_token, proxy=proxy)
            ticket = None

            farm_finished = None

            if balance_data is not None and balance_status == 200:
                if ('data' in balance_data and isinstance(balance_data['data'], dict) and
                        'farming' in balance_data['data']):
                    farming_end_at = datetime.fromtimestamp(balance_data['data']['farming']['end_at'])
                    if farming_end_at < datetime.now():
                        farm_finished = True
                    else:
                        farm_finished = False
                        farm_time_to_the_end = int((farming_end_at - datetime.now()).total_seconds())
                        if farm_time_to_the_end > max_delay:
                            max_delay = farming_end_at

                if balance_data['status'] == 0 and balance_data['message'] == '':
                    ticket = balance_data['data']['play_passes']
                    balance = balance_data['data']['available_balance']

                    print(f"{Fore.CYAN}[ BALANCE ] Количество билетов: {ticket}")
                    print(f"{Fore.WHITE}[ BALANCE ] Общий баланс: {balance}")
                else:
                    print(f"{Fore.RED}[ BALANCE ] Ошибка: {balance_data}")
            else:
                print(f"{Fore.RED}[ BALANCE ] Не удалось получить баланс. {balance_data}")

            time.sleep(2)
            info, info_code = farm_info(new_token, proxy)
            # if info is not None and info_code == 200:
            #     if 'data' in info and isinstance(info['data'], dict) and 'finished' in info['data']:
            #         print(f"{Fore.CYAN}[ CLAIM ] Токены уже собираются. Аккаунт пропущен")
            #         end_time = datetime.fromtimestamp(info['data']['end_at'])
            #         finish_farming = end_time - datetime.now()
            #         count_second_for_finish = int(finish_farming.total_seconds())
            #         if count_second_for_finish > max_delay:
            #             max_delay = count_second_for_finish
            #             continue

            # else:
            #   print(f"{Fore.CYAN}[ CLAIM ] Не удалось получить доступ к info: {info}")

            time.sleep(2)
            tasks_list(new_token, proxy=proxy)

            time.sleep(2)
            if farm_finished is None:
                time_sleep = view_farming(new_token, proxy=proxy)
                if time_sleep > max_delay:
                    max_delay = time_sleep

            elif farm_finished:
                claim, claim_status = claim_farming(new_token, proxy=proxy)
                if claim is not None and claim_status == 200:
                    if claim['status'] == 500 and claim['message'] == 'farm not started or claimed':
                        print(f"{Fore.RED} [ FARMING ] Не удалось собрать: {claim}")

                    elif claim['status'] == 0 and claim['message'] == '' and claim['data']['finished']:
                        points = claim['data']['points']
                        print(f"{Fore.CYAN}[ FARMING ] {points} поинтов собрано.")

                    elif claim['status'] == 0 and claim['message'] == '' and not claim['data']['finished']:
                        print(
                            f"{Fore.CYAN}[ FARMING ] Аккаунт: {acc['number']} не закончил фарм.")
                        end_time = datetime.fromtimestamp(claim['data']['end_at'])
                        if end_time > datetime.now():
                            finish_farming = end_time - datetime.now()
                            count_second_for_finish = int(finish_farming.total_seconds())
                            if count_second_for_finish > max_delay:
                                max_delay = count_second_for_finish
                else:
                    print(f"{Fore.RED}[ FARMING ] Ошибка: {claim}")

                time.sleep(2)
                time_sleep = view_farming(new_token, proxy=proxy)
                if time_sleep > max_delay:
                    max_delay = time_sleep
            else:
                print(f"{Fore.CYAN}[ FARMING ] Поинты уже собираются. ")

            # Game
            if ticket is not None:
                while ticket > 0:
                    print(f"{Fore.CYAN}[ GAME ] Начало игры...")
                    play, play_status = start_game(new_token, proxy)
                    if play is not None and play_status == 200:
                        if play['status'] == 0 and play['message'] == '':
                            print(f"{Fore.CYAN}[ GAME ] Игра началась.")

                            for j in range(30):
                                print(
                                    f"{random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE])}[ GAME ] Конец игры через: {30 - j} секунд..",
                                    end='\r', flush=True)
                                time.sleep(1)
                            print(f"{Fore.CYAN}[ GAME ] Игра завершена. Клеймим поинты...")

                            point = random.randint(700, 1300)
                            game, game_status = claim_game(new_token, point, proxy=proxy)
                            if game is not None and game_status == 200:
                                if game['status'] == 0 and game['message'] == '':
                                    print(f"{Fore.CYAN}[ GAME ] Получено: {point} поинтов")
                                else:
                                    print(f"{Fore.RED} [ GAME ] Не удалось получить токены. Ошибка: {game}")
                            ticket -= 1

                    else:
                        print(f"{Fore.CYAN}[ GAME ] Не удалось начать игру {play}")
                else:
                    print(f"{Fore.CYAN}[ GAME ] Билеты закончились")
            print(f"{Fore.CYAN}{'=' * 30}")

        with open(DATA_FILE, mode='w', encoding='utf-8', newline='') as file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)
            time_sleep_second = max_delay + random.randint(0, 100)
            print(
                f"{Fore.YELLOW}\n\n{'=' * 30}\n[ INFO ] Токены перезаписаны\n[ INFO ] Sleep: {time_sleep_second}\n{'=' * 30}")
        time.sleep(time_sleep_second)
        max_delay = 0


def say_hello():
    print(Fore.BLUE + r"""  _____                  
 |  __ \                 
 | |__) |_ _ _ __  _   _ 
 |  ___/ _` | '_ \| | | |
 | |  | (_| | | | | |_| |
 |_|   \__,_|_| |_|\__,_|                             
""")
    print(Fore.CYAN + "Questions - https://t.me/Panunchik")
    print(Fore.CYAN + "GitHub - https://github.com/VrotNaoborot")


if __name__ == '__main__':
    main()
