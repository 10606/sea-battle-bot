﻿# -*- coding: utf-8 -*-
import sys, time, math, random, threading ## pygame
from request import *
from check_field import *
from contacts_sock import *
py_flag=0

if py_flag:
    from frontend import *
# создание полей

max_iter = 1000 #лимит количества ходов
def get_coordinate(msg):
    letter = 'ABCDEFGHIJ'
    return [int(msg[1:]), letter.index(msg[0])+1]

mimo = ['Прoмаx','Прoмах','Прoмax','Прoмaх','Промаx','Промах','Промax','Промaх',
        'Пpoмаx','Пpoмах','Пpoмax','Пpoмaх','Пpомаx',
        'Пpомах','Пpомax','Пpомaх']
ranen = ['Paнeниe','Paнeние','Paнениe','Paнение','Pанeниe','Pанeние',
         'Pанениe','Pанение','Рaнeниe','Рaнeние','Рaнениe',
         'Рaнение','Ранeниe','Ранeние','Ранениe','Ранение']
ubit = ['Убит','убит','Убил','убил']
used = ['Вы уже стреляли сюда', 'Bы уже стреляли сюда', 'Вы ужe стреляли сюда', 'Вы уже cтреляли сюда',
        'Вы уже стрeляли сюда', 'Вы уже стреляли cюда', 'Вы уже стреляли сюдa']
'''
def get_tue_ans(msg):
    global gg
    gg+=1
    if (msg in mimo):
        return mimo[gg%(len(mimo))]
    if (msg in ranen):
        return ranen[gg%(len(ranen))]
    if (msg in ubit):
        return ubit[gg%(len(ubit))]
    return msg
'''

my_index = 0
empty = 0

