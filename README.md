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
		2) в функции get_coordinate (устаревшая, не поддерживается сервером) - для приёма сообщения соперника о его выстреле
		3) в функции get_answer - для приема сообщения сервера о результате нашего хода
		4) в функции get_result - для приема сообщения сервера о результате нашего хода
		5) в функции send_field - для приема ответа от сервера о корректности поля
	
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

	def get_coordinate(): (не поддерживается сервером)
	- получает сообщение соперника (?) о выстреле, перерабатывает его из формата <буква><число> в формат <число><число>
	- ничего не принимает, т.к. вызывает message_get
	- возвращает информацию о выстреле в формате <число><число>
	- не используется

	def get_answer(a,b):
	- обработка сообщения сервера о результате нашего хода, принимает картинку от сервера по окончании игры
	- принимает координаты выстрела a,b (0 <= x,y <= 9)
	- возвращает:
		1) -1, если выстрел - промах
		2) 1, если выстрел - попадание в корабль, но не уничтожение
		3) 2, если выстрел - уничтожение корабля
		4) 3, если выстрел в эту точку был произведен
		5) 4, если игра окончена
	- выводит "Победа" или "Поражение", если игра окончена
	- не используется в этом файле
		
