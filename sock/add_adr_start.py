import atexit
import requests, sys,time,json, urllib, vk
from urllib import *
import threading, os, atexit
from group_edit import *

unique_text = " Список работающих серверов:"
unique_text2 = " Нет доступных серверов. "
url='http://ip-address.ru/'
time_t = time.time()
page = ""


token = ""
bo = ""
bot1 = ""
bot2 = ""
captcha = ""
id_bot1 = ""
def loginn_():
    global token
    global bo
    global bot1
    global bot2
    global captcha
    global id_bot1
    stdin1=open('token_server.txt','r')
    token1=stdin1.read()
    token += token1
    stdin1.close()
    stdin1=open('group.txt','r')
    bo1=stdin1.read()
    bo += bo1
    id_bot1 += bo
    stdin1.close()
    stdin1=open('capt_chat.txt','r')
    bot2=stdin1.read()
    bot1 += bot2
    stdin1.close()
    stdin1=open('token_captcha.txt','r')
    captcha1=stdin1.read()
    captcha += captcha1
    stdin1.close()
    return 51


gg = login_()
gg = loginn_()

def norm(msg):
    i = 0
    while (i < len(msg) - 1):
        # print(i, len(msg))
        if (i >= len(msg) - 1):
            break
        if (msg[i] == ' ' and msg[i + 1] == ' '):
            # print(i)
            msg = msg[0: i] + msg[(i + 1): len(msg)]
        else:
            i += 1
    return msg

def add_adres(msg, ip):

    index0 = msg.find(unique_text2, 0, len(msg))
    if (index0 != -1):
        msg = msg[0:index0]
    msg = norm(msg)

    ip = ' ' + ip + ' '
    index1 = msg.find(unique_text, 0, len(msg))
    if (index1 == -1):
        msg += unique_text
    msg = norm(msg)
    index0 = msg.find(ip, 0, len(msg))
    if (index0 == -1):
        msg += ip
    msg = norm(msg)

    return msg


#atexit.register(nOnExit)
#atexit.unregister(nOnExit)


def added(ans):

    global id_bot1
    global token
    time_t = time.time()
    while (1):
        time.sleep(10)
        try:
            #token = "9f22a66f34a05311d98a0149884b75cdc051bb42127f5b68341668ec103fb4aaf2e7ab8050147904c1e95"
            session = vk.Session(access_token=token)
            api = vk.API(session)
            # print("gg")
            time.sleep(3)
            print(id_bot1)
            temp = api.groups.getById(group_ids=str(id_bot1), fields="description", version="5.51")
            #temp = api.groups.getById(group_ids="123404080", fields="description", version="5.51")
            # print(temp)

            time.sleep(3)
            answer = temp[0]['description']
            answer = ' ' + answer + ' '
            print(answer)

            answer = add_adres(answer, ans)
            #temp = api.groups.edit(group_id="123404080", description=answer, version="5.51")
            group_edit(id_bot1, answer)
            #print(temp)
            break
        except Exception as e:
            print(e)
            if (time.time() - time_t > 60):
                break


def get_adr_start():
    while 1:
        try:
            page = urllib.request.urlopen(url).read()
            page = page.decode('utf-8')
            index0 = page.find("Ваш IP адрес: ", 0, len(page) - 1) + len("Ваш IP адрес: ")
            index1 = page.find("      </b>", index0, len(page) - 1)
            # print(page)

            # print(type(page))

            # print(index0, index1)
            ans = page[index0: index1]
            print(ans)

            last_ip_file = open('server_IP.txt', 'r')
            last_ip = last_ip_file.read()
            last_ip_file.close()

            if (last_ip != ans):
                print("need")

                new_ip_file = open('server_IP.txt', 'w')
                new_ip_file.write(ans)
                new_ip_file.close()

                added(ans)

            else:
                print("not need")
                #break
                added(ans)
            break
        except Exception as e:
            if (time.time() - time_t > 60):
                print(e)
                break
        time.sleep(10)

get_adr_start()
