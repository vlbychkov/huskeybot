from Lib import *
from Other import *
#нужные библиотеки
TOKEN = '815806413:AAGh41rYw3mok9SvLPePMGjBrjAKX7zyvag'
bot = telebot.TeleBot(TOKEN)
menu_remove=types.ReplyKeyboardRemove() 
City = ['Москва','СПб']

#_______________________________________________________________________________________________________________________________________________________________
@bot.message_handler(commands=['aoao'])
def aoao(message):
	for i in City:
		bot.send_message(message.chat.id, i, end=' ')

#Команды
#Начало диалога + вызов кнопок
@bot.message_handler(commands=['start']) 
def handle_start(message):
	bot.send_message(message.chat.id,'Здравствуй, ' + str(message.from_user.first_name),reply_markup=markup )
	bot.send_message(message.chat.id, "Этот Бот устроен по типу календаря. В него можно: Добавлять, удалять, изменять, смотреть даты.")
	bot.send_message(message.chat.id, 'Используй /help, чтобы посмотреть все функции.')
	print(message.from_user.first_name)

#_______________________________________________________________________________________________________________________________________________________________


@bot.message_handler(commands=['help','помощь'])
def handler_help(message):
	bot.send_message(message.chat.id,"""Вижу, тебе нужна помощь...
Смотри внимательней и запоминай:
Это основные команды 
/Инструкция или /instruction - Инструкция к использованию.
/setdate или /установкадаты - Создай событие и установи его дату. 
/lookdate или /ближдата - Просмотр ближайшего события и его даты.
/monthdate или /датанамесяц - Просмотр дат на месяц.
/changedate или /изменадаты - Измени дату события. p.s. забыл вписать - пока не трогать.
/cpass - Изменение пароля.
/deletedate или /удалениедаты - Удаление даты.
Также есть команда /scommands - Показ второстепенных команд.
Немного подожди и будет больше команд и возможностей!""")
	print(message.from_user.first_name)

@bot.message_handler(commands=['scommands'])
def scommand(message):
	bot.send_message(message.chat.id,"""Это второстепенные команды, которые мало влияют на что-то: 
/time - Вызов времени.
/random - Рандомное число до 10.
/info - Информация о моем создателе и фото его команды. """)


#Конец диалога + убирает кнопки
@bot.message_handler(commands=['end']) 
def handle_end(message):
	bot.reply_to(message, 'Ладно, сворачиваю панель. Чтобы снова вызвать - /start.',reply_markup=menu_remove)
	print(message.from_user.first_name)
#_______________________________________________________________________________________________________________________________________________________________
#Вызов даты
@bot.message_handler(commands=['time','время']) 
def handle_time(message):
	bot.send_message(message.chat.id, "Ты же в телефоне сидишь? Не мог на нем посмотреть? А часов у тебя тоже нет? Да ладно тебе...")
	bot.reply_to(message,'На,смотри сегодняшнюю дату: '+ maneTimeDate)
	bot.send_message(message.chat.id,"Надеюсь, время тебе не нужно хоть? 🤔")

	
#_______________________________________________________________________________________________________________________________________________________________
@bot.message_handler(commands=['test'])
def test(message):
	bot.send_message(message.chat.id, message.chat.id)
	bot.send_message(message.chat.id, message.chat.type)
	bot.send_message(message.chat.id, message.chat.username)
	bot.send_message(message.chat.id, message.chat.title)
#_______________________________________________________________________________________________________________________________________________________________

@bot.message_handler(commands=['monthdate','датанамесяц'])     # ВЫЗОВ КОМАНДЫ ДЛЯ ПОКАЗА ДАТЫ НА МЕСЯЦ
def handle_okey(message):
	msg = bot.send_message(message.chat.id, "Название команды? ")
	bot.register_next_step_handler(msg, commandAOAO)
	bot.send_message(message.chat.id, "Если ты передумал вводить на каком-либо этапе, то введи '-' или напиши 'Выход'")
def commandAOAO(message):
	global nameCommand
	global index
	index = 0
	nameCommand = message.text
	if nameCommand =="-" or nameCommand =="exit" or nameCommand=="выход" or nameCommand=="Выход":
		bot.send_message(message.chat.id, "Ладно.")
	else:
		try:
			with sqlite3.connect('HD.db') as con:
				cur = con.cursor()
				cur.execute("SELECT * FROM HD")
				for row in cur.fetchall():
					if row[0] == nameCommand:
						index+=1
				if index>0:
					msg = bot.send_message(message.chat.id, "Введи пароль, пожалуйста. Тебе должен был написать твой комнадир или тот, кто отвечает за игры.")
					bot.register_next_step_handler(msg, OPass)
				elif index==0:
					bot.send_message(message.chat.id, "Твоей команды нет в списке. Перейди к комане /setdate .")
		except UnboundLocalError:
			pass
