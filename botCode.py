import telebot
from telebot import types

# token1 = 1337741156:AAEAXiceoDUDxtQloBS1L3_rYp9SpWUnhc
# token2 = 1431032404:AAFL8WHpn2dJryplX4Bc5oUA3iiWj9WjfqA
name, skills, lowSkills = '', '', ''
age, course = 0, 0

bot = telebot.TeleBot("1431032404:AAFL8WHpn2dJryplX4Bc5oUA3iiWj9WjfqA")


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привет, как тебя зовут ?")
    user_id = message.from_user.id


@bot.message_handler(func=lambda m: True, content_types=['text'])
def name_register(message):
    global name
    name = message.text
    bot.send_message(message.chat.id, "Окей, сколько тебе лет?")
    bot.register_next_step_handler(message, age_reg)


def age_reg(message):
    global age
    while True:
        try:
            age = int(message.text)
        except ValueError:
            bot.send_message(message.chat.id, "Введи цифрами!")
            bot.register_next_step_handler(message, age_reg)
        finally:
            break
    if age != 0:
        bot.send_message(message.chat.id, "Неплохо, а на каком ты курсе?")
        bot.register_next_step_handler(message, course_reg)


def course_reg(message):
    global course
    while True:
        try:
            course = int(message.text)
        except ValueError:
            bot.send_message(message.chat.id, "Введи цифрами!")
            bot.register_next_step_handler(message, course_reg)
        finally:
            break
    if course != 0:
        bot.send_message(message.chat.id, "В каких предметах ты силен?")
        bot.register_next_step_handler(message, skills_reg)


def skills_reg(message):
    global skills
    skills = message.text
    bot.send_message(message.chat.id, "Осталось совсем немного\nА в каких предметах ты разбираешься хуже всего?")
    bot.register_next_step_handler(message, result)


def result(message):
    global lowSkills
    lowSkills = message.text

    bot.send_message(message.chat.id, "Получается, тебя зовут "
                     + name + "\nТвой возраст: " + str(age)
                     + "\nТы учишься на " + str(course)
                     + " курсе" + "\nТвоя биография:"
                     + "\n" + skills + "\n" + lowSkills)

    keyboard = types.ReplyKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text="Да")
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text="Нет")
    keyboard.add(key_no)
    bot.send_message(message.chat.id, text="Все верно ?", reply_markup=keyboard)
    bot.register_next_step_handler(message, answer)


def answer(message):
    if message.text == "Да":
        bot.send_message(message.chat.id, "Приятно познакомиться, я записал тебя в БД :)")
    elif message.text == "Нет":
        global name, skills, lowSkills, age, course
        name, skills, lowSkills = '', '', ''
        age, course = 0, 0
        bot.send_message(message.chat.id, "Давай попробуем еще раз!")
        bot.send_message(message.chat.id, "Как тебя зовут ?")
        bot.register_next_step_handler(message, name_register)


bot.polling()
