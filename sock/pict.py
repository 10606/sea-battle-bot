import sys, time, math,random
import socket


def get_null_string(gg):  # дописывает 0 в начало строки до длины 10
    gg = str(gg)
    k = 10 - len(gg)
    hh = '0' * k
    ss = hh + gg
    return ss

pac_accept = [0]
def send_accept(sock, msg): #отправляет подтвердение серверу что получен пакет
    t_time = time.time()
    msg1 = get_null_string(msg)
    while 1:
        try:
            sock.send((msg1).encode())
            break
        except Exception as e:
            if (time.time() - t_time > 420):
                print(e)
                return "*"

def get_list_byte(sock, i): #получает часть картинки читая заголовок а потом основную часть таймаут 420
    #print("сука блять нахуй работай")
    msg = ""
    t_time = time.time()
    time_a = time.time()
    pos = 0
    siz = 0
    '''
    get_one_byte = 0
    while 1:
        try:
            get_one_byte = sock.recv(1)
            get_one_byte = get_one_byte.decode('utf-8')
            get_one_byte = str(get_one_byte)
        except Exception as e:
            if (time.time() - t_time > 420):
                print(e)
                return "*"
        if ((str(get_one_byte) == "0") or (str(get_one_byte) == "9")):
            break
        print("get_one_byte ", get_one_byte, type(get_one_byte))
    '''
    while True:
        try:
            data = sock.recv(20)
            if (len(data) < 20):
                continue
            #print("data", data)
            pos1 = data[0:10]
            pos0 = (pos1).decode('utf-8')
            #pos0 = str(get_one_byte) + pos0
            #print("index pac", pos0)
            pos = int(pos0)
            siz1 = data[10:20]
            siz0 = (siz1).decode('utf-8')
            #print("size pac", siz0)
            siz = int(siz0)
            siz -= 20

            if (siz == 0):
                print(data, "get next list pac")
                return "+"
            data = b''
            while 1:
                try:
                    datas = sock.recv(siz)
                    #print("len datas", len(datas), " блять сука из ", siz)
                    siz -= len(datas)
                    data += datas
                    #print(data)
                    if (siz == 0):
                        break
                except Exception as e:
                    if (time.time() - t_time > 420):
                        print(e)
                        return "*"
                    continue
        except Exception as e:
            if (time.time() - t_time > 420):
                print(e)
                return "*"
            continue
        #print(data)
        msg = data
        if (len(msg) > 0):
            break
    #print(pos, "index")
    #if (pac_accept[pos] == ""):
    #    print("pac empty")
    #print(pac_accept[pos], "fill")
    pac_accept[pos] = msg
    return msg



def get_pic(file_name,sock): #читает длину, получает  получает часть картинки от get_list_byte и пишет  в файл таймуат 420
    pac_accept.clear()
    pac_accept.append("")
    flag = 0
    temp = get_list_byte(sock, 0)
    if (temp == "*"):
        return "*"
    pac_accept[0] = ""
    size = int(temp)
    if flag:
        print(time.time())
    t_time = time.time()
    if (send_accept(sock, 9999999999) == "*"):
        return "*"
    pac_accept.clear()
    for i in range(size):
        pac_accept.append("")
    data = ""
    dwreadbuf = 0
    stdout = open(file_name, "wb")
    iter = 0
    i = 0
    #while (dwreadbuf < size):
    while (pac_accept.count("") != 0):
        data = "*"
        while (data != "+"):
            data = get_list_byte(sock, dwreadbuf)
            if (pac_accept.count("") == 0):
                break
            if (iter > 100000):
                stdout.close()
                return "*"
            if (data == "*"):
                stdout.close()
                return "*"
            iter += 1
        data = "*"
        for j in range(len(pac_accept)):
            #print("type pac_accept[j] = ", type(pac_accept[j]), " j = ", j)
            if (pac_accept[j] == ""):
                #print(j, "getter")
                time.sleep(0.001)
                if (send_accept(sock, j) == "*"):
                    stdout.close()
                    return "*"
        #print(pac_accept.count(""), "сука нахуй заебал работай блять")
    if (send_accept(sock, 9999999999) == "*"):
        stdout.close()
        return "*"
    if (send_accept(sock, 9999999999) == "*"):
        stdout.close()
        return "*"
    for j in range(len(pac_accept)):
        stdout.write(pac_accept[j])
    stdout.close()
    if flag:
        print(time.time())

