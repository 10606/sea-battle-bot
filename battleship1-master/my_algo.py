# -*- coding: utf-8 -*-
#неоптимальный алгоритм для тестирования
import sys, time, math,random
import vk
from client_cerver import *
field=[[0]*12 for i in range(12)]
ships=[0,4,3,2,1]
wounds=[]
for i in range(12):
    field[0][i]=-1
    field[11][i]=-1
    field[i][0]=-1
    field[i][11]=-1
def make_shot_not_wound(field,wounds):
    want = 0
    for i in range(5):
        if ships[i]:
            want=i
    copy_field=[[0]*12 for i in range(12)]
    all_ships=get_ships(want, field)
    max_=0
    for ship in all_ships:
        for coor in ship:
            copy_field[coor[0]][coor[1]] += 1
            max_=max(max_,copy_field[coor[0]][coor[1]])
    best=[]
    for i in range(12):
        for j in range(12):
            if copy_field[i][j]==max_:
                best.append((i,j))
    rnd=random.randint(0,len(best)-1)
    return(best[rnd])

def make_shot_wound(field,wounds):
    wounds.sort()
    for k in range(len(wounds)):
        x,y=wounds[k][0],wounds[k][1]
        field[x][y]=0
    all_ships=[]
    for i in range(len(wounds)+1,5):
        boats=get_ships(i,field)
        for j in boats:
            ctr=0
            for k in range(len(wounds)):
                if [wounds[k][0],wounds[k][1]] in j:
                    ctr+=1
            if ctr==len(wounds):
                all_ships.append(j)
    for k in range(len(wounds)):
        x,y=wounds[k][0],wounds[k][1]
        field[x][y]=1
    copy_field=[[0]*12 for i in range(12)]
    max_=0
    for ship in all_ships:
        for coor in ship:
            if (coor[0],coor[1]) in wounds:
                continue
            flag=False
            for k in range(len(wounds)):
                x,y=wounds[k][0],wounds[k][1]
                if math.fabs(x-coor[0])+math.fabs(y-coor[1])==1:
                    flag=True
                    break
            if flag:        
                copy_field[coor[0]][coor[1]] += 1
                max_=max(max_,copy_field[coor[0]][coor[1]])
    best=[]
    if max_==0:
        print(all_ships)
    for i in range(12):
        for j in range(12):
            if copy_field[i][j]==max_:
                best.append((i,j))
    rnd=random.randint(0,len(best)-1)
    return(best[rnd])
                
def shooting_changing_not_wound(field,wounds):
    shoot=make_shot_not_wound(field,wounds)
    x=shoot[0]; y=shoot[1]
    ans=get_answer(x,y)
    if ans==-1:
        field[x][y]=-1
    elif ans==1:
        field[x][y]=1
        wounds.append((x,y))
        field[x+1][y+1]=-1
        field[x+1][y-1]=-1
        field[x-1][y+1]=-1
        field[x-1][y-1]=-1
    elif ans==2:
        field[x][y]=1
        field[x+1][y+1]=-1
        field[x+1][y-1]=-1
        field[x-1][y+1]=-1
        field[x-1][y-1]=-1
        field[x+1][y]=-1
        field[x-1][y]=-1
        field[x][y+1]=-1
        field[x][y-1]=-1
        ships[1]-=1
    return(field,wounds)

def shooting_changing_wound(field,wounds):
    shoot=make_shot_wound(field,wounds)
    x=shoot[0]; y=shoot[1]
    ans=get_answer(x,y)
    if ans==-1:
        field[x][y]=-1
    elif ans==1:
        field[x][y]=1
        wounds.append((x,y))
        field[x+1][y+1]=-1
        field[x+1][y-1]=-1
        field[x-1][y+1]=-1
        field[x-1][y-1]=-1
    elif ans==2:
        wounds.append((x,y))
        field[x+1][y+1]=-1
        field[x+1][y-1]=-1
        field[x-1][y+1]=-1
        field[x-1][y-1]=-1
        field[x+1][y]=-1
        field[x-1][y]=-1
        field[x][y+1]=-1
        field[x][y-1]=-1
        for i in range(len(wounds)-1):
            x,y=wounds[i][0],wounds[i][1]
            field[x+1][y]=-1
            field[x-1][y]=-1
            field[x][y+1]=-1
            field[x][y-1]=-1
        for i in range(len(wounds)):
            x,y=wounds[i][0],wounds[i][1]
            field[x][y]=1
        ships[len(wounds)]-=1
        wounds=[]
    return(field,wounds)
def game():
    global field, ships, wounds
    field=[[0]*12 for i in range(12)]
    ships=[0,4,3,2,1]
    wounds=[]
    for i in range(12):
        field[0][i]=-1
        field[11][i]=-1
        field[i][0]=-1
        field[i][11]=-1
    while True:
        print(wounds)
        if wounds:
            field,wounds=shooting_changing_wound(field,wounds)
        else:
            field,wounds=shooting_changing_not_wound(field,wounds)
