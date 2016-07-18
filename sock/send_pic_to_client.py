import sys, time, math, random, socket
from contacts_sock import *

def get_null_string(gg):  # дописывает 0 в начало строки до длины 10
    k = 10 - len(gg)
    hh = '0' * k
    ss = hh + gg
    return ss


def get_pref(index, length):  # создает заголовок пакета позиция + длина
    temp0 = get_null_string(str(index))
    temp2 = get_null_string(str(length))
    ans0 = temp0 + temp2
    ans1 = ans0.encode('utf-8')
    return ans1


def send_to_client1(msg, index):  # отправляет большое сообщение msg сначала размер потом по частям содержание
    t_time = time.time()
    while 1:
        try:
            temp = str(len(msg)).encode()
            temp = get_pref(0, len(temp) + 20) + temp
            conn[index].send(temp)
            break
        except Exception as e:
            if (time.time() - t_time > 60):
                print(e, " send len to client ", index)
                return "*"

    t_time = time.time()
    while 1:
        try:
            data = conn[index].recv(10000)
            ttmp = data.decode('utf-8')
            if ((len(ttmp) >= len("134")) and (ttmp[-len("134"):] == "134")):
                break
        except Exception as e:
            if (time.time() - t_time > 60):
                print(e, " get accept len from client ", index)
                return "*"

    t_time = time.time()
    i = 0
    split_len = 1400
    while i < len(msg):
        while 1:
            try:
                temp = msg[i:min(len(msg), i + split_len)]
                temm = get_pref(i, len(temp) + 20)
                temr = temm + temp
                conn[index].send(temr)
                flag = 0
                tt_time = time.time()
                while 1:
                    try:
                        data = conn[index].recv(10000)
                        ttmp = data.decode('utf-8')
                        if ((len(ttmp) >= len("134")) and (ttmp[-len("134"):] == "134")):
                            flag = 1
                            break
                    except Exception as e:
                        if (time.time() - tt_time > 0.1):
                            flag = 0
                            break
                if (flag == 1):
                    i += split_len
                    break
                else:
                    continue
            except Exception as e:
                if (time.time() - t_time > 60):
                    print(e, " send picture to client ", index)
                    return "*"


def send_pic(file_name, index):  # отправляет картинку
    sin = open(file_name, 'rb')  ###
    send = sin.read()
    if (send_to_client1(send, index) == "*"):
        sin.close()
        print("client ", index, " not get picture")
        return "*"
    sin.close()
