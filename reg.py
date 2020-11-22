from telebot import types
from config import bot, updateId
from handlers import mainMenu
from SQLite import SQLreg

name, skills, lowSkills = '', '', ''
age, course = 0, 0


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
        bot.register_next_step_handler(message, course_reg)


def course_reg(message):
    global course
    while True:
        try:
            course = int(message.text)
        except ValueError:
            bot.send_message(message.from_user.id, "Введи цифрами!")
            bot.register_next_step_handler(message, course_reg)
        finally:
            break
    if course != 0:
        bot.register_next_step_handler(message, result)


def result(message):
    global url
    url = message.text
    bot.send_message(message.from_user.id,
                     "Получается, тебя зовут " + name + "\nТвой возраст: " + str(age) +
                     "\nТы учишься на " + str(course) + " курсе")
    keyboard = types.ReplyKeyboardMarkup()
    keyButton = types.InlineKeyboardButton(text="Да")
    keyboard.add(key_yes)
    keyButton = types.InlineKeyboardButton(text="Нет")
    keyboard.add(key_no)
    bot.send_message(message.from_user.id, text="Все верно?", reply_markup=keyboard)
    bot.register_next_step_handler(message, answer)


def answer(message):
    if message.text == "Да":
        user_id = updateId(message)
        SQLreg(user_id, name, url, age, course)
        bot.send_message(message.from_user.id, "Приятно познакомиться")
        mainMenu(message)

    elif message.text == "Нет":
        bot.send_message(message.from_user.id, "Давай попробуем еще раз!\nКак тебя зовут?")
        bot.register_next_step_handler(message, name_register)
