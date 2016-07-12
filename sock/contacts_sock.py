# -*- coding: utf-8 -*-
#для сервера
#send_answer(userid, msg) для отправки ответа userid - пользователь msg - текст
#get_request(userid) возвращает запрос от userid - пользователь первый запрос должен быть поле

#инициализация сессии
import sys, time, math, random
import socket

sock = socket.socket()

sin=open('port.txt','r')###
portc = int(sin.read())
sin.close()

sock.bind(("", portc))
sock.listen(100)
conn = []
addr  = []
firstmsgbot = []
timemsgbot = []
def init_sock(sz, iindex): #init инициализация сокет соединений вызвать в маине
    for i in range(sz):
        conn.append(0)
        addr.append(0)
        firstmsgbot.append(1)
        timemsgbot.append(time.time())
        conn[i + iindex], addr[i + iindex] = sock.accept()
        conn[i + iindex].setblocking(0)
        print ('connected:', addr[i + iindex])

def send_to_client(index, msg):
    ctr = 0
    tttime = time.time()
    timeer = time.time()
    while 1:
        if (time.time() - tttime > 5 * 60):
            print("player ", index, " not ask")
            return "*"
        ctr += 1
        try:
            conn[index].send(msg.encode())
            print("send ", msg, " client ", index)
            break
        except Exception as e:
            if (time.time() - timeer > 60):
                print(e, ctr, " send", index)
                timeer = time.time()


def send_answer_sock(index, msg): #отправка ответа
    return send_to_client(index, msg)

def check_format_field(msg): #проверка что это поле по формату
    count = 100;
    for i in range (len(msg)):
        if (msg[i] == '1' or msg[i] == '0'):
            count -= 1
    return (count == 0)

def check_format_request(message):
    global user_field
    message_s = str(message)
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


def get_from_client(index):
    msg = ""
    time_t = time.time()
    ctr = 0
    while True:
        ctr += 1
        try:
            data = conn[index].recv(10000)
        except Exception as e:
            if (time.time() - time_t > 60):
                time_t = time.time()
                print(e, ctr, " get", index)
            if (firstmsgbot[index] == 0 and time.time() - timemsgbot[index] > 5*60):
                return ("*")
            continue
        if not data:
            break
        msg = data.decode("utf-8")
        if (len(msg) > 0):
            break
    return msg

def get_request_sock(index): #получение запроса от index 0 или 1
    timemsgbot[index] = time.time()
    while (1):
        msg = get_from_client(index)
        if (msg == "*" and firstmsgbot[index] == 0):
            return "*"
        #если это первый запрос index это должно быть поле
        if (firstmsgbot[index] == 1):
            if (check_format_field(msg)):
                firstmsgbot[index] = 0
                timemsgbot[index] = time.time()
                print("get field client ", index)
                return msg #возвращаем результат запроса
        # если это не первый запрос index
        elif (check_format_request(msg)):
            timemsgbot[index] = time.time()
            print("get ", msg, " client ", index)
            return msg #возвращаем результат запроса

