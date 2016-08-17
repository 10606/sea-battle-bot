# -*- coding: utf-8 -*-
import atexit
import sys, time, math, random, threading ## pygame
from request import *
from check_field import *
from drawing import *
from resourse import *
from send_pic_to_client import *
import requests, sys,time,json, urllib, vk
from urllib import *
import subprocess
import os, atexit
from atexit import *
my_index = 0
empty = 0

def main ():
    to_draw1 = [[0] * 10 for x in range(10)]
    to_draw2 = [[0] * 10 for x in range(10)]
    
    field1 = [[0] * 10 for x in range(10)]
    field2 = [[0] * 10 for x in range(10)]

    fieldreq1 = [[0] * 10 for x in range(10)]
    fieldreq2 = [[0] * 10 for x in range(10)]

    sdout = ""
    global my_index
    global empty
    iindex = my_index
    init_sock(2, iindex)
    empty = 1
    print(iindex)
    gg = 0
    name = ["", ""]
    #получение и проверка поля бота 1
    name[0] = get_from_client(iindex + 0)
    send_answer_sock(iindex + 0, "здравствуйте, " + name[0])
    sdout += ("client " + str(iindex + 0) + ": " + name[0] + "\n")
    print("client " + str(iindex + 0) + ": " + name[0], "\n")
    flag1 = 0
    while (flag1 == 0):
        temp1 = get_request_sock(iindex + 0)
        if (temp1 == "*"):
            send_answer_sock(iindex + 1, "Победа")
            print("player ", iindex + 0, " not ask")
            stdout = open('result.txt', 'a')  ###
            stdout.write(sdout)
            stdout.write(name[0] + "  :  " + name[1] + "\n")
            stdout.write(name[0] + "  disconnect" + "\n" + "\n")
            stdout.close()
            return
        print(temp1)
        counter = 0
        for i in range(len(temp1)):
            if (counter >= 100):
                break
            if (temp1[i] == '0'):
                field1[counter // 10][counter % 10] = 0
                counter += 1

            if (temp1[i] == '1'):
                field1[counter // 10][counter % 10] = 1
                counter += 1
        flag1 = check_field(field1)
        if (flag1 == 0):
            if (send_answer_sock(iindex + 0, "0") == "*"):
                send_answer_sock(iindex + 1, "Победа")
                stdout = open('result.txt', 'a')  ###
                stdout.write(sdout)
                stdout.write(name[0] + "  :  " + name[1] + "\n")
                stdout.write(name[0] + "  disconnect" + "\n" + "\n")
                stdout.close()
                return
        if (flag1 == 1):
            firstmsgbot[0] = 0
            if (send_answer_sock(iindex + 0, "1") == "*"):
                send_answer_sock(iindex + 1, "Победа")
                stdout = open('result.txt', 'a')  ###
                stdout.write(sdout)
                stdout.write(name[0] + "  :  " + name[1] + "\n")
                stdout.write(name[0] + "  disconnect" + "\n" + "\n")
                stdout.close()
                return
    sdout += ("field client " + str(iindex + 0) + ": " + "\n")
    for i in range(10):
        for j in range (10):
            if (j == 9):
                sdout += (str(field1[i][j]) + '\n')
            else:
                sdout += (str(field1[i][j]) + ' ')
    #получение и проверка поля бота 2
    name[1] = get_from_client(iindex + 1)
    send_answer_sock(iindex + 1, "здравствуйте, " + name[1])
    sdout += ("client " + str(iindex + 1) + ": " + name[1] + "\n")
    print("client " + str(iindex + 1) + ": " + name[1], "\n")
    flag2 = 0
    while (flag2 == 0):
        temp2 = get_request_sock(iindex + 1)
        if (temp2 == "*"):
            send_answer_sock(iindex + 0, "Победа")
            print("player ", iindex + 1, " not ask")
            stdout = open('result.txt', 'a')  ###
            stdout.write(sdout)
            stdout.write(name[0] + "  :  " + name[1] + "\n")
            stdout.write(name[1] + "  disconnect" + "\n" + "\n")
            stdout.close()
            return
        print(temp2)
        counter = 0
        for i in range(len(temp2)):
            if (counter >= 100):
                break
            if (temp2[i] == '0'):
                field2[counter // 10][counter % 10] = 0
                counter += 1

            if (temp2[i] == '1'):
                field2[counter // 10][counter % 10] = 1
                counter += 1
        flag2 = check_field(field2)
        if (flag2 == 0):
            if (send_answer_sock(iindex + 1, "0") == "*"):
                send_answer_sock(iindex + 0, "Победа")
                stdout = open('result.txt', 'a')  ###
                stdout.write(sdout)
                stdout.write(name[0] + "  :  " + name[1] + "\n")
                stdout.write(name[1] + "  disconnect" + "\n" + "\n")
                stdout.close()
                return

        if (flag2 == 1):
            firstmsgbot[1] = 0
            if (send_answer_sock(iindex + 1, "1") == "*"):
                send_answer_sock(iindex + 0, "Победа")
                stdout = open('result.txt', 'a')  ###
                stdout.write(sdout)
                stdout.write(name[0] + "  :  " + name[1] + "\n")
                stdout.write(name[1] + "  disconnect" + "\n" + "\n")
                stdout.close()
                return

    sdout += ("field client " + str(iindex + 1) + ": " + "\n")
    for i in range(10):
        for j in range (10):
            if (j == 9):
                sdout += (str(field2[i][j]) + '\n')
            else:
                sdout += (str(field2[i][j]) + ' ')
    for i in range(10):
        for j in range(10):
            if field1[i][j] > 0:
                to_draw1[i][j] = 2
            if field2[i][j] > 0:
                to_draw2[i][j] = 2
    ship1 = 10
    ship2 = 10
    player_queue = 1
    iter_ = 0
    shots=[]
    while (ship1 * ship2 > 0 and iter_ < max_iter): #процесс ответа на запросы
        if (player_queue == 1): #очередь игрока 1
            while True:
                temp1 = get_request_sock(iindex + 0)
                if (temp1 == "*"):
                    send_answer_sock(iindex + 1, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[0] + "  disconnect" + "\n" + "\n")
                    stdout.close()

                    draw(to_draw2, to_draw1, iindex)
                    print('ready send picture to client2 ', iindex + 1)
                    send_pic('ready' + str(iindex) + '.jpg', iindex + 1)
                    print('send picture to client2 ', iindex + 1)

                    return
                temp_coord = get_coordinate(temp1)
                if fieldreq2[temp_coord[0] - 1][temp_coord[1] - 1] < 1:
                    break
                else:
                    gg += 1
                    if (send_answer_sock(iindex + 0, used[gg % len(used)]) == "*"):
                        send_answer_sock(iindex + 1, "Победа")
                        stdout = open('result.txt', 'a')  ###
                        stdout.write(sdout)
                        stdout.write(name[0] + "  :  " + name[1] + "\n")
                        stdout.write(name[0] + "  disconnect" + "\n" + "\n")
                        stdout.close()

                        draw(to_draw2, to_draw1, iindex)
                        print('ready send picture to client2 ', iindex + 1)
                        send_pic('ready' + str(iindex) + '.jpg', iindex + 1)
                        print('send picture to client2 ', iindex + 1)

                        return
            ans = check_request(field2, temp_coord[0] - 1, temp_coord[1] - 1)
            number=(temp_coord[0]-1)*10 + temp_coord[1] - 1
            fieldreq2[temp_coord[0] - 1][temp_coord[1] - 1] = 1
            if (ans == 0):
                to_draw2[temp_coord[0] - 1][temp_coord[1] - 1] = 1
                gg += 1
                if (send_answer_sock(iindex + 0, mimo[gg%(len(mimo))]) == "*"):
                    send_answer_sock(iindex + 1, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[0] + "  disconnect" + "\n" + "\n")
                    stdout.close()

                    draw(to_draw2, to_draw1, iindex)
                    print('ready send picture to client2 ', iindex + 1)
                    send_pic('ready' + str(iindex) + '.jpg', iindex + 1)
                    print('send picture to client2 ', iindex + 1)

                    return

                player_queue = 2
            elif (ans == 1):
                to_draw2[temp_coord[0] - 1][temp_coord[1] - 1] = 3
                gg += 1
                if (send_answer_sock(iindex + 0, ranen[gg%(len(ranen))]) == "*"):
                    send_answer_sock(iindex + 1, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[0] + "  disconnect" + "\n" + "\n")
                    stdout.close()

                    draw(to_draw2, to_draw1, iindex)
                    print('ready send picture to client2 ', iindex + 1)
                    send_pic('ready' + str(iindex) + '.jpg', iindex + 1)
                    print('send picture to client2 ', iindex + 1)

                    return

            elif (ans == 2):
                to_draw2[temp_coord[0] - 1][temp_coord[1] - 1] = 4
                to_draw2 = ch(to_draw2, temp_coord[0] - 1, temp_coord[1] - 1)
                gg += 1
                if (send_answer_sock(iindex + 0, ubit[gg%(len(ubit))]) == "*"):
                    send_answer_sock(iindex + 1, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[0] + "  disconnect" + "\n" + "\n")
                    stdout.close()

                    draw(to_draw2, to_draw1, iindex)
                    print('ready send picture to client2 ', iindex + 1)
                    send_pic('ready' + str(iindex) + '.jpg', iindex + 1)
                    print('send picture to client2 ', iindex + 1)

                    return

                ship2 -= 1

        elif (player_queue == 2): #очередь игрока 2
            while True:
                temp2 = get_request_sock(iindex + 1)
                if (temp2 == "*"):
                    send_answer_sock(iindex + 0, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[1] + "  disconnect" + "\n" + "\n")
                    stdout.close()

                    draw(to_draw1, to_draw2, iindex)
                    print('ready send picture to client2 ', iindex)
                    send_pic('ready' + str(iindex) + '.jpg', iindex + 0)
                    print('send picture to client2 ', iindex)

                    return
                temp_coord = get_coordinate(temp2)
                if fieldreq1[temp_coord[0] - 1][temp_coord[1] - 1] < 1:
                    break
                else:
                    gg += 1
                    if (send_answer_sock(iindex + 1, used[gg % len(used)]) == "*"):
                        send_answer_sock(iindex + 0, "Победа")
                        stdout = open('result.txt', 'a')  ###
                        stdout.write(sdout)
                        stdout.write(name[0] + "  :  " + name[1] + "\n")
                        stdout.write(name[1] + "  disconnect" + "\n" + "\n")
                        stdout.close()

                        draw(to_draw1, to_draw2, iindex)
                        print('ready send picture to client2 ', iindex)
                        send_pic('ready' + str(iindex) + '.jpg', iindex + 0)
                        print('send picture to client2 ', iindex)

                        return
            ans = check_request(field1, temp_coord[0] - 1, temp_coord[1] - 1)
            number=(temp_coord[0]-1)*10 + temp_coord[1] - 1
            fieldreq1[temp_coord[0] - 1][temp_coord[1] - 1] = 1
            if (ans == 0):
                to_draw1[temp_coord[0] - 1][temp_coord[1] - 1] = 1
                gg += 1
                if (send_answer_sock(iindex + 1, mimo[gg%(len(mimo))]) == "*"):
                    send_answer_sock(iindex + 0, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[1] + "  disconnect" + "\n" + "\n")
                    stdout.close()

                    draw(to_draw1, to_draw2, iindex)
                    print('ready send picture to client2 ', iindex)
                    send_pic('ready' + str(iindex) + '.jpg', iindex + 0)
                    print('send picture to client2 ', iindex)

                    return

                player_queue = 1
            elif (ans == 1):
                to_draw1[temp_coord[0] - 1][temp_coord[1] - 1] = 3
                gg += 1
                if (send_answer_sock(iindex + 1, ranen[gg%(len(ranen))]) == "*"):
                    send_answer_sock(iindex + 0, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[1] + "  disconnect" + "\n" + "\n")
                    stdout.close()

                    draw(to_draw1, to_draw2, iindex)
                    print('ready send picture to client2 ', iindex)
                    send_pic('ready' + str(iindex) + '.jpg', iindex + 0)
                    print('send picture to client2 ', iindex)

                    return

            elif (ans == 2):
                to_draw1[temp_coord[0] - 1][temp_coord[1] - 1] = 4
                to_draw1 = ch(to_draw1, temp_coord[0] - 1, temp_coord[1] - 1)
                gg += 1
                if (send_answer_sock(iindex + 1, ubit[gg%(len(ubit))]) == "*"):
                    send_answer_sock(iindex + 0, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[1] + "  disconnect" + "\n" + "\n")
                    stdout.close()

                    draw(to_draw1, to_draw2, iindex)
                    print('ready send picture to client2 ', iindex)
                    send_pic('ready' + str(iindex) + '.jpg', iindex + 0)
                    print('send picture to client2 ', iindex)

                    return
                ship1 -= 1
        iter_ += 1
    #time.sleep(3)
    if (ship1 == 0):
        stdout = open('result.txt', 'a')  ###
        stdout.write(sdout)
        stdout.write(name[0] + "  :  " + name[1] + "\n")
        stdout.write(name[1] + "  win" + "\n" + "\n")
        stdout.close()
        send_answer_sock(iindex + 0, "Поражение")
        draw(to_draw1, to_draw2, iindex)
        print('ready send picture to client1 ', iindex)
        send_pic('ready' + str(iindex) + '.jpg',iindex+0)
        print('send picture to client1 ', iindex)
        send_answer_sock(iindex + 1, "Победа")
        draw(to_draw2, to_draw1, iindex)
        print('ready send picture to client1 ', iindex + 1)
        send_pic('ready' + str(iindex) + '.jpg',iindex+1)
        print('send picture to client1 ', iindex + 1)
    else:
        stdout = open('result.txt', 'a')  ###
        stdout.write(sdout)
        stdout.write(name[0] + "  :  " + name[1] + "\n")
        stdout.write(name[0] + "  win" + "\n" + "\n")
        stdout.close()
        send_answer_sock(iindex + 1, "Поражение")
        draw(to_draw2, to_draw1, iindex)
        print('ready send picture to client2 ', iindex + 1)
        send_pic('ready' + str(iindex) + '.jpg',iindex+1)
        print('send picture to client2 ', iindex + 1)
        send_answer_sock(iindex + 0, "Победа")
        draw(to_draw1, to_draw2, iindex)
        print('ready send picture to client2 ', iindex)
        send_pic('ready' + str(iindex) + '.jpg',iindex+0)
        print('send picture to client2 ', iindex)


t = []

cmd1 = 'python add_adr_start.py'
cmd2 = 'python del_adr_exit.py'

def nOnExit():
    print('pop address')
    subprocess.Popen(cmd2)
    return None

print('push address')
atexit.register(nOnExit)


subprocess.Popen(cmd1)

def start_server_():
    global empty
    global my_index
    while (1):
        empty = 0
        t.append("")
        t[my_index // 2] = threading.Thread(target=main)
        temp = 1
        while (threading.activeCount() > 10):
            time.sleep(1)
            temp += 1
        t[my_index // 2].start()
        # main()
        temp = 1
        while (empty == 0):
            time.sleep(1)
            temp += 1
        empty = 0
        my_index += 2

try:
    start_server_()
#except KeyboardInterrupt or SystemExit:
except KeyboardInterrupt or SystemExit:
    print("exit")
    nOnExit()
    sys.exit(0)
    #gg = input()
except Exception as e:
    new_ip_file = open('out.txt', 'a')
    new_ip_file.write(str(e))
    new_ip_file.close()

sys.exit(0)
