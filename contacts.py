# -*- coding: utf-8 -*-
#для сервера
#send_answer(userid, msg) для отправки ответа userid - пользователь msg - текст
#get_request(userid) возвращает запрос от userid - пользователь первый запрос должен быть поле

#инициализация сессии
import sys, time, math, random, vk
from drawing import *
from message import *
sys.stdin = open('token_server.txt','r')
token = input()
sys.stdin.close()
sys.stdin = open('bot1.txt','r')
id_bot1 = int(input()) #ввести id бота 1
sys.stdin.close()
sys.stdin = open('bot2.txt','r')
id_bot2 = int(input()) #ввести id бота 2
sys.stdin.close()
session = vk.Session(access_token=token)
api=vk.API(session)
user_field=[[0]*12 for x in range(12)]
helping_str='Помощь по игре\nДля того, чтобы выстрелить введите координаты выстрела в следующем формате:\n<заглавная латинская буква от A до J><число от 1 до 10> (например "J5" (без кавычек)).\nЧтобы вывести своё поле введите "Мое поле" (без кавычек).\nЕсли бот не отвечает на ваши сообщения, то это может происходить по двум причинам:\n__1)неверный формат ввода (проверьте, что вы вводите именно в том формате, который указан выше. Частая ошибка - использование букв русского алфавита)\n__2)боту нужна капча (вам в личные сообщения должна была прийти картинка, текст на которой надо отправить отправителю).\nБот ожидает ответа в течение 15 минут, а затем автоматически выключается. Будьте внимательны.\nЧтобы узнать правила игры, введите "Правила" (без кавычек).\n'
#+'Чтобы вывести своё поле введите "Мое поле" (без кавычек).\n'+'Если бот не отвечает на ваши сообщения, то это может происходить по двум причинам:\n'+'1)неверный формат ввода (проверьте, что вы вводите именно в том формате, который указан выше. Частая ошибка - использование букв русского алфавита)\n'+'2)боту нужна капча (вам в личные сообщения должна была прийти картинка, текст на которой надо отправить отправителю).\n'+'Бот ожидает ответа в течении 15 минут, а затем автоматически выключается. Будьте внимательны.\n'+'Чтобы узнать правила игры введите "Правила" (без кавычек).\n'+'По любым другим вопросам пишите мне (vk.com/id22346494).'    
help_mas=['Мое поле','Моё поле','мое поле','моё поле']
need_help=['Помощь','помощь','help','Help']
rules=['Правила','правила']
rule1='Правила игры\n'+'В игре морской бой играющие имеют свое поле 10x10. В начале игры каждый играющий расставляет свои корабли (один четырехклеточный, два трехклеточных, три двухклеточных, четыре одноклеточных). Корабли представляют из себя прямую непрерывную последовательность клеток. Корабли не могут пересекаться, касаться (как углами, так и сторонами).\n'+'В процессе игры игроки пытаются найти на поле все корабли соперника. Для этого они стреляют, отправляя серверу точку, в которой, по их предположению, может находиться корабль соперника (то есть совершают ход). Игроки ходят по очереди. В ответ они получают одно из трех сообщений:\n'
rule2='"Промах" означает, что в данной клетке поля соперника корабля нет.\n'+'"Ранение" означает, что в данной клетке поля соперника находится корабль, не все клетки которого еще ранены. Игрок имеет право на еще один ход.\n'+'"Убит" означает, что в данной клетке поля соперника находится корабль, все клетки которого уже ранены. Такой корабль зачисляется на счет игрока. Игрок имеет право на еще один ход.\n'+'Победителем объявляется игрок, который первым убил все корабли соперника.'
#print(helping_str)
#print(rule)
def send_answer(userid, msg): #отправка ответа
    ctr=0
    while 1:
        ctr+=1
        #print('я тута')
        try:
            messages_send(userid, msg);
            break
        except Exception as e:
            time.sleep(3)
            print(e,ctr)


firstmsgbot = [1, 1]
timemsgbot = [0, 0]

def check_format_field(msg): #проверка что это поле по формату
    #print('enter the function')
    count = 100
    for i in range (len(msg)):
        #print(msg)
        if (msg[i] == '1' or msg[i] == '0'):
            count -= 1
    #print(count)
    return (count == 0)

def check_format_request(message):
    global user_field
    message_s = str(message)
    if str(message_s) in help_mas:
        draw_the_field(user_field, id_bot2,'Ваше поле выглядит так:')
        return False
    if len(message_s)<=1:
        return False
    if (65 <= ord(message_s[0]) <= 74) and (49 <= ord(message_s[1]) <= 57):
        if len(message_s) == 2:
            return True
        elif len(message_s) == 3 and (ord(message_s[1]) == 49) and (ord(message_s[2]) == 48):
            return True
        else:
            return False
    else:
        return False


def get_request(userid): #получение запроса от userid
    start_time=time.time()
    while (1):
        #print(time.time()-start_time, firstmsgbot)
        if time.time()-start_time>900 and (1 not in firstmsgbot):
            print('Time Limit')
            messages_send(userid,'Поражение')
            if str(userid)!=str(id_bot1):
                messages_send(str(id_bot1),'Победа')
            else:
                messages_send(str(id_bot2),'Победа')
            sys.exit(0)
        try:
            new_msg = api.messages.getHistory(offset = 0, count = 1, user_id = userid, rev = 0)
        except Exception as e:
            print(e)
            time.sleep(3)
            continue
        if (len(new_msg) <=1):
            time.sleep(3)
            continue
        msg = new_msg[1]['body']
        date = new_msg[1]['date']
        
        if (new_msg[1]['uid'] != userid):
            time.sleep(3)
            continue
        if msg in need_help:
            #print('here')
            messages_send(str(id_bot2), helping_str)
            time.sleep(2)
            continue
        if msg in rules:
            messages_send(str(id_bot2), rule1)
            messages_send(str(id_bot2), rule2)
            time.sleep(2)
            continue
        #если это первый запрос userid это должно быть поле
        if ((userid == id_bot1 and firstmsgbot[0] == 1 and timemsgbot[0] != date) or
            (userid == id_bot2 and firstmsgbot[1] == 1 and timemsgbot[1] != date)):
            if (check_format_field(msg)):
                if (userid == id_bot1): #изменяем время
                    timemsgbot[0] = date
                else:
                    timemsgbot[1] = date
                return msg #возвращаем результат запроса
        # если это не первый запрос userid
        elif (((userid == id_bot1 and timemsgbot[0] != date) or (userid == id_bot2 and timemsgbot[1] != date))
              and (check_format_request(msg))):
            if (userid == id_bot1): #изменяем время
                timemsgbot[0] = date
            else:
                timemsgbot[1] = date
            return msg #возвращаем результат запроса
        time.sleep(3)

#print(get_request(id_bot1))