def OPass(message):
	global index
	passwordCommand = message.text
	if passwordCommand =="-" or passwordCommand =="exit" or passwordCommand=="выход" or passwordCommand=="Выход":
		bot.send_message(message.chat.id, "Ладно.")
	else:
		try:
			passwordCommand = int(message.text)	
			with sqlite3.connect("HD.db") as con:
				cur = con.cursor()
				cur.execute("SELECT * FROM HD")
				for row in cur.fetchall():
					if nameCommand ==row[0] and int(passwordCommand)==row[3]:
						if row[1][3:5]==maneDate: # До этого момента выводит только все даты на настоящий месяц
							bot.send_message(message.chat.id, row[2] + " : "+row[1])
		except ValueError as e:
			pass

#_______________________________________________________________________________________________________________________________________________________________

@bot.message_handler(commands=['lookdate', 'ближдата']) # ВЫЗОВ БЛИЖАЙШЕЙ ДАТЫ
def handler_okey(message):
	msg = bot.send_message(message.chat.id, "Название команды? ")
	bot.register_next_step_handler(msg, OPassword)
	bot.send_message(message.chat.id, "Если ты передумал вводить на каком-либо этапе, то введи '-' или напиши 'Выход'")
def OPassword(message):
	global nameCommand
	global index
	index = 0
	nameCommand = message.text
	if nameCommand =="-" or nameCommand =="exit" or nameCommand=="выход" or nameCommand=="Выход":
		bot.send_message(message.chat.id,"Ладно.")
	else:
		try:
			with sqlite3.connect('HD.db') as con:
				cur = con.cursor()
				cur.execute("SELECT * FROM HD")
				for row in cur.fetchall():
					if row[0] == nameCommand:
						index+=1
				if index>0:
					msg = bot.send_message(message.chat.id, "Введи пароль, пожалуйста. Тебе должен был написать твой комнадир или тот, кто отвечает за игры.")
					bot.register_next_step_handler(msg, OMl)
				elif index==0:
					bot.send_message(message.chat.id, "Твоей команды нет в списке. Перейди к комане /setdate .")
		except UnboundLocalError:
			pass
def OMl(message):
	index=1
	secondIndex=0
	massivDate = []
	print(nameCommand)
	passwordCommand = message.text
	if passwordCommand =="-" or passwordCommand =='exit' or passwordCommand=="Exit" or passwordCommand =="Выход" or passwordCommand == 'выход':
		bot.send_message(message.chat.id, "Ладно.")
	with sqlite3.connect('HD.db') as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM HD")
		for row in cur.fetchall():
			if int(passwordCommand) == row[3]:
				print("Прошло")
				print(maneDate)
				print(row[1][3:5])
				if row[1][3:5]==maneDate:
					print("ПРОШЛО")
					massivDate.append(row[1])
					secondIndex+=1
				elif row[1][3:5]>=maneDate:
					bot.send_message(message.chat.id, "Твои события будут в других месяцах. " + row[2] +" : "+row[1]) 
		if int(passwordCommand)!= row[3] and secondIndex==0:
			bot.send_message(message.chat.id, "Пароль неправильный. Перепроверь. /lookdate")
		elif secondIndex>0:
			if row[3]==int(passwordCommand):
				otherMassivDate = massivDate[0][0:2]
				if "0" in otherMassivDate:
					firstDay = otherMassivDate.lstrip("0")
				else:
					firstDay = otherMassivDate
				nearestNumber = massivDate[0]
				for i in range(len(massivDate)):
					try:
						secondDay = massivDate[index][0:2]
						if "0" in secondDay:
							secondSecondDay = secondDay.lstrip("0")
						else:
							secondSecondDay = secondDay
						if int(firstDay)>int(secondSecondDay):
							otherMassivDate = massivDate[index][0:2]
							if "0" in otherMassivDate:
								firstDay = otherMassivDate.lstrip("0")
							else:
								firstDay = otherMassivDate
							nearestNumber = massivDate[index]
						index+=1
					except IndexError as e:
						pass
				bot.send_message(message.chat.id, nearestNumber)	
#_______________________________________________________________________________________________________________________________________________________________

