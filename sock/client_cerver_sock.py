# -*- coding: utf-8 -*-
#версия для игры с сервером
#get_answer(a,b): по координатам a b [1 10] возвращает результат выстрела
#вызвать connect_to_server()
import sys, time, math,random
import socket
from check_okrest import *
from pict import *
py_flag=1
try:
    from PIL import Image, ImageDraw
    py_flag = 1
except:
    print('Фронтенд отключен, так как у вас нет PIL')
    py_flag = 0
killed=0

sock = socket.socket()
mimo = ['Прoмаx','Прoмах','Прoмax','Прoмaх','Промаx','Промах','Промax','Промaх','Пpoмаx','Пpoмах','Пpoмax','Пpoмaх','Пpомаx',
        'Пpомах','Пpомax','Пpомaх']
ranen = ['Paнeниe','Paнeние','Paнениe','Paнение','Pанeниe','Pанeние',
         'Pанениe','Pанение','Рaнeниe','Рaнeние','Рaнениe',
         'Рaнение','Ранeниe','Ранeние','Ранениe','Ранение']
ubit = ['Убит','убит','Убил','убил']
used = ['Вы уже стреляли сюда', 'Bы уже стреляли сюда', 'Вы ужe стреляли сюда', 'Вы уже cтреляли сюда',
        'Вы уже стрeляли сюда', 'Вы уже стреляли cюда', 'Вы уже стреляли сюдa']

gin=open('server_IP.txt','r')###
server_ip = gin.read()
gin.close()

hin=open('name.txt','r')###
name = hin.read()
hin.close()

sin=open('port.txt','r')###
portc = int(sin.read())
sin.close()



last_message = 0
firstmsg = [0]
endgame = [0]

def send_to_server(msg):
    tttime = time.time()
    timeer = time.time()
    ctr = 0
    while 1:
        ctr += 1
        if (time.time() - tttime > 6 * 60 and firstmsg[0]):
            print("server not ask")
            return "*"
        try:
            sock.send(msg.encode())
            break
        except Exception as e:
            if (time.time() - timeer > 60):
                timeer = time.time()
                print(e, ctr)



def message_get():
    global last_message
    msg = ""
    time_t = time.time()
    ctr = 0
    while True:
        ctr += 1
        try:
            data = sock.recv(10000)
        except Exception as e:
            if (time.time() - time_t > 60):
                time_t = time.time()
                print(e, ctr)
            if (last_message - time.time() < -6*60 and firstmsg[0]):
                print("time out")
                return "*"
            continue
        if not data:
            break
        msg = data.decode("utf-8")
        if (len(msg) > 0):
            last_message = time.time()
            break
    return msg



#отправляет запрос по координатам x y
def send_message(x,y):
    letter = 'ABCDEFGHIJ'
    ctr=0
    while 1:
        ctr+=1
        try:
            if (send_to_server(letter[y - 1] + str(x)) == "*"):
                return "*"
            print(letter[y-1]+str(x))
            break
        except Exception as e:
            print(e, ctr)
            
# принимаем сообщение соперника о результате нашего хода (Мимо - -1, Ранил - 1, Убил - 2, Вы уже сюда стреляли - 3, Конец игры - 4, Победа - 5, Поражение - 6, Сервер не отвечает - 7  иначе - ошибка)
def get_answer(a,b):
    if (endgame[0] == 1):
        return 4
    if (send_message(a,b) == "*"):
        endgame[0] = 1
        return 7
    while True:
        msg=message_get()
        if (msg == "*"):
            endgame[0] = 1
            return 7
        firstmsg[0] = 1
        if msg in mimo:
            return -1
        elif msg in ranen:
            return 1
        elif msg in ubit:
            return 2
        elif msg in used:
            return 3
        elif ((len(msg) > len("Победа")) and (msg[-len("Победа") : ] == "Победа")):
            print("Победа")
            unique_add = str(random.randint(0, 10 ** 9))
            get_pic('result' + unique_add + '.jpg', sock)
            if py_flag:
                res =  Image.open('result' + unique_add + '.jpg')
                res.show()
                res.close()
            endgame[0] = 1
            return 5
        elif msg == 'Поражение' or msg =='Победа':
            print(msg)
            unique_add = str(random.randint(0, 10 ** 9))
            get_pic('result' + unique_add + '.jpg', sock)
            if py_flag:
                res =  Image.open('result' + unique_add + '.jpg')
                res.show()
                res.close()
            endgame[0] = 1
            if (msg == "Победа"):
                return 5
            if (msg == "Поражение"):
                return 6

#тоже что и get_answer только без перевода форматов
def get_result(req):
    if (endgame[0] == 1):
        return "Игра уже завершена"
    if (send_to_server(req) == "*"):
        endgame[0] = 1
        return ("Сервер не отвечает")
    while True:
        msg = message_get()
        if (msg == "*"):
            endgame[0] = 1
            return ("Сервер не отвечает")
        firstmsg[0] = 1
        if msg in mimo:
            return "Промах"
        elif msg in ranen:
            return "Ранение"
        elif msg in ubit:
            return "Убит"
        elif msg in used:
            return "Вы уже стреляли сюда"
        elif msg == 'Поражение' or msg == 'Победа':
            unique_add = str(random.randint(0, 10 ** 9))
            get_pic('result' + unique_add + '.jpg', sock)
            if py_flag:
                res.show()
                res.close()
            endgame[0] = 1
            return (msg)
        elif ((len(msg) > len("Победа")) and (msg[-len("Победа") : ] == "Победа")):
            unique_add = str(random.randint(0, 10 ** 9))
            get_pic('result' + unique_add + '.jpg', sock)
            if py_flag:
                res.show()
                res.close()
            endgame[0] = 1
            return ("Победа")

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
                        if 59<=check_okr(change_field(field))<=61:
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
            if (send_to_server(msg) == "*"):
                return "*"
            break
        except Exception as e:
            print(e)

def send_field():
    while (1):
        temp_field = make_field()
        print("send_field")
        if (send_field_to_server(temp_field) == "*"):
            return "*"
        temp = str(message_get())
        if (temp == "*"):
            return "*"
        if temp == "1":
            return

# процесс игры

def connect_to_server():
    global sock
    sock = socket.socket()
    global last_message
    global server_ip
    global portc
    global name
    last_message=time.time()
    print("server IP = '" + server_ip + "'")
    try:
        sock.connect((server_ip, portc))
        sock.setblocking(0)
    except Exception as e:
        print(e, "не удалось подключиться к серверу")
        return "*"
    print("connect")
    firstmsg[0] = 0
    if (send_to_server(name) == "*"):
        return "*"
    if (message_get() == "*"):
        return "*"
    endgame[0] = 0
    if (send_field() == "*"):
        return "*"

#connect_to_server()
#from pict import *
#функция игры
#используйте get_answer(a,b): по координатам a b [1 10] возвращает результат выстрела


