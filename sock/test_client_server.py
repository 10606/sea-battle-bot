import sys, time, math,random
from client_cerver_sock import *

for gg in range(1):
    if (connect_to_server() == "*"):
        continue
    for i in range(10):
        for j in range(10):
            temp = get_answer(i + 1, j + 1)
            #print(temp)
    temp = get_answer(1, 1)
gg = input()