# -*- coding: utf-8 -*-
import sys,vk, threading
from main_server import *
from my_algo import *
# Чтение токена
token = open('token_server.txt','r')
api = vk.API(vk.Session(access_token=token.read()))
token.close()
# Чтение всех пользователей, даты последней игры. "Антиспам"
users_file = open('users.txt','r')
users_time = {}
reads = ' '
while reads != '': # While not eof
    reads = users_file.readline()
    user,time = reads.split(' ')
    users_time[int(user)] = int(time)
users_file.close()
while True:
    messages = api.messages.search(q='хочу играть',count=200) # Кодовое слово для начала игры
    for i in messages['items']: # Пока не отработаем все старые сообщения, новые не принимаем
        player,time = i['user_id'], i['time'] # id игрока и время сообщения
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
            for ids in users_time.keys():
                users_file.write(str(ids)+' '+str(users_time[ids]))
            users_file.close()