@bot.message_handler(commands=['setdate',"установкадаты"])
def whatscommands(message):
	msg=bot.send_message(message.chat.id, "Введи название твоей команды. Если твоей команды нет в списке Базы данных, то Бот перенаправит тебя на регистрацию. ")
	bot.register_next_step_handler(msg, ifnameCommand)
	bot.send_message(message.chat.id, "Если ты передумал вводить что-то на каком-либо этапе, то введи '-' или напиши 'Выход'.")
def ifnameCommand(message):
	index=0
	global nameCommand
	nameCommand = message.text
	if any(x for x in '/' if x in nameCommand)==True:
		bot.send_message(message.chat.id,"Ты ввел команду для бота, а не название своей команды. Обратись к команде /setdate еще раз.")
	elif nameCommand =="-" or nameCommand =="exit" or nameCommand=="выход" or nameCommand=="Выход":
		bot.send_message(message.chat.id, "Ладно.")
	else:
		with sqlite3.connect('HD.db') as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM HD")
			for row in cur.fetchall():
				if row[0] == nameCommand:
					index+=1
			print(index)
			if index>0:
				msg = bot.send_message(message.chat.id, "Введи пароль, пожалуйста. Тебе должен был написать твой командир или тот, кто отвечает за игры.")
				bot.register_next_step_handler(msg, OPL)
			elif index==0:
				msg = bot.send_message(message.chat.id, "Твоей команды нет в списке. Придумай пароль в формате цифр для регистрации команды в Базе Данных. ") #НЕ РАБОТАЕТ И НЕ ПРОПУСКАЕТ
				bot.register_next_step_handler(msg, newCommand)
def newCommand(message):
	global passwordCommand
	try:
		passwordCommand = int(message.text)
		if passwordCommand =="-" or passwordCommand =='exit' or passwordCommand=="Exit" or passwordCommand =="Выход" or passwordCommand == 'выход':
			bot.send_message(message.chat.id, "Ладно.")
		else:
			msg = bot.send_message(message.chat.id,"""Хорошо, сообщи своим товарищам из команды, чтобы они смогли посмотреть даты. Но не сообщай другим людям!
Теперь напиши, когда проходит твое событие в формате ДД.ММ.ГГ . Пример: 20.07.19 или 20.07.2019.""")
			bot.register_next_step_handler(msg, whatsEvent)
	except ValueError as e:
		bot.send_message(message.chat.id, "Ты ввел не пароль. Перепроверь пароль и обратись к команде /setdate еще раз. ")

def OPL(message):
	index=0
	global passwordCommand
	global nameCommand
	global nameDate
	try:
		passwordCommand = message.text
		if passwordCommand =="-" or passwordCommand =='exit' or passwordCommand=="Exit" or passwordCommand =="Выход" or passwordCommand == 'выход':
			bot.send_message(message.chat.id, "Ладно.")
		else:
			with sqlite3.connect("HD.db") as con:
				cur = con.cursor()
				cur.execute("SELECT * FROM HD")
				for row in cur.fetchall():
					if row[3]==int(passwordCommand):
						index+=1
				if index>0:
					msg = bot.send_message(message.chat.id, "Подходит, продолжим. Какая дата? ")
					bot.register_next_step_handler(msg, whatsEvent)
				elif index==0:
					bot.send_message(message.chat.id, "Твоей команды нет в списке. Обратись к /setdate . ")
	except ValueError:
		pass
def whatsEvent(message):
	try:	
		global passwordCommand
		global nameCommand
		global nameDate
		nameDate = message.text
		if (len(nameDate)!=8 and len(nameDate)!=10):
			bot.send_message(message.chat.id, "Ты ввел не ту дату. Она должна быть в формате ДД.ММ.ГГ . Исправь. Используй команду /setdate ещё раз. ")
		elif nameDate == "-" or nameDate == "Выход" or nameDate == "выход":
			bot.send_message(message.chat.id, "Ладно.")
		elif any(x for x in wordUp if x in nameDate)==True:
			bot.send_message(message.chat.id, "Ты ввел не дату.")
		elif nameDate[6:]>=maneYear or maneDate>=maneyear[6:] or nameDate>=maneDate:
			msg = bot.send_message(message.chat.id, "А как называется событие? ")
			bot.register_next_step_handler(msg, writeAll)
	except ValueError as e:
		pass
