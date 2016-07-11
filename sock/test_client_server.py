import sys, time, math,random
from client_cerver_sock import *

connect_to_server()
for i in range(10):
    for j in range(10):
        temp = get_answer(i + 1, j + 1);
        temp = get_answer(i + 1, j + 1);
        #print(temp)

connect_to_server()
for i in range(10):
    for j in range(10):
        temp = get_answer(i + 1, j + 1);