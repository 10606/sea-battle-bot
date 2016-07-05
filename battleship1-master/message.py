import requests, sys,time,json, urllib.request,vk
sys.stdin=open('token_server.txt','r')
token=input()
sys.stdin.close()
sys.stdin=open('capt_chat.txt','r')
bot1=input()
sys.stdin.close()
sys.stdin=open('bot2.txt','r')
bot2=input()
sys.stdin.close()
sys.stdin=open('token_captcha.txt','r')
captcha=input()
sys.stdin.close()
#отправляет сообщение пользователю to_id (с обходом капчи)
def messages_send(to_id, msg):
    print('sending message to ',to_id)
    while True:
        try:
            url='https://api.vk.com/method/messages.send?message='+str(msg)+'&user_id='+str(to_id)+'&access_token='+str(token)+'&v=5.52'
            r=requests.get(url)
            if len(str(r.text))>25:
                print('КАПЧА!!1!!1')
                print(r.text)
                v=json.loads(r.text)
                capt_url=v['error']['captcha_img']
                sid=v['error']['captcha_sid']
                new_msg='Для продолжения игры введите капчу '
                session = vk.Session(access_token=captcha)
                api = vk.API(session)
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
                #print(photo_id)
                photo_id=photo_id[0]['id']
                print('sending message')
                api.messages.send(user_id = bot1, message='Чтобы продолжить игру введите эту капчу (прямо сюда)', attachment = photo_id)
                time.sleep(3)
                api.messages.send(user_id = bot2, message='Чтoбы продолжить игру введите эту капчу (прямо сюда)', attachment = photo_id)
                print('ready')
                while True:
                    flag=True
                    time.sleep(3)
                    new_msg = api.messages.getHistory(offset=0, count=1, user_id=bot2, rev=0)
                    mesg=new_msg[1]['body']
                    print(mesg)
                    if (len(new_msg) == 0):
                        flag=False
                    print(new_msg[1]['uid'])
                    if (str(new_msg[1]['uid']) != str(bot2)):
                        flag=False
                    if flag:
                        break
                    flag=True
                    time.sleep(3)
                    new_msg = api.messages.getHistory(offset=0, count=1, user_id=bot1, rev=0)
                    mesg=new_msg[1]['body']
                    print(mesg)
                    if (len(new_msg) == 0):
                        flag=False
                    print(new_msg[1]['uid'])
                    if (str(new_msg[1]['uid']) != str(bot1)):
                        flag=False
                    if flag:
                        break
                key=mesg
                print(key)
                url='https://api.vk.com/method/messages.send?message='+str(msg)+'&user_id='+str(to_id)+'&access_token='+str(token)+'&v=5.52'
                par = {'captcha_sid': sid, 'captcha_key':key}
                r=requests.get(url, params=par)
                if len(str(r.text))>25:
                    api.messages.send(user_id = bot2, message='Введите другую капчу')
                    time.sleep(3)
                    api.messages.send(user_id = bot1, message='Введите другую кaпчу')
                    continue
                else:
                    break
            else:
                break
        except Exception as e:
            print(e)
            time.sleep(5)
