# -*- coding: utf-8 -*-
import sys, time, math, random, vk, pygame
player_names=['Игрок1','Игрок2']
#рисование
class Sprite:
    def __init__(self, x, y, size, mode, filename):
        self.x = x
        self.y = y
        self.x_size = size[0]
        self.y_size = size[1]
        self.mode = mode
        self.bitmap = pygame.image.load(filename)
        if filename!='images/_background.jpg':
            self.bitmap.set_colorkey((0,0,0))
    def render(self): #вывод на экран
        screen.blit(self.bitmap,(self.x,self.y))
pygame.init()
size=(1366,768)
window=pygame.display.set_mode(size, pygame.RESIZABLE, 32)
pygame.display.set_caption('IS')
screen=pygame.Surface(size)
pygame.font.init()
screen.fill((50,50,50))
background=Sprite(0,0,(1366,768), 0,'images/_background.jpg')
background.render()
window.blit(screen,(0,0))
pygame.display.flip()
picture_ship='images/_ship.jpg'
picture_beside='images/_beside.png'
picture_hit='images/_hit.png'
picture_cell='images/_cell.png'
#надписи
pygame.font.init()
pygame.font.init()
count_font=pygame.font.SysFont('Agency FB',70)
under_font=pygame.font.SysFont('Agency FB',20)
screen.blit(count_font.render(player_names[0],1,(250,250,250)),(363-(len(player_names[0])/2)*33,20))
screen.blit(count_font.render(player_names[1],1,(250,250,250)),(1003-(len(player_names[1])/2)*33,20))
screen.blit(under_font.render('Морской бой. Авторы:',1,(250,250,250)),(1100,685))
screen.blit(under_font.render('Александр Глезденев',1,(250,250,250)),(1100,695))
screen.blit(under_font.render('Юрий Парадовский',1,(250,250,250)),(1100,705))
screen.blit(under_font.render('Игорь Смирнов',1,(250,250,250)),(1100,715))
screen.blit(under_font.render('Сергей Харитонцев-Беглов',1,(250,250,250)),(1100,725))
#звуки
miss = pygame.mixer.Sound('sounds/miss.ogg')
wound = pygame.mixer.Sound('sounds/wound.ogg')
kill = pygame.mixer.Sound('sounds/kill.ogg')
#рисуем поля
pict_size=(60,60)
now_x=33
now_y=84
pict_1=[]
for i in range(10):
    for j in range(10):
        pict_1.append(Sprite(now_x+j*pict_size[0],
                            now_y+i*pict_size[1], pict_size, 1,
                            picture_cell))
        pict_1[-1].render()
now_x=33+600+40
now_y=84
pict_2=[]
for i in range(10):
    for j in range(10):
        pict_2.append(Sprite(now_x+j*pict_size[0],
                            now_y+i*pict_size[1], pict_size, 1,
                            picture_cell))

        pict_2[-1].render()
window.blit(screen,(0,0))
pygame.display.flip()
def field_1(field1):
    pict_size=(60,60)
    now_x=33
    now_y=84
    ships_1=[]
    for i in range(10):
        for j in range(10):
            if field1[i][j]:
                ships_1.append(Sprite(now_x+j*pict_size[0],
                                     now_y+i*pict_size[1], pict_size, 1,
                                     picture_ship))
                ships_1[-1].render()
    window.blit(screen,(0,0))
    pygame.display.flip()
def field_2(field2):
    now_x=33+600+40
    now_y=84
    ships_2=[]
    for i in range(10):
        for j in range(10):
            if field2[i][j]:
                ships_2.append(Sprite(now_x+j*pict_size[0],
                                     now_y+i*pict_size[1], pict_size, 1,
                                     picture_ship))
                ships_2[-1].render()
    window.blit(screen,(0,0))
    pygame.display.flip()
