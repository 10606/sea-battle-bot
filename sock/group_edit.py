import requests, sys,time,json, urllib.request,vk
TL = 2
token = ""
bo = ""
bot1 = ""
bot2 = ""
captcha = ""
id_bot1 = ""
def login_():
    global token
    global bo
    global bot1
    global bot2
    global captcha
    global id_bot1
    stdin1=open('token_server.txt','r')
    token1=stdin1.read()
    token += token1
    stdin1.close()
    stdin1=open('group.txt','r')
    bo1=stdin1.read()
    bo += bo1
    id_bot1 += bo
    stdin1.close()
    stdin1=open('capt_chat.txt','r')
    bot2=stdin1.read()
    bot1 += bot2
    stdin1.close()
    stdin1=open('token_captcha.txt','r')
    captcha1=stdin1.read()
    captcha += captcha1
    stdin1.close()
    #print(id_bot1, bo)
    return 51

#отправляет сообщение пользователю to_id (с обходом капчи)
def group_edit(to_id, msg):
    #print("captcha ", captcha)
    time_start = time.time()
    print('edit description group ',to_id)
    while True:
        if time.time()-time_start > 120:
            return "*"
        try:
            url='https://api.vk.com/method/groups.edit?group_id='+str(to_id)+'&description='+str(msg)+'&access_token='+str(token)+'&v=5.52'
            #url='https://api.vk.com/method/messages.send?message='+str(msg)+'&user_id='+str(to_id)+'&access_token='+str(token)+'&v=5.52'
            r=requests.get(url)
            if len(str(r.text))>25:
                print('КАПЧА!!1!!1')
                print(r.text)
                v=json.loads(r.text)
                capt_url=v['error']['captcha_img']
                sid=v['error']['captcha_sid']
                new_msg='Для продолжения игры введите капчу '
                session = vk.Session(access_token=captcha,)
                api = vk.API(session,v='5.38')
                url = capt_url
                img = urllib.request.urlopen(url).read()
                out = open('images/captcha.jpg','wb')
                out.write(img)
                out.close()
                print('Saved as','images/captcha.jpg')
                ans=api.photos.getMessagesUploadServer()
                print('sending photo')
                new_url = ans['upload_url']
                files = {'photo': open('images/captcha.jpg', 'rb')}
                r = requests.post(new_url, files=files)
                r = r.json()
                print('get photo id')
                photo_id = api.photos.saveMessagesPhoto(photo = r['photo'], server = r['server'], hash = r['hash'])
                photo_id='photo'+str(photo_id[0]['owner_id'])+'_'+str(photo_id[0]['id'])
                print('sending message')
                api.messages.send(peer_id = str(int(bot1)+2000000000), message='Чтобы продолжить игру введите эту капчу (прямо сюда)', attachment = photo_id)
                #time.sleep(TL)
                #api.messages.send(user_id = bot2, message='Чтoбы продолжить игру введите эту капчу (прямо сюда)', attachment = photo_id)
                print('ready')
                while True:
                    flag=True
                    time.sleep(TL)
                    new_msg = api.messages.getHistory(offset=0, count=1, peer_id=str(int(bot1)+2000000000), rev=0)
                    mesg=new_msg['items'][0]['body']
                    if (len(new_msg) == 0 or len(mesg)>=10):
                        flag=False
                    if flag:
                        break
                key=mesg
                print(key)
                url = 'https://api.vk.com/method/groups.edit?group_id=' + str(to_id) + '&description=' + str(msg) + '&access_token=' + str(token) + '&v=5.52'
                #url='https://api.vk.com/method/messages.send?message='+str(msg)+'&user_id='+str(to_id)+'&access_token='+str(token)+'&v=5.52'
                par = {'captcha_sid': sid, 'captcha_key':key}
                r=requests.get(url, params=par)
                if len(str(r.text))>25:
                    #api.messages.send(user_id = bot2, message='Введите другую капчу')
                    #time.sleep(1)
                    api.messages.send(peer_id = str(int(bot1)+2000000000), message='Введите другую кaпчу')
                    continue
                else:
                    break
            else:
                break
        except Exception as e:
            print(e)
            time.sleep(TL)