def main ():
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
    #sdout = open('result.txt', 'a')  ###
    sdout += ("client " + str(iindex + 0) + ": " + name[0] + "\n")
    #sdout.close()
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
            #acc = input()
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
    if py_flag:
        field_1(field1)
    #sdout = open('result.txt', 'a')  ###
    sdout += ("field client " + str(iindex + 0) + ": " + "\n")
    for i in range(10):
        for j in range (10):
            if (j == 9):
                sdout += (str(field1[i][j]) + '\n')
            else:
                sdout += (str(field1[i][j]) + ' ')
    #sdout.close()
    #получение и проверка поля бота 2
    name[1] = get_from_client(iindex + 1)
    send_answer_sock(iindex + 1, "здравствуйте, " + name[1])
    #sdout = open('result.txt', 'a')  ###
    sdout += ("client " + str(iindex + 1) + ": " + name[1] + "\n")
    #sdout.close()
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
            #acc = input()
            return
        print(temp2)
        counter = 0
        for i in range(len(temp2)):
            if (counter >= 100):
                break;
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

    if py_flag:
        field_2(field2)
    #sdout = open('result.txt', 'a')  ###
    sdout += ("field client " + str(iindex + 1) + ": " + "\n")
    for i in range(10):
        for j in range (10):
            if (j == 9):
                sdout += (str(field2[i][j]) + '\n')
            else:
                sdout += (str(field2[i][j]) + ' ')
    #sdout.close()

    ship1 = 10
    ship2 = 10
    player_queue = 1
    iter_ = 0
    shots=[]
    while (ship1 * ship2 > 0 and iter_ < max_iter): #процесс ответа на запросы
        #print('here')
        if (player_queue == 1): #очередь игрока 1
            while True:
                #print('get_request')
                temp1 = get_request_sock(iindex + 0)
                #time.sleep(30)
                if (temp1 == "*"):
                    send_answer_sock(iindex + 1, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[0] + "  disconnect" + "\n" + "\n")
                    stdout.close()
                    return
                #print('get_coordinate')
                temp_coord = get_coordinate(temp1)
                #print('check_request')
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
                        return
            ans = check_request(field2, temp_coord[0] - 1, temp_coord[1] - 1)
            number=(temp_coord[0]-1)*10 + temp_coord[1] - 1
            fieldreq2[temp_coord[0] - 1][temp_coord[1] - 1] = 1
            #print('send_answer')
            if (ans == 0):
                if py_flag:
                    shots.append(Sprite(pict_2[number].x,pict_2[number].y,pict_size,0,
                                   picture_beside))
                    miss.play()
                gg += 1
                if (send_answer_sock(iindex + 0, mimo[gg%(len(mimo))]) == "*"):
                    send_answer_sock(iindex + 1, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[0] + "  disconnect" + "\n" + "\n")
                    stdout.close()
                    return

                player_queue = 2
            elif (ans == 1):
                if py_flag:
                    shots.append(Sprite(pict_2[number].x,pict_2[number].y,pict_size,0,
                                   picture_hit))
                    wound.play()
                gg += 1
                if (send_answer_sock(iindex + 0, ranen[gg%(len(ranen))]) == "*"):
                    send_answer_sock(iindex + 1, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[0] + "  disconnect" + "\n" + "\n")
                    stdout.close()
                    return

            elif (ans == 2):
                if py_flag:
                    shots.append(Sprite(pict_2[number].x,pict_2[number].y,pict_size,0,
                                   picture_hit))
                    kill.play()
                gg += 1
                if (send_answer_sock(iindex + 0, ubit[gg%(len(ubit))]) == "*"):
                    send_answer_sock(iindex + 1, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[0] + "  disconnect" + "\n" + "\n")
                    stdout.close()
                    return

                ship2 -= 1

        elif (player_queue == 2): #очередь игрока 2
            while True:
                #print('get_request')
                temp2 = get_request_sock(iindex + 1)
                #time.sleep(30)
                if (temp2 == "*"):
                    send_answer_sock(iindex + 0, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[1] + "  disconnect" + "\n" + "\n")
                    stdout.close()
                    return
                #print('get_coordinate')
                temp_coord = get_coordinate(temp2)
                #print('check_request')
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
                        return
            ans = check_request(field1, temp_coord[0] - 1, temp_coord[1] - 1)
            number=(temp_coord[0]-1)*10 + temp_coord[1] - 1
            fieldreq1[temp_coord[0] - 1][temp_coord[1] - 1] = 1
            #print('send_answer')
            if (ans == 0):
                if py_flag:
                    shots.append(Sprite(pict_1[number].x,pict_1[number].y,pict_size,0,
                                   picture_beside))
                    miss.play()
                gg += 1
                if (send_answer_sock(iindex + 1, mimo[gg%(len(mimo))]) == "*"):
                    send_answer_sock(iindex + 0, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[1] + "  disconnect" + "\n" + "\n")
                    stdout.close()
                    return

                player_queue = 1
            elif (ans == 1):
                if py_flag:
                    shots.append(Sprite(pict_1[number].x,pict_1[number].y,pict_size,0,
                                   picture_hit))
                    wound.play()
                gg += 1
                if (send_answer_sock(iindex + 1, ranen[gg%(len(ranen))]) == "*"):
                    send_answer_sock(iindex + 0, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[1] + "  disconnect" + "\n" + "\n")
                    stdout.close()
                    return

            elif (ans == 2):
                if py_flag:
                    shots.append(Sprite(pict_1[number].x,pict_1[number].y,pict_size,0,
                                   picture_hit))
                    kill.play()
                gg += 1
                if (send_answer_sock(iindex + 1, ubit[gg%(len(ubit))]) == "*"):
                    send_answer_sock(iindex + 0, "Победа")
                    stdout = open('result.txt', 'a')  ###
                    stdout.write(sdout)
                    stdout.write(name[0] + "  :  " + name[1] + "\n")
                    stdout.write(name[1] + "  disconnect" + "\n" + "\n")
                    stdout.close()
                    return
                ship1 -= 1
        iter_ += 1
        if py_flag:
            shots[-1].render()
            window.blit(screen,(0,0))
            pygame.display.flip()
    #time.sleep(3)
    if (ship1 == 0):
        send_answer_sock(iindex + 0, "Поражение")
        send_answer_sock(iindex + 1, "Победа")
        stdout = open('result.txt', 'a')  ###
        stdout.write(sdout)
        stdout.write(name[0] + "  :  " + name[1] + "\n")
        stdout.write(name[1] + "  win" + "\n" + "\n")
        stdout.close()
    else:
        send_answer_sock(iindex + 1, "Поражение")
        send_answer_sock(iindex + 0, "Победа")
        stdout = open('result.txt', 'a')  ###
        stdout.write(sdout)
        stdout.write(name[0] + "  :  " + name[1] + "\n")
        stdout.write(name[0] + "  win" + "\n" + "\n")
        stdout.close()
#main()

t = []

while (1):
    empty = 0
    t.append("")
    t[my_index // 2] = threading.Thread(target=main)
    t[my_index // 2].start()
    #main()
    temp = 1
    while (empty == 0):
        time.sleep(1)
        temp += 1
    empty = 0
    my_index += 2

ss = input()