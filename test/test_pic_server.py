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
#conn[i + iindex].setblocking(0)
send = ""



#send = "<html>\n<body>\n<div>" + send
#send += "</div>\n</body>\n</html>"

#print("[" + send + "]")
def send_pic(file_name):
    sin=open(file_name,'rb')###
    send = sin.read()
    sin.close()
    def send_to_client(msg):
        conn[0].send(str(len(msg)).encode())
        data = conn[0].recv(10000)
        while 1:
            try:
                conn[0].send(msg)
                #print("send ", msg, " client ")
                break
            except Exception as e:
                print(e, " send")

    send_to_client(send)


send_pic('captureqwsx.bmp')