def writeAll(message):
	try:
		global passwordCommand
		global nameCommand
		global nameDate
		global nameEvent
		nameEvent = message.text
		if nameEvent == "-" or nameEvent == "Выход" or nameEvent == "выход":
			bot.send_message(message.chat.id, "Ладно.")

		else:
			with sqlite3.connect('HD.db') as con:
				cur = con.cursor()
				cur.execute("INSERT INTO HD (nameCommand, DateEvent, Event, PasswordCommand) VALUES (?,?,?,?)",
					(nameCommand, nameDate, nameEvent,passwordCommand))
				con.commit()
				cur.close()
			con.close()
			bot.send_message(message.chat.id, "Готово!!!")
	except ValueError as e:
		pass
#_______________________________________________________________________________________________________________________________________________________________

@bot.message_handler(commands=['cpass'])
def changepassword(message):
	msg = bot.send_message(message.chat.id, "Название команды? ")
	bot.register_next_step_handler(msg, securityPassword)
def securityPassword(message):
	global nameCommand
	global index
	index = 0
	nameCommand = message.text
	if nameCommand =="-" or nameCommand =='exit' or nameCommand=="Exit" or nameCommand =="Выход" or nameCommand == 'выход':
		bot.send_message(message.chat.id, "Ладно")
	else:
		try:
			with sqlite3.connect('HD.db') as con:
				cur = con.cursor()
				cur.execute("SELECT * FROM HD")
				for row in cur.fetchall():
					if row[0] == nameCommand:
						index+=1
				if index>0:
					msg = bot.send_message(message.chat.id, "Введи пароль, пожалуйста. Тебе должен был написать твой комнадир или тот, кто отвечает за игры.")
					bot.register_next_step_handler(msg, OPL)
				elif index==0:
					bot.send_message(message.chat.id, "Твоей команды нет в списке. Перейди к комане /setdate .")
		except UnboundLocalError:
			pass	
def OPL(message):
	index=0
	global passwordCommand
	passwordCommand = int(message.text)	
	if passwordCommand =="-" or passwordCommand =='exit' or passwordCommand=="Exit" or passwordCommand =="Выход" or passwordCommand == 'выход':
		bot.send_message(message.chat.id, "Ладно")
	else:
		with sqlite3.connect("HD.db") as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM HD")
			for row in cur.fetchall():
				if row[3]==passwordCommand:
					index+=1
					#if nameCommand == row[0]:
					#	bot.send_message(message.chat.id, row[2] +" : " + row[1])
			if index>0:
				msg = bot.send_message(message.chat.id, "На какой пароль хочешь изменить?")
				bot.register_next_step_handler(msg, ChangePass)
			elif index==0:
				bot.send_message(message.chat.id, "Пароль не тот. Обратись к команде /cpass еще раз")
def ChangePass(message):
	try:
		changepassword=message.text
		if changepassword =="-" or changepassword =='exit' or changepassword=="Exit" or changepassword =="Выход" or changepassword == 'выход':
			bot.send_message(message.chat.id, "Ладно")
		else:
			with sqlite3.connect("HD.db") as con:
				cur = con.cursor()
				cur.execute("UPDATE HD SET PasswordCommand = (?) WHERE PasswordCommand=(?)", (int(changepassword), int(passwordCommand)))
				con.commit()
			bot.send_message(message.chat.id, "Готово! ")
	except ValueError as e:
		bot.send_message(message.chat.id, "Ты ввел не пароль в виде цифр. ")




#_______________________________________________________________________________________________________________________________________________________________

@bot.message_handler(commands=["deletedate", "удалениедаты"])
def DeleteDate(message):
	msg=bot.send_message(message.chat.id, "Название твоей команды? ")
	bot.register_next_step_handler(msg, LogPassword)
	bot.send_message(message.chat.id, "Если ты передумал вводить на каком-либо этапе, то введи '-' или напиши 'Выход'")
def LogPassword(message):
	index=0
	global nameCommand
	nameCommand = message.text
	with sqlite3.connect('HD.db') as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM HD")
		for row in cur.fetchall():
			if row[0] == nameCommand:
				index+=1
		if index>0:
			msg = bot.send_message(message.chat.id, "Введи пароль, пожалуйста. Тебе должен был написать твой комнадир или тот, кто отвечает за игры.")
			bot.register_next_step_handler(msg, iDontKnow)
		elif index==0:
			bot.send_message(message.chat.id, "Твоей команды нет в списке. Перейди к команде /writedate . ") #НЕ РАБОТАЕТ И НЕ ПРОПУСКАЕТ
