# -*- coding: utf-8 -*-

def check_field(field):
    ship = [0, 8, 3, 2, 1]
    flag = 1
    if (len(field) != 10):
        return 0 
    for i in range(len(field)):
        counter = 0
        if (len(field[i]) != 10):
            return 0
        for j in range(len(field[i])):
            if field[i][j] == 0:
                if counter > 4:
                    flag = 0
                else:
                    ship[counter] -= 1
                counter = 0
            if ((field[i][j] != 0) and (i == 0 or field[i - 1][j] == 0) and (i == len(field) - 1 or field[i + 1][j] == 0)):
                counter += 1
            if ((field[i][j] != 0) and not((i == 0 or field[i - 1][j] == 0) and (i == len(field) - 1 or field[i + 1][j] == 0))):
                if counter > 4:
                    flag = 0
                else:
                    ship[counter] -= 1
                counter = 0
        if counter > 4:
            flag = 0
        else:
            ship[counter] -= 1
            counter = 0            
    for i in range(len(field)):
        counter = 0
        for j in range(len(field[i])):
            if field[j][i] == 0:
                if counter > 4:
                    flag = 0
                else:                
                    ship[counter] -= 1
                counter = 0
            if ((field[j][i] != 0) and (i == 0 or field[j][i - 1] == 0) and (i == len(field) - 1 or field[j][i + 1] == 0)):
                counter += 1
            if ((field[j][i] != 0) and not((i == 0 or field[j][i - 1] == 0) and (i == len(field) - 1 or field[j][i + 1] == 0))):
                if counter > 4:
                    flag = 0
                else:
                    ship[counter] -= 1
                counter = 0 
        if counter > 4:
            flag = 0
        else:
            ship[counter] -= 1
            counter = 0                  
    ship[0] = 0;
    for i in range(5):
        if ship[i] != 0:
            flag = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] != 0:
                if i > 0:
                    if (j > 0 and field[i - 1][j - 1] != 0):
                        flag = 0
                    if (j < len(field[i]) - 1 and field[i - 1][j + 1] != 0):
                        flag = 0
                if i < len(field) - 1:
                    if (j > 0 and field[i + 1][j - 1] != 0):
                        flag = 0
                    if (j < len(field[i]) - 1 and field[i + 1][j + 1] != 0):
                        flag = 0     
    return flag

