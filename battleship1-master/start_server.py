out = open('talking.txt','w')
out.write('gameBegan')
out.close()
from main_server import *
import threading
serv = threading.Thread(target=st_serv, name="st_serv")
serv.start()
from my_algo import *
bot = threading.Thread(target=game, name="game")
bot.start()
serv.join()
bot.join()
