import sys, time, math,random
import vk
from client_cerver_sock import *
field = [[0]*10 for x in range(10)]

def cout(field):
    print("x ", end = ' ')
    for k in range(10):
        print(k + 1, end = '  ')
    for k in range(10):
        if (k < 9):
            print("\n" + str(k + 1) + " ", end = ' ')
        else:
            print("\n" + str(k + 1), end = ' ')
        for j in range(10):
            if (field[k][j] >= 0):
                print (field[k][j], end = '  ')
            else:
                print (field[k][j], end = ' ')


for i in range(10):
    for j in range(10):
        try:
            x, y = map(int,input().split())
        except Exception as e:
            print (e)
            x = input()
        temp = get_answer(x, y);
        field[x - 1][y - 1] = temp
        cout(field)
        print("\n", temp)