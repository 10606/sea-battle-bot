'''
Обрисовка полей для отправки результата клиентам
Используется в файле main_server_sock.py в функции main
Внимание! Используется библиотека PIL, являющаяся сторонней библиотекой Python
Перед использованием необходимо ее установить
Установка через pip:
    pip install Pillow
Другие способы установки ищите в интернете
'''
from PIL import Image, ImageDraw
'''
принимает поле field (двумерный массив) в формате 10x10
0 - клетка пуста
1 - мимо
2 - есть корабль
3 - есть раненый корабль
4 - есть убитый корабль
Обносит убитые корабли точками (мимо)
Возвращает поле в том же формате с обнесенными кораблями
Используется в функции draw этого файла
'''
def recover(field):
    #создаем копию текущего поля, но в формате 12x12
    #крайние столбцы и строки для удобства
    new_fld=[[0]*12 for i in range(12)]
    for i in range(10):
        for j in range(10):
            new_fld[i+1][j+1]=field[i][j]
    #Для каждой клетки нового поля смотрим, не лежит ли в ней убитый корабль
    #Если лежит, то обносим все клетки вокруг этой кроме тех, в которых тоже есть части убитого корабля
    #Обноска обозначается как 1
    for i in range(1,11):
        for j in range(1,11):
            if new_fld[i][j] == 4:
                if new_fld[i+1][j] != 4:
                    new_fld[i+1][j] = 1
                if new_fld[i][j+1] != 4:
                    new_fld[i][j+1] = 1
                if new_fld[i-1][j] != 4:
                    new_fld[i-1][j] = 1
                if new_fld[i][j-1] != 4:
                    new_fld[i][j-1] = 1
                new_fld[i-1][j-1] = 1
                new_fld[i-1][j+1] = 1
                new_fld[i+1][j-1] = 1
                new_fld[i+1][j+1] = 1
    #переносим результат в новое поле, в формате 10х10
    res = [[0]*10 for i in range(10)]
    for i in range(10):
        for j in range(10):
            res[i][j] = new_fld[i+1][j+1]
    return res
'''
Принимает два поля (двумерные массивы) в формате 10x10 и порядковый номер клиента
Формат полей:
0 - клетка пуста
1 - мимо
2 - есть корабль
3 - есть раненый корабль
4 - есть убитый корабль
Ничего не возвращает
В результате исполнения в папке с drawing.py появляется JPEG файл, который отправляется клиенту
Итоговый размер картинки: 800px в ширину и 400px в высоту
Для работы использует файлы _beside.png, _em_ship.png, _kill_ship.png из папки draw и файл field.jpg
Используется в файле main_server_sock.py в функции main
'''
def draw(field1, field2, index):
    #Рисование происходит на базе field.jpg
    field = Image.open('field.jpg')
    draw = ImageDraw.Draw(field)
    width = field.size[0]
    height = field.size[1]	
    pix = field.load()
    #Загружаем картинку "мимо"
    fir = Image.open('draw/_beside.png')
    beside_ = fir.load()
    #Загружаем картинку "не раненая палуба корабля"
    sec = Image.open('draw/_em_ship.png')
    em_ship = sec.load()
    #Загружаем картинку "раненая палуба корабля"
    third = Image.open('draw/_kill_ship.png')
    kill_ship = third.load()
    now_x = 50
    now_y = 70
    #Выполняем обноску убитых кораблей на field1
    field1 = recover(field1)
    #Процесс рисования. 
    for i in range(10):
        for j in range(10):
            #Обноска или мимо
            if field1[i][j] == 1:
                for k in range(30):
                    for t in range(30):
                        #Здесь и далее цвет (0, 0, 0) является фоновым цветом и не выносится на итоговый рисунок
                        if beside_[k,t]!=(0,0,0):
                            draw.point((now_x+k,now_y+t), beside_[k,t])
            #Не раненая палуба корабля
            elif field1[i][j]==2:
                for k in range(30):
                    for t in range(30):
                         if em_ship[k,t]!=(0,0,0):
                            draw.point((now_x+k,now_y+t), em_ship[k,t])
            #Раненая палуба корабля
            elif field1[i][j]>=3:
                for k in range(30):
                    for t in range(30):
                        if kill_ship[k,t]!=(0,0,0):
                            draw.point((now_x+k,now_y+t), kill_ship[k,t])
            now_x += 30
        now_y += 30
        now_x = 50
    now_x = 450
    now_y = 70
    #Рисование второго поля аналогично рисованию первого
    field2 = recover(field2)
    for i in range(10):
        for j in range(10):
            if field2[i][j] == 1:
                for k in range(30):
                    for t in range(30):
                        if beside_[k,t]!=(0,0,0):
                            draw.point((now_x+k,now_y+t), beside_[k,t])
            elif field2[i][j]==2:
                for k in range(30):
                    for t in range(30):
                         if em_ship[k,t]!=(0,0,0):
                            draw.point((now_x+k,now_y+t), em_ship[k,t])
            elif field2[i][j]>=3:
                for k in range(30):
                    for t in range(30):
                        if kill_ship[k,t]!=(0,0,0):
                            draw.point((now_x+k,now_y+t), kill_ship[k,t])
            now_x += 30
        now_y += 30
        now_x = 450
    #сохраняем результат в файл 'ready' + str(index) + '.jpg'
    field.save('ready' + str(index) + '.jpg', 'JPEG')
    field.close()

    
