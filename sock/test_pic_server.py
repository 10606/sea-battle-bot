import sys, time, math, random
import socket

sock = socket.socket()
#sock = socket()

#sin=open('port.txt','r')###
#portc = int(sin.read())
#sin.close()

sock.bind(("", 13451))
sock.listen(100)
conn = []
addr  = []
conn.append(0)
addr.append(0)
conn[0], addr[0] = sock.accept()
print ('connected:', addr[0])
conn[0].setblocking(0)
send = ""



#send = "<html>\n<body>\n<div>" + send
#send += "</div>\n</body>\n</html>"

#print("[" + send + "]")'


def send_to_client(msg, index):
    t_time = time.time()
    while 1:
        try:
            #print("send")
            conn[index].send(str(len(msg)).encode())
            break
        except Exception as e:
            if (time.time() - t_time > 60):
                print(e)
                return "*"

    t_time = time.time()
    while 1:
        try:
            #print("get")
            data = conn[index].recv(10000)
            break
        except Exception as e:
            if (time.time() - t_time > 60):
                print(e)
                return "*"

    t_time = time.time()
    while 1:
        try:
            #print("send")
            conn[index].send(msg)
            # print("send ", msg, " client ")
            break
        except Exception as e:
            if (time.time() - t_time > 60):
                print(e)
                return "*"

def send_pic(file_name, index):
    sin=open(file_name,'rb')###
    send = sin.read()
    sin.close()
    if (send_to_client(send, index) == "*"):
        return "*"


#send_pic('captureqwsx.bmp')
send_pic('background1.jpg', 0)
