Документацию для фронтенда запилю.
Документацию запилю. ДАААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА
Пишу в первый раз, так что сообщайте, если что не так. А еще лучше, если будете сами дополнять, ведь вы это писали)

Если видите ?, значит, я чего-то не знаю, и либо сами допишите, что там должно быть, либо напишите мне, чтобы я это вставил.



check_field.py (серверная часть):

	def check_field(field):
	- проверяет введённое поле field на правильность (размеры, количество и размещение кораблей).
	- принимает поле field
	- возвращает 0, если поле неправильное, 1 - если правильное
    
check_okrest.py (клиентская часть):

	def check_okr(temp):
	- считает количество соседних с кораблями клеток (для генерации равных полей) на поле temp.
	- принимает поле temp
	- возвращает количество соседних с кораблями клеток
	- используется в файле client_cerver_sock.py в функции make_field

	def fill_okr(field, x, y):
	- заполняет на поле field все соседние с клтекой (х,у) клетки, а также саму эту клетку
	- принимает поле field, координаты клетки x и y
	- ничего не возвращает, т.к в процессе выполнения изменяет поле field
	- используется в check_okrest() в этом же файле
  
client_cerver_sock.py - версия для игры с сервером через сокеты (клиетнтская часть):

	def send_to_server(msg):
	- пытается отправить сообщение msg, если сервер не отвечает, выводит сообщение об ошибке
	- принимает строку msg
	- ничего не возвращает:
	- выводит:
		1) "server not ask" - если сервер не отвечает
		2) ошибку е и порядковый номер ошибки ctr, если произошла ошибка
		3) ничего, если сообщение удалось отправить
	- используется только в этом файле:
		1) вне функций  - в начале игры для отправки серверу name - имя игрока
		2) в функции send_message - для отправки запроса по координатам (х,у)
		3) в функции send_field_to_server - для отправки поля

	def message_get():
	- получает сообщение от сервера по сокету
	- ничего не принимает
	- возвращает то, что находится на сокете (или то, что придет на сокет), в виде строки
	- выводит:
		1) ошибку е и порядковый номер ошибки ctr, если произошла ошибка
		2) "time out", если слишком долго не можем получить сообщение
		3) ничего, если все нормально
	- используется только в этом файле:
		1) в начале игры
		2) в функции get_answer - для приема сообщения сервера о результате нашего хода
		3) в функции get_result - для приема сообщения сервера о результате нашего хода
		4) в функции send_field - для приема ответа от сервера о корректности поля
	
	def send_message(x,y):
	- отправляет запрос по координатам х и у
	- принимает координаты x и y (0 <= x,y <= 9)
	- ничего не возвращает, т.к. вызывает send_to_server
	- выводит:
		1) координаты в виде <буква A-J><цифра 1-10> в случае удачной отправки
		2) ошибку е и порядковый номер ошибки ctr в случае ошибки во время отправки
	- используется в этом файле:
		1) в функции get_answer - для отправки серверу запроса
		2) в функции get_result - для отправки серверу запроса

	def get_answer(a,b):
	- обработка сообщения сервера о результате нашего хода, принимает картинку от сервера по окончании игры
	- принимает координаты выстрела a,b (0 <= x,y <= 9)
	- возвращает:
		1) -1, если выстрел - промах
		2) 1, если выстрел - попадание в корабль, но не уничтожение
		3) 2, если выстрел - уничтожение корабля
		4) 3, если выстрел в эту точку был произведен
		5) 4, если игра окончена
		6) 5, если победа
		7) 6, если поражение
		8) 7, если сервер не отвечает
	- выводит "Победа" или "Поражение", если игра окончена
	- не используется в этом файле необходимо вызвать для получения ответа сервера на запрос
	
	def get_result(req):
	- обработка сообщения сервера о результате нашего хода, принимает картинку от сервера по окончании игры
	- принимает координаты выстрела req в формате <бувка A - J><число 1 - 10> 
	- возвращает:
		1) Промах, если выстрел - промах
		2) Ранение, если выстрел - попадание в корабль, но не уничтожение
		3) Убит, если выстрел - уничтожение корабля
		4) Вы уже стреляли сюда, если в эту точку был произведен
		5) Игра уже завершена, если игра окончена
		6) Победа, если победа
		7) Поражение, если поражение
		8) Сервер не отвечает, если сервер не отвечает
	- не используется в этом файле необходимо вызвать для получения ответа сервера на запрос
	
	def get_ships(length, field):
	- поиск всех возможных кораблей длины length на поле field
	- принимает 
		1) длину length корабля координаты корректной постановки которого необходимо найти на поле
		2) поле field на котором надо найти все возможные корректные позиции корабля длины length
	- возвращает список координат
	- используется в make_field() для генерации поля
	
	def change_field(field):
	- приведение поля 12х12 к типу 10х10
	- принимает поле 12х12
	- возвращает поле 10х10
	- используется в make_field() для подсчета количества окрестностей корабля на поле для генерации равных полей
	
	def make_field():
	- генерирует поле
	- ничего не принимает 
	- возвращает поле
	- используется в send_field() для отправки сгенерированного поля серверу
	
	def send_field_to_server(field):
	- отправляет поле серверу
	- принимает поле
	- возвращает "*" если не удалось отправить поле
	- используется в send_field() для отправки поля
	
	def send_field():
	- отправляет поле пока не получит ответ сервера что поле корректно выводит "send field"
	- ничего не принимает
	- возвращает "*" если не удалось отправить или получить ответ
	- используется в connect_to_server()
	
	def connect_to_server():
	- подключается к серверу, отправляет имя и поле и получает подтверждение от сервера выводит "не удалось подключиться к серверу" если сервер недоступен для подключения
	- ничего не принимает
	- возвращает "*" если не удалось подключиться, отправить имя или поле или же получить подтверждение
	- необходимо вызвать перед началом партии


