from config import bot, updateId, updateUsername
from SQLite import botStart, registration
from handlers import mainMenu, doTask, userInfo, start, taskInfo


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = updateId(message)
    user_username = updateUsername(message)
    botStart()
    if registration(user_id, user_username):
        start(message)
    else:
        bot.send_message(message.from_user.id, "Рады видеть тебя вновь")
        mainMenu(message)


@bot.message_handler(content_types=['text'])
def allMenu(message):
    botStart()
    user_id = updateId(message)
    if message.text == 'Выполнить задание' or message.text == 'Дать задание':
        doTask(message)
    elif message.text == 'Информация о профиле':
        userInfo(message, user_id)
    elif message.text == "Информация о заданиях":
        taskInfo(message)
bot.polling()
