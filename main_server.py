# -*- coding: utf-8 -*-
import sys, time, math, random, vk
from request import *
from check_field import *
from contacts import *
from drawing import *
from check_okrest import *
py_flag=1
if py_flag:
    from frontend import *
    import pygame
    
# создание полей
field1 = [[0]*10 for x in range(10)]
field2 = [[0]*10 for x in range(10)]
bot_field=[[0]*12 for x in range(12)]
res_field1=[[0]*10 for x in range(10)]
res_field2=[[0]*10 for x in range(10)]
def get_letter(a,b):
    letter = 'ABCDEFGHIJ'
    numb=['1','2','3','4','5','6','7','8','9','10']
    return (letter[b]+numb[a])

#вспомогательные функции
# поиск всех возможных кораблей длины length на поле field
def get_ships(length, field):
    ships = []
    for i in range(1, 11):
        for j in range(1, 12 - length):
            coordinate = []
            good = True
            for k in range(j, j + length):
                if field[i][k] != 0:
                    good = False
                    break
                else:
                    coordinate.append([i, k])
            if good:
                ships.append(coordinate)
    for i in range(1, 12 - length):
        for j in range(1, 11):
            coordinate = []
            good = True
            for k in range(i, i + length):
                if field[k][j] != 0:
                    good = False
                    break
                else:
                    coordinate.append([k, j])
            if good:
                ships.append(coordinate)
    return ships

#приведение поля к типу 10х10
def change_field(field):
    new_field=[[0]*10 for i in range(10)]
    for i in range(1,11):
        for j in range(1,11):
            if field[i][j]>0:
                new_field[i-1][j-1]=1
            else:
                new_field[i-1][j-1]=0
    return(new_field)

# создание поля с нуля
def make_field():
    while True:
        ready = False
        field = [[0 for i in range(12)]
                 for j in range(12)]
        for i in range(12):
            field[11][i] = -1
            field[0][i] = -1
            field[i][11] = -1
            field[i][0] = -1
        boats = [0, 4, 3, 2, 1]
        now_ship = 4
        while True:
            ships = get_ships(now_ship, field)
            if len(ships) == 0:
                break
            else:
                rnd = random.randint(0, len(ships) - 1)
                current_ship = ships[rnd]
                for i in range(now_ship):
                    x = current_ship[i][0]
                    y = current_ship[i][1]
                    field[x][y] = -1
                    field[x + 1][y] = -1
                    field[x][y + 1] = -1
                    field[x - 1][y] = -1
                    field[x][y - 1] = -1
                    field[x + 1][y + 1] = -1
                    field[x - 1][y - 1] = -1
                    field[x + 1][y - 1] = -1
                    field[x - 1][y + 1] = -1
                for i in range(now_ship):
                    x = current_ship[i][0]
                    y = current_ship[i][1]
                    field[x][y] = now_ship
                boats[now_ship] -= 1
                if boats[now_ship] == 0:
                    now_ship -= 1
                    if now_ship == 0:
                        if 59<=check_okr(change_field(field))<=61:
                            ready = True
                        break
        if ready:
            return field
msg='Здравствуйте! Коротко о формате игры:\n Игра идет по стандартным правилам морского боя. Для начала игры отправьте серверу поле в формате 10х10, состоящее из 0 и 1. 1 означает, что в этой клетке находится корабль, 0 - нет. Для вашего удобства вам будут предоставлены 5 случайно сгенерированных полей, которые достаточно просто скопировать.\n Формат выстрела: <Заглавная латинская буква от A до J><число от 1 до 10> (например, J5). Бот игнорирует любые сообщения, отправленные не в описанном формате. Выстрел можно совершать только после соответствующей команды сервера.\n Все вопросы задавайте мне (vk.com/id22346494).\n Подробнее с правилами игры вы сможете ознакомиться, введя "Правила" (без кавычек).\n Если вам нужна помощь, введите "Помощь" (без кавычек)'
send_answer(id_bot2,msg)      
msg='Для начала игры скопируйте одно из следующих полей и отправьте его боту\n\n'
msg+=' 0 означает отсутствие корабля в клетке, а 1 - его наличие\n\n'
for i in range(5):
    nf=change_field(make_field())
    for i in range(10):
        for j in range(10):
            msg+=str(nf[i][j])+' '
        msg+='\n'
    msg+='\n'
