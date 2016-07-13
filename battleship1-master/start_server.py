# -*- coding: utf-8 -*-
import sys,vk, threading, time, os
from main_server import *
from my_algo import *
# Чтение токена
lastgame = 0
token = open('token_server.txt','r')
gg = token.read()
api = vk.API(vk.Session(access_token=gg[:-1]))
token.close()
# Чтение всех пользователей, даты последней игры. "Антиспам"
try:
    users_file = open('users.txt','r')
    users_time = {}
    reads = users_file.readline()
    while reads != '': # While not eof
        reads = users_file.readline()
        user,time = reads.split(' ')
        users_time[int(user)] = int(time)
    users_file.close()
except FileNotFoundError:
    users_time = {}
    print('Файл не найден!')
    users_file = open('users.txt','w') #
    users_file.write('')               # Создаем файл, если его не существует
    users_file.close()                 #
except Exception as e:
    print('Необработанное исключение!\n Текст:\n',e) # Защита от вылетов
try:
    while True:
        while True:
            try:
                messages = api.messages.search(q='хочу играть',count=100) # Кодовое слово для начала игры
                break
            except Exception as e:
                print('Исключение!',e)
                time.sleep(2)
        for i in messages[-2::-1]: # Пока не отработаем все старые сообщения, новые не принимаем
            player,time = i['uid'], i['date'] # id игрока и время сообщения
            if player not in users_time.keys(): # Если игрок еще никогда не играл
                users_time[player] = 0
            if users_time[player] < time: # Если это не спам, то начинаем играть
                out = open('talking.txt','w')
                out.write('gameBegan with '+str(player)) # Лог by Игорь
                out.close()
                record = open('bot2.txt','w') # Пишем в файл id игрока для мэина
                record.write(str(player))
                record.close()
                serv = threading.Thread(target=st_serv, name="st_serv") # стартуем сервер
                serv.start()
                bot = threading.Thread(target=game, name="game") # стартуем бота
                bot.start()
                serv.join() # Ждем завершения всех потоков
                bot.join()
                users_file = open('users.txt','w') # Переписываем весь файл. TODO: Более элегантное решение
                users_time[player] = i['date'] # Обновляем время последней игры
                for ids in users_time.keys():
                    users_file.write(str(ids)+' '+str(users_time[ids]))
                users_file.close()
except KeyboardInterrupt or SystemExit: # Если вы решили выйти
    os.remove('bot2.txt')
    for ids in users_time.keys():
        users_file.write(str(ids) + ' ' + str(users_time[ids]))
    users_file.close()
    users_file = open('users.txt', 'w')