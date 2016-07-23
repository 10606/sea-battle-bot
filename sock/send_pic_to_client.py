import sys, time, math, random, socket, threading
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
    split_len = 1000
    count_pack = math.ceil(len(msg) / split_len)
    while 1:
        try:

            temp = (str(count_pack)).encode('utf-8')
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
            data = conn[index].recv(100)
            ttmp = data.decode('utf-8')
            if ((len(ttmp) >= len("9999999999")) and (ttmp[-len("9999999999"):] == "9999999999")):
                break
        except Exception as e:
            if (time.time() - t_time > 60):
                print(e, " get accept len from client ", index)
                return "*"


    t_time = time.time()
    i = 0

    #while i < len(msg):
    while i < count_pack:
        while 1:
            try:
                position = i * split_len
                temp = msg[position:min(len(msg), position + split_len)]
                temm = get_pref(i, len(temp) + 20)
                temr = temm + temp
                conn[index].send(temr)
                time.sleep(0.001)
                break
            except Exception as e:
                if (time.time() - t_time > 60):
                    print(e, " send picture to client ", index)
                    return "*"
        i += 1

    t_time = time.time()
    while 1:
        try:
            temp = ""
            temm = get_pref(9999999999, 20)
            temr = temm
            conn[index].send(temr)
            break
        except Exception as e:
            if (time.time() - t_time > 10):
                print(e, " send picture to client ", index)
                return "*"
    while (1):
        t_time = time.time()
        time_acc = time.time()
        index_pac = 0
        ttmp = 0
        while (1):
            if (time.time() - t_time > 40):
                return "*"
            try:
                data = conn[index].recv(10)
                ttmp = data.decode('utf-8')
                if (ttmp == "9999999999"):
                    return
                ttmp = int(ttmp)
                index_pac = int(int(ttmp) * split_len)
                print(ttmp, "req client ", index)
                break
            except Exception as e:
                if (time.time() - t_time > 60):
                    print(e, " get index from client ", index, "get request")
                    return "*"
                if (time.time() - time_acc > 1):
                    time_acc = time.time()
                    while 1:
                        try:
                            print(" send picture to client ", index, "send accept")
                            temp = ""
                            temm = get_pref(9999999999, 20)
                            temr = temm
                            conn[index].send(temr)
                            break
                        except Exception as e:
                            if (time.time() - time_acc > 10):
                                print(e, " send picture to client ", index, "send accept")
                                return "*"
        while (1):
            try:
                temp = msg[index_pac : min(len(msg), index_pac + split_len)]
                temm = get_pref(ttmp, len(temp) + 20)
                temr = temm + temp
                #print("send msg = ", temm, type(temr), len(temr))
                conn[index].send(temr)
                #print(ttmm, "send client ", index)
                break
            except Exception as e:
                if (time.time() - t_time > 60):
                    print(e, " send picture to client ", index, "send request")
                    return "*"


def send_pic(file_name, index):  # отправляет картинку
    sin = open(file_name, 'rb')  ###
    send = sin.read()
    thr = threading.Thread(target = send_to_client1, args = [send, index])
    thr.start()
    '''
    if (send_to_client1(send, index) == "*"):
        sin.close()
        print("client ", index, " not get picture")
        return "*"
    '''
    sin.close()
