ttmp = [[0]*10 for x in range(10)]
ttmp[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
ttmp[1] = [0, 1, 1, 1, 1, 0, 1, 0, 0, 0]
ttmp[2] = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1]
ttmp[3] = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
ttmp[4] = [0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
ttmp[5] = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
ttmp[6] = [0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
ttmp[7] = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
ttmp[8] = [0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
ttmp[9] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ttmp[9] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def fill_okr(field, x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (x + i >= 0 and x + i < len(field) and y + j >= 0 and y + j < len(field[x + i])):
                field[x + i][y + j] = 1;

def check_okr(temp):
    field = [[0] * 10 for i in range(10)];
    for i in range(10):
        for j in range(10):
            if (temp[i][j] == 1):
                fill_okr(field, i, j);
    counter = 0;
    for i in range(10):
        for j in range(10):
            if (field[i][j] > 0 and temp[i][j] != 1):
                counter += 1;
    return counter;

print(check_okr(ttmp));