msg+='Вы также можете самостоятельно ввести поле в этом же формате.\n Для получения помощи напишите "Помощь" (без кавычек). \n Удачи!'
send_answer(id_bot2,msg)
print('send')
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
used = ['Вы уже стреляли сюда','Bы уже стреляли сюда','Вы ужe стреляли сюда','Вы уже cтреляли сюда',
        'Вы уже стрeляли сюда','Вы уже стреляли cюда','Вы уже стреляли сюдa']
gg=0
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

def main ():
    global gg
    global user_field
    #получение и проверка поля бота 1
    flag1 = 0
    while (flag1 == 0):
        temp1 = get_request(id_bot1)
        print(temp1)
        counter = 0
        for i in range(len(temp1)):
            if (counter >= 100):
                break
            if (temp1[i] == '0'):
                field1[counter // 10][counter % 10] = 0
                res_field1[counter // 10][counter % 10] = 0
                counter += 1
                

            if (temp1[i] == '1'):
                field1[counter // 10][counter % 10] = 1
                res_field1[counter // 10][counter % 10] = 10
                counter += 1
                
        flag1 = check_field(field1)
        if (flag1 == 0):
            send_answer(id_bot1, "0")
        if (flag1 == 1):
            firstmsgbot[0] = 0
            send_answer(id_bot1, "1")
    if py_flag:
        field_1(field1)
    #получение и проверка поля бота
    flag2 = 0
    while (flag2 == 0):
        temp2 = get_request(id_bot2)
        print(temp2)
        counter = 0
        for i in range(len(temp2)):
            if (counter >= 100):
                break;
            if (temp2[i] == '0'):
                field2[counter // 10][counter % 10] = 0
                res_field2[counter // 10][counter % 10] = 0
                counter += 1
                

            if (temp2[i] == '1'):
                field2[counter // 10][counter % 10] = 1
                res_field2[counter // 10][counter % 10] = 10
                counter += 1
                
        flag2 = check_field(field2)
        if (flag2 == 0):
            send_answer(id_bot2, 'Поле не соответствует правилам игры. Чтобы посмотреть правила игры, введите "Правила" (без кавычек).')
        if (flag2 == 1):
            firstmsgbot[1] = 0
            send_answer(id_bot2, "Поле принято")
    if py_flag:
        field_2(field2)
    ship1 = 10
    ship2 = 10
    player_queue = 1
    iter_ = 0
    shots=[]
    msg=''
    while (ship1 * ship2 > 0 and iter_ < max_iter): #процесс ответа на запросы
        #print('here')
        if (player_queue == 1): #очередь игрока 1
            while True:
                #print('get_request')
                temp1 = get_request(id_bot1)
                #print('get_coordinate')
                temp_coord = get_coordinate(temp1)
                #print('check_request')
                ans = check_request(field2, temp_coord[0] - 1, temp_coord[1] - 1)
                number=(temp_coord[0]-1)*10 + temp_coord[1] - 1
                x,y=temp_coord[0]-1,temp_coord[1]-1
                if user_field[x][y]==0:
                    break
                else:
                    gg+=1
                    send_answer(id_bot1,used[gg%len(used)])
            msg+='Соперник выстрелил '+get_letter(x,y)+' и '
            #print('send_answer')
            if (ans == 0):
                if py_flag:
                    shots.append(Sprite(pict_2[number].x,pict_2[number].y,pict_size,0,
                                   picture_beside))
                    miss.play()
                user_field[x][y]=-1
                res_field2[x][y] = -1
                send_answer(id_bot1, get_tue_ans("Промах"))
                msg+='промазал\n'
                player_queue = 2
            elif (ans == 1):
                if py_flag:
                    shots.append(Sprite(pict_2[number].x,pict_2[number].y,pict_size,0,
                                   picture_hit))
                    wound.play()
                send_answer(id_bot1, get_tue_ans("Ранение"))
                msg+='ранил ваш корабль\n'
                res_field2[x][y] = 1
                user_field[x][y]=1
            elif (ans == 2):
                if py_flag:
                    shots.append(Sprite(pict_2[number].x,pict_2[number].y,pict_size,0,
                                   picture_hit))
                    kill.play()
                user_field[x][y]=2
                res_field2[x][y] = 2
                for k in range(x+1,10):
                    if user_field[k][y]==1:
                        user_field[k][y]=2
                        res_field2[k][y] = 2
                    else:
                        break
                for k in range(x-1,-1,-1):
                    if user_field[k][y]==1:
                        user_field[k][y]=2
                        res_field2[k][y] = 2
                    else:
                        break
                for k in range(y+1,10):
                    if user_field[x][k]==1:
                        user_field[x][k]=2
                        res_field2[x][k] = 2
                    else:
                        break
                for k in range(y-1,-1,-1):
                    if user_field[x][k]==1:
                        user_field[x][k]=2
                        res_field2[x][k] = 2
                    else:
                        break
                send_answer(id_bot1, get_tue_ans("Убит"))
                msg+='потопил ваш корабль\n'
                ship2 -= 1

        elif (player_queue == 2): #очередь игрока 2
            msg+='Ваш ход. Чтобы посмотреть свое поле, введите "Мое поле" (без кавычек)\n Поле соперника выглядит так:'
            draw_the_field(bot_field, id_bot2, msg)
            msg=''
            while True:
                #print('get_request')
                temp2 = get_request(id_bot2)
                #print('get_coordinate')
                temp_coord = get_coordinate(temp2)
                #print('check_request')
                ans = check_request(field1, temp_coord[0] - 1, temp_coord[1] - 1)
                number=(temp_coord[0]-1)*10 + temp_coord[1] - 1
                x,y=temp_coord[0]-1,temp_coord[1]-1
                if bot_field[x][y]==0:
                    break
                else:
                    gg+=1
                    send_answer(id_bot2,used[gg%len(used)])
            #print('send_answer')
            if (ans == 0):
                if py_flag:
                    shots.append(Sprite(pict_1[number].x,pict_1[number].y,pict_size,0,
                                   picture_beside))
                    miss.play()
                bot_field[x][y]=-1
                res_field1[x][y] = -1
                send_answer(id_bot2, get_tue_ans("Промах"))
                player_queue = 1
            elif (ans == 1):
                if py_flag:
                    shots.append(Sprite(pict_1[number].x,pict_1[number].y,pict_size,0,
                                   picture_hit))
                    wound.play()
                bot_field[x][y]=1
                res_field1[x][y] = 1
                send_answer(id_bot2, get_tue_ans("Ранение"))
            elif (ans == 2):
                if py_flag:
                    shots.append(Sprite(pict_1[number].x,pict_1[number].y,pict_size,0,
                                   picture_hit))
                    kill.play()
                bot_field[x][y]=2
                res_field1[x][y] = 2
                for k in range(x+1,10):
                    if bot_field[k][y]==1:
                        bot_field[k][y]=2
                        res_field1[k][y] = 2
                    else:
                        break
                for k in range(x-1,-1,-1):
                    if bot_field[k][y]==1:
                        bot_field[k][y]=2
                        res_field1[k][y] = 2
                    else:
                        break
                for k in range(y+1,10):
                    if bot_field[x][k]==1:
                        bot_field[x][k]=2
                        res_field1[x][k] = 2
                    else:
                        break
                for k in range(y-1,-1,-1):
                    if bot_field[x][k]==1:
                        bot_field[x][k]=2
                        res_field1[x][k] = 2
                    else:
                        break
                send_answer(id_bot2, get_tue_ans("Убит"))
                ship1 -= 1
        iter_ += 1
        if py_flag:
            shots[-1].render()
            window.blit(screen,(0,0))
            pygame.display.flip()
    time.sleep(3)
    get_result(res_field1,res_field2, id_bot2)
    if (ship1 == 0):
        send_answer(id_bot1, "Поражение")
        send_answer(id_bot2, "Победа")
    else:
        send_answer(id_bot2, "Поражение")
        send_answer(id_bot1, "Победа")
main()