contacts_sock.py - версия с сокетами (серверная часть)
	
	def init_sock(sz, iindex):
	- инициализирует sz сокетов начиная с позиции iindex выводит адрес подключившихся клиентов
	- принимает sz количетво сокетов для инициализации и iindex позицию 
	- ничего не возвращает
	- используется в main_server_sock.py 
	
	def send_to_client(index, msg):
	- отправляет сообщение msg клиенту с номером index, выводит ошибку если не удалось отправить, выводит что было отправлено
	- принимает index номер клиента и msg сообщение которое необходимо отправить
	- возвращает "*" если не удалось отправить
	- используется в main_server_sock.py 
	
	def check_format_field(msg): 
	- проверяет что это поле по формату
	- принимает запрос field
	- возвращает 1, если формат верный и 0, если формат неверный
	- используется в get_request_sock(index)
	
	def check_format_request(message):
	- прповеряет что это запрос от клиента по формату
	- принимает запрос message
	- возвращает 0, если неверный форма и 1, если верный
	- используется в get_request_sock(index)
	
	def get_from_client(index):
	- получает сообщение от клиента с номером index
	- принимает index индекс клиента
	- возвращает "*" если клиент не отвечает, иначе сообщение клиента
	- используется в get_request_sock(index)
	
	def get_request_sock(index):
	- получает запрос от клиента index, если он не соответствует формату игнорирует его, выводит что было принято если соответствует формату
	- принимает index индекс клиента
	- возвращает "*" если не удалось получить запрос, иначе запрос клиента 
	- используется в main_server_sock.py 

drawing.py - версия с сокетами (серверная часть)
	
	def recover(field):
	- принимает поле field (двумерный массив) в формате 10x10
	- Формат поля:
            1) 0 - клетка пуста
            2) 1 - мимо
            3) 2 - есть корабль 
            4) 3 - есть раненый корабль
            5) 4 - есть убитый корабль
	- Обносит убитые корабли точками (мимо)
	- Возвращает поле в том же формате с обнесенными кораблями
	- Используется в функции draw этого файла
	
	def draw(field1, field2, index):
	- Принимает два поля (двумерные массивы) в формате 10x10 и порядковый номер клиента
	- Формат поля:
            1) 0 - клетка пуста
            2) 1 - мимо
            3) 2 - есть корабль 
            4) 3 - есть раненый корабль
            5) 4 - есть убитый корабль
	- Ничего не возвращает
	- В результате исполнения в папке с drawing.py появляется JPEG файл, который отправляется клиенту
	- Итоговый размер картинки: 800px в ширину и 400px в высоту
	- Для работы использует файлы _beside.png, _em_ship.png, _kill_ship.png из папки draw и файл field.jpg
	- Используется в файле main_server_sock.py в функции main


main_server_sock.py - основнаой файл сервера (серверная часть)
	
	def main ():
	- основная функция сервера, инициализирует клиентов, принимает поле и имя игроков, ведет игру, отправляет результат и картинку
	- принимает my_index индекс клиента
	- возвращает empty когда оба клиента проинициализированы
	- используется в этом файле
	
	
	запускается main () в отдельном потоке если empty == 1 и передает через глобалльную переменную индекс клиента


pict.py - файл приема картинки (клиентская часть)
	
	def send_accept(sock):
	- отправляет подтвердение серверу что получен пакет
	- принимает сокет на который отправляет подтверждение
	- вовзращает "*", если не удалось отправить
	- используется в get_list_byte(sock, i) и get_pic(file_name,sock)
	
	def get_list_byte(sock, i):
	- получает пакет с номером i с сокета sock
	- получает сокет и намер пакета
	- возвращает пакет или "*", если сервер не отвечает
	- используется в get_pic(file_name,sock)
	
	def get_pic(file_name,sock):
	- записывает картинку в file_name полученную с сокета
	- принимает сокет и имя файла
	- возвращает "*", если не удалось принять
	- используется в main_server_sock.py


request.py - файл ответа на запрос (серверная часть)

 	def check_request(field, x, y):
 	- на поле field по координатам x y возвращает результат запроса
 	- принимает поле field и координаты x y
 	- возвращает результат запроса:
 		1) 0 - мимо
		2) 1 - ранил
		3) 2 - убил


resourse.py  - файл ресурсов сервера (серверная часть)
	
	содержит описание всех синонимов к ответам на запрос
	
	def ch(field, x, y):
	- превращает раненые палубы убитого корабля в убитые
	- принимает поле и координаты убитого корабля
	- возвращает измененное поле
	- используется в main_server_sock.py для рисования обноски корабля
	
	def get_coordinate(msg):
	- переводит формат запроса <бувка><число> в формат <число><число>
	- принимает сообщение в формате <бувка><число>
	- возвращает сообщение в формате <число><число>
	- использкется в main_server_sock.py
	

