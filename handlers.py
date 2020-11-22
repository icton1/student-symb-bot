from telebot import types
from config import bot, updateId, updateUsername
from SQLite import taskCostSQL, offerTaskSQL, userInfoSQL, SQLreg, addToInProcessSQL, showInProcess

section = ''
subject = ''
difficulty = ''
money = ''
name = ''
age, course = 0, 0


def mainMenu(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyButton = types.InlineKeyboardButton(text="Выполнить задание")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Дать задание")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Информация о профиле")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Информация о заданиях")
    keyboard.add(keyButton)
    bot.send_message(message.from_user.id, "Выбирай", reply_markup=keyboard)


def doTask(message):
    global section
    section = message.text
    keyboard = types.ReplyKeyboardMarkup()
    key_firstBestLesson = types.InlineKeyboardButton(text="Математика")
    keyboard.add(key_firstBestLesson)
    key_secondBestLesson = types.InlineKeyboardButton(text="Информатика")
    keyboard.add(key_secondBestLesson)
    key_anotherLesson = types.InlineKeyboardButton(text="Физика")
    keyboard.add(key_anotherLesson)

    bot.send_message(message.from_user.id, "Выбери предмет", reply_markup=keyboard)

    bot.register_next_step_handler(message, taskDifficulty)


def taskDifficulty(message):
    global subject
    subject = message.text

    keyboard = types.ReplyKeyboardMarkup()
    keyButton = types.InlineKeyboardButton(text="Легкая")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Средняя")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Сложная")
    keyboard.add(keyButton)

    bot.send_message(message.from_user.id, "Выбери сложность задания", reply_markup=keyboard)
    global section
    if section == "Выполнить задание":
        bot.register_next_step_handler(message, chooseTask)
    elif section == "Дать задание":
        bot.register_next_step_handler(message, giveTask)


def chooseTask(message):
    global difficulty, subject, money
    difficulty = message.text
    user_username = updateUsername(message)
    money = taskCostSQL(subject, difficulty)
    keyboard = types.ReplyKeyboardMarkup()
    if len(money) == 0:
        bot.send_message(message.from_user.id, "К сожалению, заданий нет по выбранным критериям нет",
                         reply_markup=keyboard)
        mainMenu(message)
    else:
        keyboard = types.InlineKeyboardMarkup()
        for i in money:
            cost = i[0]
            output = "Стоимость задания: " + str(cost) + " монет"
            link = "https://t.me/" + user_username
            keyButton = types.InlineKeyboardButton(text=output, url=link, callback_data=addToInProcessSQL(cost, user_username, subject, difficulty))
            keyboard.add(keyButton)
        bot.send_message(message.from_user.id, text="Выбери задание", reply_markup=keyboard)
        keyboard = types.ReplyKeyboardMarkup()
        keyButton = types.InlineKeyboardButton(text="Вернуться в меню")
        keyboard.add(keyButton)
        bot.send_message(message.chat.id, "Либо вернись в меню", reply_markup=keyboard)
        bot.register_next_step_handler(message, mainMenu)


def giveTask(message):
    global difficulty
    difficulty = message.text
    bot.send_message(message.from_user.id, "Сколько монет заплатишь за выполнение?", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, giveMoney)


def giveMoney(message):
    global money, subject, difficulty, user_id
    while True:
        try:
            money = int(message.text)
        except ValueError:
            bot.send_message(message.from_user.id, "Введи корректно!")
            bot.register_next_step_handler(message, giveMoney)
        finally:
            break
    if money >= 0:
        user_id = updateId(message)
        offerTaskSQL(user_id, subject, difficulty, money)
        mainMenu(message)


def userInfo(message, user_id):
    information = userInfoSQL(user_id)
    name = information[0][0]
    age = information[1][0]
    course = information[2][0]
    money = information[3][0]
    bot.send_message(message.from_user.id,
                     "Получается, тебя зовут " + name + "\nТвой возраст: " + str(age) +
                     "\nТы учишься на " + str(course) + " курсе\nИ на твоем счету " + str(money) + "монет")
    keyboard = types.ReplyKeyboardMarkup()
    keyButton = types.InlineKeyboardButton(text="Да")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Нет")
    keyboard.add(keyButton)
    bot.send_message(message.from_user.id, text="Все верно?", reply_markup=keyboard)
    bot.register_next_step_handler(message, answer)


def start(message):
    bot.send_message(message.from_user.id, "Привет, как тебя зовут?")
    bot.register_next_step_handler(message, name_register)


def name_register(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Окей, сколько тебе лет?")
    bot.register_next_step_handler(message, age_reg)


def age_reg(message):
    global age
    while True:
        try:
            age = int(message.text)
        except ValueError:

            bot.send_message(message.from_user.id, "Введи цифрами!")
            bot.register_next_step_handler(message, age_reg)
        finally:
            break
    if age != 0:
        bot.send_message(message.from_user.id, "Неплохо, а на каком ты курсе?")
        bot.register_next_step_handler(message, result)


#def course_reg(message):


def result(message):
    global course
    while True:
        try:
            course = int(message.text)
        except ValueError:
            bot.send_message(message.from_user.id, "Введи цифрами!")
            bot.register_next_step_handler(message, result)
        finally:
            break
    if course != 0:
        bot.send_message(message.from_user.id,
                         "Получается, тебя зовут " + name + "\nТвой возраст: " + str(age) +
                         "\nТы учишься на " + str(course) + " курсе")
        keyboard = types.ReplyKeyboardMarkup()
        keyButton = types.InlineKeyboardButton(text="Да")
        keyboard.add(keyButton)
        keyButton = types.InlineKeyboardButton(text="Нет")
        keyboard.add(keyButton)
        bot.send_message(message.from_user.id, text="Все верно?", reply_markup=keyboard)
        bot.register_next_step_handler(message, answer)


def answer(message):
    if message.text == "Да":
        user_id = updateId(message)
        user_username = updateUsername(message)
        SQLreg(user_id, name, user_username, age, course)
        bot.send_message(message.from_user.id, "Приятно познакомиться")
        mainMenu(message)

    elif message.text == "Нет":
        bot.send_message(message.from_user.id, "Давай попробуем еще раз!\nКак тебя зовут?", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, name_register)


def taskInfo(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyButton = types.InlineKeyboardButton(text="Выполняемые мной")
    keyboard.add(keyButton)
    keyButton = types.InlineKeyboardButton(text="Переданные на выполнение")
    keyboard.add(keyButton)
    bot.send_message(message.from_user.id, text="Какие именно задания ты хочешь посмотреть?", reply_markup=keyboard)
    bot.register_next_step_handler(message, myTask)


def myTask(message):
    user_username = updateUsername(message)
    if message.text == "Выполняемые мной":
        information = showInProcess(user_username)
        bot.send_message(message.from_user.id, "Стоимость задания: " + str(information[0][0][0]) + "\nПредмет: " +
                         information[1][0][0] + "\nСложность: " + information[2][0][0])
        keyboard = types.ReplyKeyboardMarkup()
        keyButton = types.InlineKeyboardButton(text="Вернуться в меню")
        keyboard.add(keyButton)
        bot.send_message(message.chat.id, "Возврат в меню", reply_markup=keyboard)
        bot.register_next_step_handler(message, mainMenu)
    elif message.text == "Переданные на выполнение":
        print(2)