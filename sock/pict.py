import sys, time, math,random
import socket

def send_accept(sock): #отправляет подтвердение серверу что получен пакет
    t_time = time.time()
    while 1:
        try:
            sock.send(("134").encode())
            break
        except Exception as e:
            if (time.time() - t_time > 420):
                print(e)
                return "*"

def get_list_byte(sock, i): #получает часть картинки читая заголовок а потом основную часть таймаут 420
    msg = ""
    t_time = time.time()
    time_a = time.time()
    while True:
        try:
            data = sock.recv(20)
            if (len(data) < 20):
                continue
            pos1 = data[0:10]
            pos0 = (pos1).decode('utf-8')
            pos = int(pos0)
            siz1 = data[10:20]
            siz0 = (siz1).decode('utf-8')
            siz = int(siz0)
            data = sock.recv(siz)
            if (time.time() - time_a > 5):
                time_a = time.time()
                if (send_accept(sock) == "*"):
                    return "*"
            if (len(data) + 20 < siz or pos != i):
                continue
        except Exception as e:
            if (time.time() - t_time > 420):
                print(e)
                return "*"
            continue
        if not data:
            break
        msg = data
        if (len(msg) > 0):
            break
    return msg



def get_pic(file_name,sock): #читает длину, получает  получает часть картинки от get_list_byte и пишет  в файл таймуат 420
    flag = 0
    temp = get_list_byte(sock, 0)
    if (temp == "*"):
        return "*"
    size = int(temp)
    if flag:
        print(time.time())
    t_time = time.time()
    while 1:
        try:
            sock.send(("134").encode())
            break
        except Exception as e:
            if (time.time() - t_time > 420):
                print(e)
                return "*"
    data = ""
    dwreadbuf = 0
    stdout = open(file_name, "wb")
    iter = 0
    i = 0
    while (dwreadbuf < size):
        data = "*"
        while (data == "*"):
            data = get_list_byte(sock, dwreadbuf)
            if (iter > 100000):
                stdout.close()
                return "*"
            if (data == "*"):
                stdout.close()
                return "*"
            iter += 1
        i += 1
        stdout.write(data)
        dwreadbuf += len(data)
        if (send_accept(sock) == "*"):
            stdout.close()
            return "*"
    stdout.close()
    if flag:
        print(time.time())

