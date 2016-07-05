# -*- coding: utf-8 -*-
temp = [[0]*10 for x in range(10)]
temp[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
temp[1] = [0, 1, 1, 1, 1, 0, 1, 0, 0, 0]
temp[2] = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1]
temp[3] = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
temp[4] = [0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
temp[5] = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
temp[6] = [0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
temp[7] = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
temp[8] = [0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
temp[9] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#0 - мимо
#1 - ранил
#2 - убил

def check_request(field, x, y):
    if (x < 0 or x > 9 or y < 0 or y > 9):
        return 0
    if (field[x][y] == 0):
        return 0
    field[x][y] = 2
    flag = 2
    if (x == 0 or field[x - 1][y] == 0) and (x >= len(field) - 1 or field[x + 1][y] == 0):
        i = y
        while (i < len(field[x]) and field[x][i] != 0):
            if (field[x][i] != 0 and field[x][i] != 2):
                flag = 1
            i += 1
        i = y
        while (i >= 0 and field[x][i] != 0):
            if (field[x][i] != 0 and field[x][i] != 2):
                flag = 1
            i -= 1
    else:
        i = x
        while (i < len(field) and field[i][y] != 0):
            if (field[i][y] != 0 and field[i][y] != 2):
                flag = 1
            i += 1
        i = x
        while (i >= 0 and field[i][y] != 0):
            if (field[i][y] != 0 and field[i][y] != 2):
                flag = 1
            i -= 1
    return flag
'''
print(check_request(temp, 1, 2))
print(check_request(temp, 1, 1))
print(check_request(temp, 1, 3))
print(check_request(temp, 1, 4))
print(check_request(temp, 1, 5))
print(check_request(temp, 0, 9))
'''
