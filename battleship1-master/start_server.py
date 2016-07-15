# -*- coding: utf-8 -*-
import sys,vk, threading, time, os
from main_server import *
from my_algo import *
# Чтение токена
lastgame = 0
ts=int(time.time())
token = open('token_server.txt','r')
gg = token.read()
api = vk.API(vk.Session(access_token=gg[:-1]))
token.close()
botOfff = open('post.txt','r')
botoff = botOfff.readline()
botOfff.close()
api.wall.delete(post_id=botoff) # Удаляем запись о том, что бот отключен
postId = api.wall.post(message='Бот свободен, ты можешь поиграть с ним прямо сейчас!\nКак сыграть смотри в официалной группе проекта:https://vk.com/battleship_chat')['post_id'] # Делаем запись о том, что бот свободен
api.wall.pin(post_id=postId)                    # Закрепляем запись
# Чтение всех пользователей, даты последней игры. "Антиспам"
try:
    users_file = open('users.txt','r')
    users_time = {}
    reads = users_file.readline()
    while reads != '': # While not eof
        print(reads.split())
        user,times = reads.split(' ')
        users_time[int(user)] = int(times)
        reads = users_file.readline()
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
                time.sleep(2)
                messages = api.messages.search(q='хочу играть',count=100) # Кодовое слово для начала игры
                break
            except Exception as e:
                print('Исключение!',e)
                time.sleep(2)
        if len(messages) == 1:
            continue
        for i in messages[-1::-1]: # Пока не отработаем все старые сообщения, новые не принимаем
            if type(i) is int:
                continue
            player,times = i['uid'], i['date'] # id игрока и время сообщения
            if player not in users_time.keys(): # Если игрок еще никогда не играл
                users_time[player] = 0
            if users_time[player] < times and ts < times: # Если это не спам, то начинаем играть
                out = open('talking.txt','w')
                out.write('gameBegan with '+str(player)) # Лог by Игорь
                out.close()
                playerName = api.users.get(user_ids=player,name_case='ins')[0]
                api.wall.delete(post_id=postId)
                postId = api.wall.post(message='Сейчас идет игра с @id{1}({0}). Бот занят. \n Хочешь поиграть? Смотри, как это сделать, тут: https://vk.com/battleship_chat '.format(
                    playerName['first_name'] + ' ' + playerName['last_name'],
                    player))['post_id'] # Публикуем пост о том, что бот занят
                api.wall.pin(post_id=postId)
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
                users_time[player] = int(time.time()) # Обновляем время последней игры
                for ids in users_time.keys():
                    users_file.write(str(ids)+' '+str(users_time[ids]) + '\n')
                users_file.close()
                api.wall.delete(post_id=postId)
                playerNameRes = api.users.get(users_id=player)[0]
                result = open('result','r')
                res = result.readline()
                result.close()
                if res == 'victory':
                    api.wall.post(message='''Поздравляем! @id{0}({1}) только что выиграл у бота в морской бой! Ты тоже сможешь!
О том, как сыграть, можно прочитать в официальной группе проекта:https://vk.com/battleship_chat'''.format(player,playerNameRes))
                elif res == 'lose':
                    api.wall.post(message="""К сожалению, @id{0}({1}) только что проиграл боту в морской бой. Может быть, именно ты сможешь выиграть?
О том, как сыграть, можно прочитать в официальной группе проекта:https://vk.com/battleship_chat""".format(player,playerNameRes))
                else:
                    api.wall.post(message="""К сожалению, партия @id{0}({1}) и бота не была окончена. Если проблема на нашей стороне, то ошибка будет устранена в ближайшее время.
О любых ошибках сообщайте в официальную группу проекта:""".format(player,playerName))
                postId = api.wall.post(message='Бот свободен, ты можешь поиграть с ним прямо сейчас!\nКак сыграть смотри в официалной группе проекта:https://vk.com/battleship_chat')['post_id'] # Делаем запись о том, что бот свободен
                api.wall.pin(post_id=postId)  # Закрепляем запись
except KeyboardInterrupt or SystemExit: # Если вы решили выйти
    api.wall.delete(post_id=postId)
    pId = api.wall.post(message='Бот выключен.\n'
                                'Узнай о его включении в официальной группе проекта: https://vk.com/battleship_chat !')['post_id']
    api.wall.pin(post_id=pId)
    post = open('post.txt', 'w')
    post.write(str(pId))
    post.close()
