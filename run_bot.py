import telebot
import random
from telebot import types
import speech_recognition as sr
import os
import uuid

language = 'ru_RU'
bot = telebot.TeleBot('5889845611:AAGuXmV69LYKKh8IHxJ1TlMCn0bfXjjMHMw')
r = sr.Recognizer()

'''
def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text,language=language)
            print('Перевожу голосовое сообщение в текст ...')
            print(text)
            return text
        except:
            print('Что-то пошло не так.. Попробуйте снова...')
            return "Что-то пошло не так.. Попробуйте снова..."
'''

#Команда приветствия при старте + стикер
@bot.message_handler(commands=['start'])
def welcome(message):

    username = message.from_user.username

    # keyboard (обычная)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("😊 Как дела?")
    markup.add(item1, item2) #Добавляем объект марка при помощи метода add

    bot.send_message(message.chat.id,f'Добро пожаловать, {username}!\nЯ умею конвертировать голосовые сообщения в текст,\n'
                                     f'А также еще кое-что😊', parse_mode='html',reply_markup=markup)

'''
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full="./voice/"+filename+".ogg"
    file_name_full_converted="./ready/"+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    text=recognise(file_name_full_converted)
    bot.reply_to(message, text)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)
    '''


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id ,
            str(random.randint(0,100)))
        elif message.text == '😊 Как дела?':

#Инлайновая клавиатура
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            markup.add(item1, item2) #Прикрепил инлайновуюклавиатуру методом add

            bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')

@bot.callback_query_handler(func=lambda call: call.data == "good")
def good_pressed(call: types.CallbackQuery):
    bot.send_message(chat_id=call.message.chat.id, text="Это просто отлично!")

@bot.callback_query_handler(func=lambda call: call.data == "bad")
def good_pressed(call: types.CallbackQuery):
    bot.send_message(chat_id=call.message.chat.id, text="Что стряслось?")

bot.polling(none_stop=True)