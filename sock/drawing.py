from PIL import Image, ImageDraw
def recover(field):
    new_fld=[[0]*12 for i in range(12)]
    for i in range(10):
        for j in range(10):
            new_fld[i+1][j+1]=field[i][j]
    for i in range(1,11):
        for j in range(1,11):
            if new_fld[i][j]==4:
                if new_fld[i+1][j]!=4:
                    new_fld[i+1][j]=-1
                if new_fld[i+1][j+1]!=4:
                    new_fld[i+1][j+1]=-1
                if new_fld[i][j+1]!=4:
                    new_fld[i][j+1]=-1
                if new_fld[i-1][j]!=4:
                    new_fld[i-1][j]=-1
                if new_fld[i-1][j-1]!=4:
                    new_fld[i-1][j-1]=-1
                if new_fld[i-1][j+1]!=4:
                    new_fld[i-1][j+1]=-1
                if new_fld[i+1][j-1]!=4:
                    new_fld[i+1][j-1]=-1
                if new_fld[i][j-1]!=4:
                    new_fld[i][j-1]=-1
    res = [[0]*10 for i in range(10)]
    for i in range(10):
        for j in range(10):
            res[i][j] = new_fld[i+1][j+1]
    return res
'''
принимает два поля в формате
-1 - обноска
0 - клетка пуста
1 - мимо
2 - есть корабль
3 - есть раненый корабль
4 - есть убитый корабль
'''
def draw(field1, field2, index):
    field = Image.open('field.jpg')
    draw = ImageDraw.Draw(field)
    width = field.size[0]
    height = field.size[1]	
    pix = field.load()    
    fir = Image.open('draw/_beside.png')
    beside = fir.load()
    sec = Image.open('draw/_em_ship.png')
    em_ship = sec.load()
    third = Image.open('draw/_kill_ship.png')
    kill_ship = third.load()
    fir_ = Image.open('draw/_beside.png')
    beside_ = fir_.load()
    now_x = 50
    now_y = 70
    field1 = recover(field1)
    for i in range(10):
        for j in range(10):
            if field1[i][j] == -1:
                for k in range(30):
                    for t in range(30):
                        if beside_[k,t]!=(0,0,0):
                            draw.point((now_x+k,now_y+t), beside_[k,t])
            if field1[i][j] == 1:
                for k in range(30):
                    for t in range(30):
                        if beside[k,t]!=(0,0,0):
                            draw.point((now_x+k,now_y+t), beside[k,t])
            elif field1[i][j]==2:
                for k in range(30):
                    for t in range(30):
                         if em_ship[k,t]!=(0,0,0):
                            draw.point((now_x+k,now_y+t), em_ship[k,t])
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
    field2 = recover(field2)
    for i in range(10):
        for j in range(10):
            if field2[i][j] == -1:
                for k in range(30):
                    for t in range(30):
                        if beside_[k,t]!=(0,0,0):
                            draw.point((now_x+k,now_y+t), beside_[k,t])
            if field2[i][j] == 1:
                for k in range(30):
                    for t in range(30):
                        if beside[k,t]!=(0,0,0):
                            draw.point((now_x+k,now_y+t), beside[k,t])
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
    field.save('ready' + str(index) + '.jpg', 'JPEG')
    field.close()

    
