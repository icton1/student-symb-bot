import telebot

TOKEN = "1431032404:AAGS9MagsZ9mVTKGk9rluaAYpdOA-ZQOQ_M"
bot = telebot.TeleBot(TOKEN)

def updateUsername(message):
    return message.from_user.username


def updateId(message):
    return int(message.from_user.id)
