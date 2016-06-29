from PIL import Image, ImageDraw
import random
field = Image.open('draw/_background.jpg')
draw = ImageDraw.Draw(field)
width = field.size[0]
height = field.size[1]	
pix = field.load()
cell = Image.open('draw/_cell.jpg')
pix_cell = cell.load()
now_x=50
now_y=50
cell_size=30
#рисуем поле
for i in range(10):
    for j in range(10):
        for k in range(cell_size):
            for t in range(cell_size):
                u = pix[k,t]
                if u != (0,0,0):
                    draw.point((now_x+k,now_y+t),u)               
        now_x+=cell_size
    now_y+=cell_size
    now_x=50
field.save("field.jpg","JPEG")
field.show()
        
        

