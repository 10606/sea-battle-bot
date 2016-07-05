from PIL import Image, ImageDraw
from vk import *
from pprint import pprint
import sys,requests,time
from message import *
sys.stdin=open('token_server.txt','r')
token=input()
sys.stdin.close()
session=Session(access_token=token)
api=API(session)
#отсылает фото текущего состояния поля пользователю
def send_field_to_user(usrid,msg):
    while True:
        try:
            ans=api.photos.getMessagesUploadServer()
            print('sending photo')
            url = ans['upload_url']
            files = {'photo': open('draw/ready_field.jpg', 'rb')}
            r = requests.post(url, files=files)
            r = r.json()
            print('get photo id')
            photo_id = api.photos.saveMessagesPhoto(photo = r['photo'], server = r['server'], hash = r['hash'])
            #print(photo_id)
            photo_id=photo_id[0]['id']
            print('sending message')
            messages_send(usrid, msg+'&attachment='+str(photo_id))
            print('ready')
            break
        except Exception as e:
            print(e)
            time.sleep(5)

#обносит убитые корабли точками
def points(field):
    new_fld=[[0]*12 for i in range(12)]
    for i in range(10):
        for j in range(10):
            new_fld[i+1][j+1]=field[i][j]
    for i in range(1,11):
        for j in range(1,11):
            if new_fld[i][j]==2:
                if new_fld[i+1][j]!=2:
                    new_fld[i+1][j]=-1
                if new_fld[i+1][j+1]!=2:
                    new_fld[i+1][j+1]=-1
                if new_fld[i][j+1]!=2:
                    new_fld[i][j+1]=-1
                if new_fld[i-1][j]!=2:
                    new_fld[i-1][j]=-1
                if new_fld[i-1][j-1]!=2:
                    new_fld[i-1][j-1]=-1
                if new_fld[i-1][j+1]!=2:
                    new_fld[i-1][j+1]=-1
                if new_fld[i+1][j-1]!=2:
                    new_fld[i+1][j-1]=-1
                if new_fld[i][j-1]!=2:
                    new_fld[i][j-1]=-1
    return(new_fld)

#по полю создает его картинку
def draw_the_field(field,usrid,msg):
    picture = Image.open('draw/field.jpg')
    draw = ImageDraw.Draw(picture)
    pic = picture.load()
    now_x = 50
    now_y = 50
    get=points(field)
    for i in range(1,11):
        for j in range(1,11):
            if get[i][j]!=0:
                #если мимо
                if get[i][j]==-1:
                    for k in range(30):
                        for t in range(30):
                            if beside[k,t]!=(0,0,0):
                                draw.point((now_x+k,now_y+t), beside[k,t])
                #если ранен
                elif get[i][j]==1:
                    for k in range(30):
                        for t in range(30):
                            if hurt[k,t]!=(0,0,0):
                                draw.point((now_x+k,now_y+t), hurt[k,t])
                #если убит
                elif get[i][j]==2:
                    for k in range(30):
                        for t in range(30):
                            if killed[k,t]!=(0,0,0):
                                draw.point((now_x+k,now_y+t), killed[k,t])
            now_x+=30
        now_y+=30
        now_x=50
    picture.save('draw/ready_field.jpg','JPEG')
    send_field_to_user(usrid, msg)

def get_result(first, second, usrid):
    msg='Поле соперника:'
    picture = Image.open('draw/field.jpg')
    draw = ImageDraw.Draw(picture)
    pic = picture.load()
    now_x = 50
    now_y = 50
    get=points(first)
    for i in range(1,11):
        for j in range(1,11):
            if get[i][j]!=0:
                #если мимо
                if get[i][j]==-1:
                    for k in range(30):
                        for t in range(30):
                            if beside[k,t]!=(0,0,0):
                                draw.point((now_x+k,now_y+t), beside[k,t])
                #если ранен
                elif get[i][j]==1:
                    for k in range(30):
                        for t in range(30):
                            if kill_ship[k,t]!=(0,0,0):
                                draw.point((now_x+k,now_y+t), kill_ship[k,t])
                #если убит
                elif get[i][j]==2:
                    for k in range(30):
                        for t in range(30):
                            if kill_ship[k,t]!=(0,0,0):
                                draw.point((now_x+k,now_y+t), kill_ship[k,t])
                elif get[i][j]==10:
                    for k in range(30):
                        for t in range(30):
                            if em_ship[k,t]!=(0,0,0):
                                draw.point((now_x+k,now_y+t), em_ship[k,t])
            now_x+=30
        now_y+=30
        now_x=50
    picture.save('draw/ready_field.jpg','JPEG')
    send_field_to_user(usrid, msg)
    picture = Image.open('draw/field.jpg')
    draw = ImageDraw.Draw(picture)
    pic = picture.load()
    now_x = 50
    now_y = 50
    get=points(second)
    for i in range(1,11):
        for j in range(1,11):
            if get[i][j]!=0:
                #если мимо
                if get[i][j]==-1:
                    for k in range(30):
                        for t in range(30):
                            if beside[k,t]!=(0,0,0):
                                draw.point((now_x+k,now_y+t), beside[k,t])
                #если ранен
                elif get[i][j]==1:
                    for k in range(30):
                        for t in range(30):
                            if kill_ship[k,t]!=(0,0,0):
                                draw.point((now_x+k,now_y+t), kill_ship[k,t])
                #если убит
                elif get[i][j]==2:
                    for k in range(30):
                        for t in range(30):
                            if kill_ship[k,t]!=(0,0,0):
                                draw.point((now_x+k,now_y+t), kill_ship[k,t])
                elif get[i][j]==10:
                    for k in range(30):
                        for t in range(30):
                            if em_ship[k,t]!=(0,0,0):
                                draw.point((now_x+k,now_y+t), em_ship[k,t])
            now_x+=30
        now_y+=30
        now_x=50
    picture.save('draw/ready_field.jpg','JPEG')
    msg='Ваше поле:'
    send_field_to_user(usrid, msg)
    
#print (time.time())    
fir = Image.open('draw/_beside.png')
beside = fir.load()
sec = Image.open('draw/_hurt.png')
hurt = sec.load()
third = Image.open('draw/_killed.png')
killed = third.load()
fourth=Image.open('draw/_em_ship.png')
em_ship = fourth.load()
five=Image.open('draw/_kill_ship.png')
kill_ship = five.load()
'''field=[[0, 0, 1, 1 ,0, -1, 0, 1, 1, 0],
       [1, -1, -1, 0, 0, 2, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, -1, 0, 0],
       [0, 0, 0, -1, 0, 0, 0, 0, 0, 0],
       [0, 0, 10, 0, 0, 0, 0, 0, 0, 0],
       [0, 2, 0, 0, -1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
       [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 10, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 2]]
usrid='22346494'
msg = 'Соперник выстрелил в A3 и ранил ваш корабль\n'
for i in range(3):
    get_result(field,field,usrid)
print(time.time())'''