def iDontKnow(message):
	index=0
	passwordCommand = message.text
	if passwordCommand =="-" or passwordCommand =='exit' or passwordCommand=="Exit" or passwordCommand =="Выход" or passwordCommand == 'выход':
		bot.send_message(message.chat.id, "Ладно")
	else:
		with sqlite3.connect("HD.db") as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM HD")
			for row in cur.fetchall():
				if row[3]==int(passwordCommand):
					index+=1
					if nameCommand == row[0]:
						bot.send_message(message.chat.id, row[2] +" : " + row[1])
			if index>0:
				for row in cur.fetchall():
					if nameCommand == row[0]:
						bot.send_message(message.chat.id, row[2] +" : " + row[1])
				msg = bot.send_message(message.chat.id, "Подходит, продолжим. Какую ДАТУ ты хочешь удалить?")
				bot.register_next_step_handler(msg, DeleteDate2)
				for row in cur.fetchall():
					if nameCommand == row[0]:
						bot.send_message(message.chat.id, row[2] +" : " + row[1])
			elif index==0:
				bot.send_message(message.chat.id, "Твоей команды нет в списке. Перейди к команде /setdate")
def DeleteDate2(message):
	deletedate = message.text
	with sqlite3.connect("HD.db") as con:
		cur = con.cursor()
		cur.execute("DELETE FROM HD WHERE DateEvent=(?)",(deletedate,))
		con.commit()
	bot.send_message(message.chat.id, "Готово!")

#_______________________________________________________________________________________________________________________________________________________________



@bot.message_handler(commands=['changedate'])
def changedate(message):
	msg=bot.send_message(message.chat.id, "Название твоей команды? ")
	bot.register_next_step_handler(msg, otherchangedate)
	bot.send_message(message.chat.id, "Если ты передумал вводить на каком-либо этапе, то введи '-' или напиши 'Выход'")
def otherchangedate(message):
	index=0
	global nameCommand
	nameCommand = message.text
	if nameCommand =="-" or nameCommand =='exit' or nameCommand=="Exit" or nameCommand =="Выход" or nameCommand == 'выход':
		bot.send_message(message.chat.id, "Ладно.")
	else:
		with sqlite3.connect('HD.db') as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM HD")
			for row in cur.fetchall():
				if row[0] == nameCommand:
					index+=1
			if index>0:
				msg = bot.send_message(message.chat.id, "Введи пароль, пожалуйста. Тебе должен был написать твой комнадир или тот, кто отвечает за игры.")
				bot.register_next_step_handler(msg, Okey)
			elif index==0:
				bot.send_message(message.chat.id, "Твоей команды нет в списке. Перейди к команде /setdate . ")
def Okey(message):
	index=0
	passwordCommand = int(message.text)	
	if passwordCommand =="-" or passwordCommand =='exit' or passwordCommand=="Exit" or passwordCommand =="Выход" or passwordCommand == 'выход':
		bot.send_message(message.chat.id, "Ладно")
	else:
		with sqlite3.connect("HD.db") as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM HD")
			for row in cur.fetchall():
				if row[3]==int(passwordCommand):
					index+=1
					if nameCommand == row[0]:
						bot.send_message(message.chat.id, row[2] +" : " + row[1])
			if index>0:
				for row in cur.fetchall():
					if nameCommand == row[0]:
						bot.send_message(message.chat.id, row[2] +" : " + row[1])
				msg = bot.send_message(message.chat.id, "Подходит, продолжим. Выбери ДАТУ, если хочешь изменить саму дату или название события. ")
				bot.register_next_step_handler(msg, definitionDateOrName)
			elif index==0:
				bot.send_message(message.chat.id, "Так, пароль не тот. Перепроверь. ")
def definitionDateOrName(message):
	global DoN
	DoN=message.text
	msg = bot.send_message(message.chat.id, "Ладно, меняем саму дату или название? Введи,например: 'Дата' или 'Событие'")
	bot.register_next_step_handler(msg, definitionOfChoice)

def definitionOfChoice(message):
	Choice = message.text
	if Choice =="-" or Choice =='exit' or Choice=="Exit" or Choice =="Выход" or Choice == 'выход':
		bot.send_message(message.chat.id, "Ладно.")
	elif Choice == "Дата" or Choice =="Дату" or Choice=="дата" or Choice =="дату" or Choice == "дат":
		msg = bot.send_message(message.chat.id, "На какую ДАТУ хочешь изменить? ")
		bot.register_next_step_handler(msg, updateDate)
	elif Choice == "Событие" or Choice == "событие" or Choice =="событи":
		msg = bot.send_message(message.chat.id, "На какое СОБЫТИЕ хочешь изменить?")
		bot.register_next_step_handler(msg, updateEvent)
