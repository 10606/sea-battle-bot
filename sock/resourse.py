import sys, time, math, random

def ch(field, x, y):
    for i in range(x + 1, 10):
        if field[i][y] != 3:
            break
        field[i][y] = 4
    for i in range(x - 1, -1, -1):
        if field[i][y] != 3:
            break
        field[i][y] = 4
    for i in range(y + 1, 10):
        if field[x][i] != 3:
            break
        field[x][i] = 4
    for i in range(y - 1, -1, -1):
        if field[x][i] != 3:
            break
        field[x][i] = 4
    return field


max_iter = 1000  # лимит количества ходов


def get_coordinate(msg):
    letter = 'ABCDEFGHIJ'
    return [int(msg[1:]), letter.index(msg[0]) + 1]


mimo = ['Прoмаx', 'Прoмах', 'Прoмax', 'Прoмaх', 'Промаx', 'Промах', 'Промax', 'Промaх',
        'Пpoмаx', 'Пpoмах', 'Пpoмax', 'Пpoмaх', 'Пpомаx',
        'Пpомах', 'Пpомax', 'Пpомaх']
ranen = ['Paнeниe', 'Paнeние', 'Paнениe', 'Paнение', 'Pанeниe', 'Pанeние',
         'Pанениe', 'Pанение', 'Рaнeниe', 'Рaнeние', 'Рaнениe',
         'Рaнение', 'Ранeниe', 'Ранeние', 'Ранениe', 'Ранение']
ubit = ['Убит', 'убит', 'Убил', 'убил']
used = ['Вы уже стреляли сюда', 'Bы уже стреляли сюда', 'Вы ужe стреляли сюда', 'Вы уже cтреляли сюда',
        'Вы уже стрeляли сюда', 'Вы уже стреляли cюда', 'Вы уже стреляли сюдa']
