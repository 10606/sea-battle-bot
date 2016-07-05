from PIL import Image, ImageDraw
import random
#рисует поле с нуля
#нужно если захотим поменять надписи, сменить фон и т.п.

#в field грузим фон. На нем и будем рисовать
field = Image.open('draw/_background.jpg')
draw = ImageDraw.Draw(field)
width = field.size[0]
height = field.size[1]	
pix = field.load()

#грузим клетку
cell = Image.open('draw/_cell.png')
pix_cell = cell.load()
now_x=50
now_y=50
cell_size=30
for i in range(10):
    for j in range(10):
        for k in range(cell_size):
            for t in range(cell_size):
                u = pix_cell[k,t]
                if u != (0,0,0):
                    draw.point((now_x+k,now_y+t),u)               
        now_x+=cell_size
    now_y+=cell_size
    now_x=50

#грузим буквы и цифры для разметки поля
letter_size = 30
now_x = 50
now_y = 50-letter_size
for i in range(10):
    letter = Image.open('draw/'+str(i+1)+'.png')
    let = letter.load()
    for j in range(letter_size):
        for k in range(letter_size):
            u=let[j,k]
            if u != (0,0,0):
                draw.point((now_x+j,now_y+k),u)
    now_x+=cell_size
now_x=50-letter_size
now_y=50
for i in range(10,20):
    letter = Image.open('draw/'+str(i+1)+'.png')
    let = letter.load()
    for j in range(letter_size):
        for k in range(letter_size):
            u=let[j,k]
            if u != (0,0,0):
                draw.point((now_x+j,now_y+k),u)
    now_y+=cell_size

#место для рекламы... ну вдруг... надежда умирает последней...
add = Image.open('draw/add.png')
adv = add.load()
now_x=350
now_y=50
for i in range(50):
    for j in range(299):
        if adv[i,j] != (0,0,0):
            draw.point((now_x+i,now_y+j),adv[i,j])

#имена создатеелей
add = Image.open('draw/adr.png')
adv = add.load()
now_x=50
now_y=350
for i in range(314):
    for j in range(50):
        if adv[i,j] != (0,0,0):
            draw.point((now_x+i,now_y+j),adv[i,j])

#сохраняет поле
field.save("draw/field.jpg","JPEG")

#выводит поле на экран
field.show()
        
        

