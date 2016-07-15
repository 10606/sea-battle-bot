import time
users = open('users.txt','r')
usersf = []
gg = users.readline().split(' ')
while gg[0] != '':
    usersf.append(gg)
    gg = users.readline().split(' ')
users.close()
users = open('users.txt','w')
for i in usersf:
    users.write(i[0] + ' ' + str(int(time.time())) + '\n')
users.close()
import start_server
