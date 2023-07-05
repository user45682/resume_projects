import openai
import telebot
import sqlite3
import time

openai.api_key = 'YOUR_API_KEY'
bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_API')
conn = sqlite3.connect("users.db",check_same_thread=False)
cursor = conn.cursor()


while True:
    @bot.message_handler(commands=['start'])
    def start(message):
        all = message.from_user.id
        cursor.execute(f"SELECT all_users FROM all_users WHERE all_users = {all}")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO all_users (all_users) VALUES (?)", (all,))
        conn.commit()

    @bot.message_handler(commands=['add'])
    def add(message):
            if message.from_user.id == 1464977458:
                mess=int(message.text[-10:])
                try:
                    cursor.execute("INSERT INTO users (user_id) VALUES (?)", (mess,))
                    bot.send_message(chat_id=message.from_user.id, text="User added successfully.")
                except:
                    bot.send_message(chat_id=message.from_user.id, text="Данный пользователь уже находится в базе данных")
                conn.commit()

            else:
                bot.send_message(chat_id=message.from_user.id, text="Вы не имеете доступа к этой команде.")


    @bot.message_handler(commands=['del'])
    def add(message):
        if message.from_user.id == 1464977458:
            mess = int(message.text[-10:])
            cursor.execute(f"SELECT user_id FROM users WHERE user_id = {mess}")
            if cursor.fetchone() is None:
                bot.send_message(chat_id=message.from_user.id, text="Данный пользователь не находится в базе данных")
            else:
                cursor.execute("DELETE FROM users WHERE user_id=?", (mess,))
                bot.send_message(chat_id=message.from_user.id, text="Пользователь удален из БД")
            conn.commit()

        else:
            bot.send_message(chat_id=message.from_user.id, text="Вы не имеете доступа к этой команде.")


    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        iduser = int(message.from_user.id)
        cursor.execute(f"SELECT user_id FROM users WHERE user_id = {iduser}")
        if cursor.fetchone() is None:
            bot.send_message(chat_id=message.from_user.id,
                             text='Извините, вы не имеете доступа к данному боту. Для получения доступа обратитесь к Администратору @ChatGPT_3_Acs')
        else:
                response = openai.Completion.create(
                    model='text-davinci-003',
                    prompt=message.text,
                    temperature=0.5,
                    max_tokens=2000,
                    top_p=1.0,
                    frequency_penalty=0.5,
                    presence_penalty=0.0,
                )
                bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])


    try:
        bot.polling()
    except:
        print(ValueError)