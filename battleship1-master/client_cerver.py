# -*- coding: utf-8 -*-
#версия для игры с сервером
#get_answer(a,b): по координатам a b [1 10] возвращает результат выстрела
#вызвать init()
import sys, time, math,random
import vk
from message import *
from check_okrest import *
sys.stdin=open('token_bot.txt','r')###
token=input()
sys.stdin.close()
sys.stdin=open('server.txt','r')
id_server=int(input()) #ввести id сервера
sys.stdin.close()
session=vk.Session(access_token=token)
api=vk.API(session)
killed=0
last_message=0

mimo = ['Прoмаx','Прoмах','Прoмax','Прoмaх','Промаx','Промах','Промax','Промaх','Пpoмаx','Пpoмах','Пpoмax','Пpoмaх','Пpомаx',
        'Пpомах','Пpомax','Пpомaх']
ranen = ['Paнeниe','Paнeние','Paнениe','Paнение','Pанeниe','Pанeние',
         'Pанениe','Pанение','Рaнeниe','Рaнeние','Рaнениe',
         'Рaнение','Ранeниe','Ранeние','Ранениe','Ранение']
ubit = ['Убит','убит','Убил','убил'] 

#получение сообщения
def message_get():
    global last_message
    while True:
        #print('я тута')
        time.sleep(3)
        msg=''
        try:
            new_msg = api.messages.getHistory(offset=0, count=1, user_id=id_server, rev=0);
            msg=new_msg[1]['body']
            date=new_msg[1]['date']
            if (len(new_msg) == 0):
                continue
            if (new_msg[1]['uid'] != id_server):
                continue
            #msg=input() ####
            #break ###
            if date!=last_message:
                last_message=date
                break
        except Exception as e:
            print(e)
    return msg
    
#отправляет запрос по координатам x y
def send_message(x,y):
    letter = 'ABCDEFGHIJ'
    ctr=0
    while 1:
        ctr+=1
        try:
            api.messages.send(user_id=id_server, message=letter[y - 1] + str(x))
            print(letter[y-1]+str(x))
            break
        except Exception as e:
            time.sleep(5)
            print(e, ctr)
    time.sleep(3)
            
    
# принимаем сообщение соперника о его выстреле (строка вида <буква ABCDEFGHIJ><число 12345678910>, иначе - ошибка)
def get_coordinate():
    letter = 'ABCDEFGHIJ'
    msg=message_get()
    return [int(msg[1:]), letter.index(msg[0])+1]
            
# принимаем сообщение соперника о результате нашего хода (Мимо - -1, Ранил - 1, Убил - 2, иначе - ошибка)
def get_answer(a,b):
    send_message(a,b)
    while True:
        msg=message_get()
        if msg in mimo:
            return -1
        elif msg in ranen:
            return 1
        elif msg in ubit:
            return 2
        elif msg == 'Поражение' or msg=='Победа':
            sys.exit(0)

            

# проверяет, не закончилась ли игра
def checker(field):
    for i in range(1, 11):
        for j in range(1, 11):
            if field[i][j] > 0:
                return 0
    return 1
# поиск всех возможных кораблей длины length на поле field
def get_ships(length, field):
    ships = []
    for i in range(1, 11):
        for j in range(1, 12 - length):
            coordinate = []
            good = True
            for k in range(j, j + length):
                if field[i][k] != 0:
                    good = False
                    break
                else:
                    coordinate.append([i, k])
            if good:
                ships.append(coordinate)
    for i in range(1, 12 - length):
        for j in range(1, 11):
            coordinate = []
            good = True
            for k in range(i, i + length):
                if field[k][j] != 0:
                    good = False
                    break
                else:
                    coordinate.append([k, j])
            if good:
                ships.append(coordinate)
    return ships

#приведение поля к типу 10х10
def change_field(field):
    new_field=[[0]*10 for i in range(10)]
    for i in range(1,11):
        for j in range(1,11):
            if field[i][j]>0:
                new_field[i-1][j-1]=1
            else:
                new_field[i-1][j-1]=0
    return(new_field)

# создание поля с нуля
def make_field():
    while True:
        ready = False
        field = [[0 for i in range(12)]
                 for j in range(12)]
        for i in range(12):
            field[11][i] = -1
            field[0][i] = -1
            field[i][11] = -1
            field[i][0] = -1
        boats = [0, 4, 3, 2, 1]
        now_ship = 4
        while True:
            ships = get_ships(now_ship, field)
            if len(ships) == 0:
                break
            else:
                rnd = random.randint(0, len(ships) - 1)
                current_ship = ships[rnd]
                for i in range(now_ship):
                    x = current_ship[i][0]
                    y = current_ship[i][1]
                    field[x][y] = -1
                    field[x + 1][y] = -1
                    field[x][y + 1] = -1
                    field[x - 1][y] = -1
                    field[x][y - 1] = -1
                    field[x + 1][y + 1] = -1
                    field[x - 1][y - 1] = -1
                    field[x + 1][y - 1] = -1
                    field[x - 1][y + 1] = -1
                for i in range(now_ship):
                    x = current_ship[i][0]
                    y = current_ship[i][1]
                    field[x][y] = now_ship
                boats[now_ship] -= 1
                if boats[now_ship] == 0:
                    now_ship -= 1
                    if now_ship == 0:
                        if 59<=check_okr(change_field(field))<=61:  ##59 61
                            ready = True
                        break
        if ready:
            return field

#отправка поля
def send_field_to_server(field):
    msg = ""
    for i in range(1, 11):
        for j in range(1, 11):
            temp = field[i][j]
            if temp == -1:
                temp = 0
            if temp > 0:
                temp = 1
            msg += str(temp) + ' '
        msg += "\n"
    while True:
        try:
            api.messages.send(user_id=id_server, message=msg)
            break
        except Exception as e:
            print(e)

def send_field():
    while (1):
        temp_field = make_field()
        print("send_field")
        send_field_to_server(temp_field)
        temp = str(message_get())
        if temp == "1":
            return
        

# процесс игры
def init():
    # кто ходит первым
    #message_get()
    #turn = start()
    #print('turn =',turn)
    #my_field = make_field()
    send_field()
init()

#функция игры
#используйте get_answer(a,b): по координатам a b [1 10] возвращает результат выстрела


