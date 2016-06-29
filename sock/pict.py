import sys, time, math,random
import socket
def get_list_byte(sock, i):
    msg = ""
    t_time = time.time()
    while True:
        try:
            data = sock.recv(100000)
        except Exception as e:
            if (time.time() - t_time > 60):
                print(e)
                return "*"
            #print(e)
            continue
        if not data:
            break
        #print(data)
        msg = data#.decode('utf-8')
        #print(msg)
        if (len(msg) > 0):
            break
    return msg

def get_pic(file_name,sock):
    #time.sleep(5)
    flag = 0
    temp = get_list_byte(sock, 0)
    if (temp == "*"):
        return "*"
    size = int(temp)
    #print(size)
    if flag:
        print(time.time())
    t_time = time.time()
    while 1:
        try:
            sock.send(("134").encode())
            break
        except Exception as e:
            if (time.time() - t_time > 60):
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
            data = get_list_byte(sock, i)
            if (iter > 100000):
                stdout.close()
                return "*"
            iter += 1
        i += 1
        stdout.write(data)
        dwreadbuf += len(data)
        t_time = time.time()
        while 1:
            try:
                sock.send(("134").encode())
                break
            except Exception as e:
                if (time.time() - t_time > 60):
                    print(e)
                    stdout.close()
                    return "*"
    stdout.close()
    if flag:
        print(time.time())

#get_pic("get.bmp")
#s = input()