def updateDate(message):
	updateDate = message.text
	if updateDate =="-" or updateDate =='exit' or updateDate=="Exit" or updateDate =="Выход" or updateDate == 'выход':
		bot.send_message(message.chat.id, "Ладно.")
	else:
		with sqlite3.connect("HD.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE HD SET DateEvent=(?) WHERE DateEvent=(?)",(updateDate, DoN))
			con.commit()
		bot.send_message(message.chat.id, "Готово!")

def updateEvent(message):
	updateEvent = message.text
	if updateEvent =="-" or updateEvent =='exit' or updateEvent=="Exit" or updateEvent =="Выход" or updateEvent == 'выход':
		bot.send_message(message.chat.id, "Ладно.")
	else:
		with sqlite3.connect("HD.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE HD SET Event=(?) WHERE DateEvent=(?)",(updateEvent, DoN))
			con.commit()
		bot.send_message(message.chat.id, "Готово!")




#_______________________________________________________________________________________________________________________________________________________________


@bot.message_handler(commands=['instruction','инструкция', "Инструкция"])
def instruction(message):
	bot.send_message(message.chat.id, "Бот ещё не оптимизирован, чтобы можно было использовать его без проблем. СЛЕДУЙТЕ ИНСТРУКЦЯМ, ПОЖАЛУЙСТА. ")
	bot.send_message(message.chat.id, """При вводе /setdate нужно указать сначала название вашей команды. По типу 'Мск Лис' или похожее.
Пожалуйста, не усложняйте название для ваших друзей и сокомандников.
После Вам нужно будет ввести пароль, если вашей команды нет в Базе Данных, то Вас перенаправит на регистрацию команды в эту Базу.
Никакие данные не разглашаются.
После регистрации или проверки пароля - Вас перенаправит на ввод ДАТЫ события. Вводите в формате ДД.ММ.ГГ . Пример: 28.04.2019
Дальше Вам потребуется ввести НАЗВАНИЕ события.
Пожалуйста, большая просьба, не пишите в матном или оскорбительной форме. В будущем это будет пресекаться.""")
	bot.send_message(message.chat.id, """При вводе /lookdate - Вам покажут ближайшую дату события. Пожалуйста, удаляйте событие после того момента, как это событие прошло.
При вводе команды /deletedate - Вам будет предоставлена функция удаления даты. Просьба не баловаться, дабы не взбесить своих друзей.
При вводе команды /monthdate - Просмотр дат и собитый в настоящий месяц.
При вводе команды /changedate - Изменение даты или названия события.""")
	bot.send_message(message.chat.id, """Для связи,если что-то не работает или хотите поддержать финансово:
Vk - https://vk.com/h4zci
Instagram - @huzzky
Почта - vladislav.bychkov01@gmail.com
Telegram - @Huzkey
Спасибо за внимание. 
Пользуйтесь ботом в удовольствие.""")



#_______________________________________________________________________________________________________________________________________________________________

#Вызов фотографии
@bot.message_handler(commands=['info',"информация","инфо","инфа"])
def sendphoto(message):
	photo = open('1.jpeg', 'rb')
	photo2 = open('Huskey.jpg', 'rb')
	bot.send_photo(message.chat.id, photo)
	bot.send_photo(message.chat.id, photo2)
	bot.send_message(message.chat.id, "Создатель бота @Huzkey. Член команды МСК Л.И.С.")
	print(message.from_user.first_name)
#_______________________________________________________________________________________________________________________________________________________________


@bot.message_handler(commands = ['random',"рандом"])
def randomMessage(message):
	x = random.random()*10
	bot.send_message(message.chat.id ,int(x))
	print(message.from_user.first_name)

#_______________________________________________________________________________________________________________________________________________________________

#Кнопки
markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
itembtn1 = types.KeyboardButton(' /time ') #Название кнопки 1 
itembtn2 = types.KeyboardButton(' /lookdate') #Название кнопки 2 
itembtn3 = types.KeyboardButton(' /setdate')
itembtn4 = types.KeyboardButton(' /help') #Название кнопки 3 
itembtn5 = types.KeyboardButton(' /end')
markup.add(itembtn1, itembtn2, itembtn3, itembtn4 ,itembtn5) #Занесение кнопок на сервер



#_______________________________________________________________________________________________________________________________________________________________
bot.polling()
