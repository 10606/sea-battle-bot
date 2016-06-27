import sys, time, math,random
import socket


sock = socket.socket()
sock.connect(("5.19.254.166", 13451))
sock.setblocking(0)


def get_list_byte():
    msg = ""
    while True:
        try:
            data = sock.recv(100000)
        except Exception as e:
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
def get_pic(file_name):
    size = int(get_list_byte())
    #print(size)
    #print(time.time())
    sock.send(("134").encode())
    data = ""
    dwreadbuf = 0
    stdout = open(file_name, "wb")
    while (dwreadbuf < size):
        data = get_list_byte()
        stdout.write(data)
        dwreadbuf += len(data)

    stdout.close()

    #print(time.time())

get_pic("get.bmp")
#s = input()