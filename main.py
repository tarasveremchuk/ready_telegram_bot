import base64
import json
import random
from io import BytesIO
import io
import re
import datetime
import os
import telebot
import webbrowser

import threading
import sqlite3
import time

import telebot
from telebot import types
file = open('./mytoken.txt')
mytoken = file.read()
bot = telebot.TeleBot(mytoken)
answers = ['Я не зрозумів,що ти хочеш сказати.', 'Вибач,я не зрозумів тебе.', 'Я не знаю цієї команди.',
           'Мій творець не казав,як відповідати на цю ситуацію... >_<']

# Обработка команды /start
allowed_user_id = 788388571

global_time = None
@bot.message_handler(commands=['start'])
def welcome(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
            id INTEGER
            )""")
    connect.commit()

    user_id = [message.chat.id]
    cursor.execute("INSERT INTO login_id VALUES (?);", user_id)
    connect.commit()

    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Продати 💸')
    button2 = types.KeyboardButton('Мої замовлення 🧳')
    button6 = types.KeyboardButton('Звернутися до підтримки 📝')

    button3 = types.KeyboardButton('Як все працює❓')
    button4 = types.KeyboardButton('Про нас 👥')
    button5 = types.KeyboardButton("Відправити ціну")
    # Разделяю кнопки по строкам так, чтобы товары были отдельно от остальных кнопок
    markup.row(button1)
    markup.row(button2)
    markup.row(button3, button4)
    markup.row(button6)
    if user_id == 788388571 or user_id==5792353056 or user_id==5792353056:
        button7 = types.KeyboardButton("Адмін панель 👀")
        markup.row(button7)

    if message.text == '/start':
        bold_text = f"Привіт , *{message.from_user.first_name}*! Це *жирний* і *ще один* жирний текст."

        # bot.send_message(message.chat_id, text=bold_text, parse_mode=telegram.ParseMode.MARKDOWN)
        # Отправляю приветственный текст
        bot.send_message(message.chat.id,
                         f'Привіт 👋, *{message.from_user.first_name}*!\nЛаскаво просимо до нашого інноваційного телеграм-бота "SndSkup"!\nТут тобі вдасться продати твій одяг всього лише в декілька кліків 😉.',reply_markup=markup,
                         parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, 'Закинув тебе в головне меню,вибирай!', reply_markup=markup)


# Обработка обычных текстовых команд, описанных в кнопках
@bot.message_handler()
def info(message):
    if message.text == 'Продати 💸':
        goodsChapter(message)
    elif message.text == 'Як все працює❓':
        settingsChapter(message)
    elif message.text == 'Мої замовлення 🧳':
        my_items(message)
    elif message.text == 'Про нас 👥':
        infoChapter(message)
    elif message.text == 'Орест лох':
        OrestLoh(message)
    elif message.text == "Відправити ціну":
        handle_send_price(message)
    elif message.text == "Оплата на карту":
        handle_send_money(message)
    elif message.text == "Встановити час":
        handle_start(message)
    elif message.text=="Відмовити замовлення":
        handle_cancel_order(message)
    elif message.text=="Неправильний ТТН":
        handle_bad_ttn(message)
    elif message.text=="Пошук замовлень":
        handle_find_order(message)
    elif message.text=="Відправити розсилку":
        send_broadcast_message(message)
    elif message.text == "☑️ Речі які ми купуємо ☑️":
        handle_buying_items(message)
    elif message.text == "✅ Я відправив усі фото":
         check_and_update_status(message)
    elif message.text=="Адмін панель 👀":
        adminPanel(message)
    elif message.text == 'Скачать базу':
        extract_and_send_data(message)
    elif message.text=="Заповнити базу":
        add_photo_data_manually()
    elif message.text == '❓Як ми оцінюємо товар❓':
        OtsinkaTovaru(message)







    elif message.text == '📷 Відправити фото 📸':
        conn2 = sqlite3.connect('photos.db')
        cursor2 = conn2.cursor()

        cursor2.execute('''
                                      CREATE TABLE IF NOT EXISTS photos (
                                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                                          user_id INTEGER,
                                          file BLOB,
                                          order_number INTEGER,
                                          price INTEGER,
                                          status INTEGER,
                                          delivery TEXT,
                                          date_order DATETIME,
                                          nomer_ttn INTEGER,
                                          nomer_card INTEGER,
                                          price_status TEXT,
                                          name_order TEXT,
                                          asstimated_time INTEGER   
                                      )
                                  ''')
        conn2.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button2 = types.KeyboardButton('✅ Я відправив усі фото')
        # markup.row(button2)
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button3 = types.KeyboardButton('↩️ Назад до меню')
        markup.row(button2, button3)
        conn = sqlite3.connect('photos.db')
        cursor = conn.cursor()
        global last_order_number
        last_order_number = None
        # Оновлюємо номер замовлення
        cursor.execute('SELECT MAX(order_number) FROM photos')
        result = cursor.fetchone()[0]
        if result is None:
            last_order_number = 1
        else:
            last_order_number = int(result) + 1
        sentPhotoChapter(message)

        @bot.message_handler(content_types=['photo'])
        def handle_photo(message):
            conn = sqlite3.connect('photos.db')
            cursor = conn.cursor()
            # Створення таблиці для збереження фотографій
            cursor.execute('''
                                   CREATE TABLE IF NOT EXISTS photos (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       user_id INTEGER,
                                       file BLOB,
                                       order_number INTEGER,
                                       price INTEGER,
                                       status INTEGER,
                                       delivery TEXT,
                                       date_order DATETIME,
                                       nomer_ttn INTEGER,
                                       nomer_card INTEGER,
                                       price_status TEXT,
                                       name_order TEXT,
                                       asstimated_time INTEGER
                                   )
                               ''')
            conn.commit()
            if message.photo:
                # Отримання ідентифікатора користувача
                user_id = message.from_user.id


                # Отримання фотографії з повідомлення
                photo = message.photo[-1]

                # Отримання файлу фотографії
                file_info = bot.get_file(photo.file_id)
                file = bot.download_file(file_info.file_path)

                # Кодування фотографії в base64
                encoded_photo = base64.b64encode(file)

                # Якщо це перше фото або кнопка "Відправити фото" була натиснута, створюємо новий номер замовлення

                status = 8  # Значення статусу 8

                cursor.execute(
                    'INSERT INTO photos (user_id, file, order_number, price, status, delivery, nomer_ttn,price_status) '
                    'VALUES (?, ?, ?, ?, ?, ?,  ?,?)',
                    (user_id, encoded_photo, last_order_number, None, status, None, None, None))

                conn.commit()

                order_message = f"Користувач @{message.from_user.username}  хоче продати річ\nНомер замовлення: {last_order_number}\n З ІД:"
                bot.send_message(chat_id='-917631518', text=order_message)

                order_message2 = f"{message.chat.id}"
                bot.send_message(chat_id='-917631518', text=order_message2)

                # Відправлення фотографії до групи
                bot.send_photo(chat_id='-917631518', photo=photo.file_id)
                bot.send_message(chat_id='-4009484644', text=order_message)
                bot.send_message(chat_id='-4009484644', text=order_message2)
                bot.send_photo(chat_id='-4009484644', photo=photo.file_id)






            cursor.close()
            conn.close()












    elif message.text == 'Звернутися до підтримки 📝':
            # Сюда можете ввести свою ссылку на Телеграмм, тогда пользователя будет перекидывать к вам в личку
            # webbrowser.open('https://t.me/sndskup')
            username = '@sndskup'  # Замініть <user_id> на ідентифікатор користувача
            profile_link = f'{username}'
            bot.send_message(chat_id=message.chat.id, text='Натисни на посилання, щоб звернутися до підтримки:',
                             disable_web_page_preview=True)
            bot.send_message(chat_id=message.chat.id, text=profile_link)


    elif message.text == '↩️ Назад':
        goodsChapter(message)
    elif message.text == '↩️ Назад до меню':
        welcome(message)
    # Если пользователь написал свое сообщение, то бот рандомно генерирует один из возможных вариантов ответа
    # Добавлять и редактировать варианты ответов можно в списке answers
    else:
        bot.send_message(message.chat.id, answers[random.randint(0, 3)])


def handle_start(message):
    if message.from_user.id == 788388571 or message.from_user.id == 5792353056 or message.from_user.id ==5792353056:
        # Функція, що обробляє команду /start
        bot.send_message(message.chat.id, "Введіть час очікування : ")
        bot.register_next_step_handler(message, handle_text)
    else:
        bot.reply_to(message, 'У вас немає доступу до цієї команди.')



def handle_text(message):
    # Функція, що обробляє текстові повідомлення
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_times (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            global_time TEXT
        )
    ''')

    # Збереження змін до бази даних
    conn.commit()
    global global_time  # Дозволяємо функції використовувати глобальну змінну

    try:
        user_input = message.text
        # Тут можна додати логіку для перевірки правильності формату часу

        global_time = user_input  # Зберігаємо введений час у глобальну змінну
        cursor.execute('''
            INSERT INTO saved_times (global_time)
            VALUES (?)''', (global_time,))
        conn.commit()
        bot.send_message(message.chat.id, f"Ви ввели час: {global_time} хвилин")

    except ValueError:
        bot.send_message(message.chat.id, "Некоректний формат часу. Спробуйте ще раз.")
# def update_estimated_time(message):
#     conn = sqlite3.connect('photos.db')
#     cursor = conn.cursor()
#     # Отримуємо всі записи з таблиці "photos"
#     cursor.execute("SELECT id FROM photos")
#     rows = cursor.fetchall()
#     estimated_time = 60
#
#     order_message = f"Час очікування було встановлено: {estimated_time}"
#     bot.send_message(chat_id=message.chat.id, text=order_message)
#     # Проходимося по кожному запису та оновлюємо поле "asstimated_time"
#     for row in rows:
#         photo_id = row[0]
#         # Припустимо, що ми хочемо встановити estimated_time в 60 хвилин для кожного запису
#
#         # Оновлюємо поле "asstimated_time" для кожного запису
#         cursor.execute("UPDATE photos SET asstimated_time = ? WHERE id = ?", (estimated_time, photo_id))
#
#     # Зберігаємо зміни
#     conn.commit()




def extract_and_send_data(message):
    if message.from_user.id == 788388571 or message.from_user.id == 5792353056 or message.from_user.id ==5792353056:
        # З'єднання з базою даних
        conn = sqlite3.connect('photos.db')
        cursor = conn.cursor()

        # Отримання всіх записів з бази даних
        cursor.execute('SELECT * FROM photos')
        rows = cursor.fetchall()

        # Створення текстового представлення даних
        data_text = "Дані з бази даних:\n"
        for row in rows:
            data_text += f"ID: {row[0]}\n"
            data_text += f"User ID: {row[1]}\n"
            data_text += f"File: {row[2]}\n"
            data_text += f"Order Number: {row[3]}\n"
            data_text += f"Price: {row[4]}\n"
            data_text += f"Status: {row[5]}\n"
            data_text += f"Delivery: {row[6]}\n"
            data_text += f"Date Order: {row[7]}\n"
            data_text += f"Tracking Number: {row[8]}\n"
            data_text += f"Card Number: {row[9]}\n"
            data_text += f"Price Status: {row[10]}\n"
            data_text += f"Name Order: {row[11]}\n"
            data_text += f"Estimated Time: {row[12]}\n"
            data_text += "\n"  # Роздільник між записами

        # Збереження у файл database34
        with open('database34', 'a') as file:
            file.write(data_text)
            file.write('\n')  # Додаємо символ нового рядка між записами

        # Отримання абсолютного шляху до файлу
        absolute_file_path = os.path.abspath('database34')

        with open(absolute_file_path, 'rb') as file:
            bot.send_document(message.chat.id, document=file)

        # Поділ тексту на частини (максимальний розмір повідомлення Telegram - 4096 символів)
        max_message_length = 4096
        chunks = [data_text[i:i + max_message_length] for i in range(0, len(data_text), max_message_length)]
    else:
        bot.send_message(message.chat.id,"Я не знаю такої команди")
        # Відправлення кожної частини тексту
        # for chunk in chunks:
        #     bot.send_message(message.chat.id, text=chunk)

        # Виклик функції з потрібними параметрами (chat_id та bot)


def check_and_update_status(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()

    cursor.execute('''
            SELECT status, order_number
            FROM photos
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 1
        ''', (user_id,))

    row = cursor.fetchone()

    if row is not None:
        status, order_number = row
        if status == 8:
            cursor.execute('UPDATE photos SET status = 9 WHERE order_number = ? AND user_id = ?',
                           (order_number, message.from_user.id))
            conn.commit()
            est_time = get_global_time()
            # bot.send_message(message.chat.id, '✅ Твої фото були успішно завантажені 😌\n\n'
            #                                   '📍Щоб переглянути статус вашого товару перейди до розділу "Мої замовлення".\n\n'
            #                                   '📍Один з наших працівників розгляне твою пропозицію та запропонує тобі найкращу ціну, роблячи це максимально швидко 🚀')
            hide_markup = types.ReplyKeyboardRemove()
            # bot.send_message(message.chat.id, f'* Середній час очікування: {est_time} хвилин *',parse_mode='Markdown')

            bot.send_message(message.chat.id,'''*Придумай назву для замовлення.*

Наприклад:
Футболка червона Nike vintage L.\n\n‼️Без назви замовлення *оголошення не буде відправлено* на розгляд‼️''', parse_mode='Markdown', reply_markup=hide_markup )
            bot.register_next_step_handler(message, process_name_order,order_number)

        else:
            bot.send_message(message.chat.id, 'УПС.... Ти не завантажив фотографій!')
    else:
        bot.send_message(message.chat.id, 'УПС.... Ти не завантажив фотографій!')

    # Приховуємо панель з кнопками


    conn.close()
def get_global_time():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT global_time FROM saved_times ORDER BY id DESC LIMIT 1")
        global_time = cursor.fetchone()
        conn.close()

        if global_time:
            return global_time[0]  # Повертаємо значення global_time
        else:
            return None

    except sqlite3.Error as e:
        print("Виникла помилка при спробі отримати global_time:", str(e))
        return None

def check_photos(message):
    penultimate_message = message.history[-2]
    if penultimate_message.photo:
        bot.send_message(message.chat.id, 'Thanks, I received your photos.')
    else:
        bot.send_message(message.chat.id, 'Please send me your photos first.')
def check_for_photos2(message):
  """Check if a message contains photos.

  Args:
    message: The Telegram message to check.

  Returns:
    A string, "Yes" if the message contains photos, "No" if the message does not contain photos.

  """

  bot.send_message(message.chat.id, message.text)
  if message.photo:
      bot.send_message(message.chat.id, '+" ')
  else:
      bot.send_message(message.chat.id, '-" ')


def adminPanel(message):
    if message.chat.id == allowed_user_id or message.chat.id==5792353056:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Відправити ціну')
        button2 = types.KeyboardButton('Відправити розсилку')
        button3 = types.KeyboardButton('Пошук замовлень')
        button5 = types.KeyboardButton('Відмовити замовлення')
        button6 = types.KeyboardButton('Неправильний ТТН')
        button8 = types.KeyboardButton('Встановити час ')

        button4 = types.KeyboardButton('↩️ Назад до меню')
        button7 = types.KeyboardButton('Скачати базу')
        button9 = types.KeyboardButton('Оплата на карту')

        markup.row(button1, button2)
        markup.row(button3,button5)
        markup.row(button8,button6)
        markup.row(button4,button9)

        bot.send_message(message.chat.id, 'Ти перейшов у розділ Адмін панель', reply_markup=markup)


def goodsChapter(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('☑️ Речі які ми купуємо ☑️')
        button2 = types.KeyboardButton('📷 Відправити фото 📸')
        button3 = types.KeyboardButton('❓Як ми оцінюємо товар❓')
        button4 = types.KeyboardButton('↩️ Назад до меню')
        markup.row(button1)
        markup.row(button2)
        markup.row(button3)
        markup.row(button4)
        bot.send_message(message.chat.id, 'Ти перейшов у розділ "Продати річ" ', reply_markup=markup)




last_messages = []





def send_previous_message(message):
    previous_message = message.get_message(-2)
    bot.send_message(message.chat.id, previous_message.text)
def settingsChapter(message):
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # button3 = types.KeyboardButton('↩️ Назад до меню')
        # markup.row(button3)
        bot.send_message(message.chat.id,
                         'Натисни "Продати" ➡️ ”Відправити фото” та надішли нам потрібні фото своєї речі.\n\n'
                         '🚀 Наші колеги оперативно розглянуть твою пропозицію та запропонують найкращу можливу ціну.\n\n'
                         '👀 У розділі "Мої замовлення" зможеш відстежувати статус своєї пропозиції.\n\n'
                         '💳 Якщо запропонована ціна підходить, обери зручний спосіб доставки:\n'
                         '  - Доставка через систему\n'
                         '  - Доставка наложним платежем\n'
                         '  - Доставка з повною оплатою на карту (в розробці)\n\n'
                         '📦 Після відправлення товару, надай номер накладної, номер карти (у випадку, якщо ти обрав доставку через систему) натиснувши:  “Мої замовлення” ➡️ “Відправити номер карти” “Відправити номер накладної”.\n\n'
                         '💰Ми оперативно перерахуємо кошти на твою карту після отримання товару.')



# Функція для перевірки, чи користувач відправив фотографії до бази даних за останні 30 секунд
def check_photos(update, context):
    message = update.message

    # Перевіряємо, чи містить повідомлення зображення
    if message.photo:
        # Якщо є фотографії, можемо продовжити обробку
        # Тут ви можете додати ваш код для обробки фотографій
        # наприклад, збереження їх, виведення додаткових питань тощо
        pass
    else:
        # Якщо фотографій немає, надсилаємо повідомлення користувачеві
        message.reply_text("Ти повинен надіслати фотографію своїх речей, щоб продати її в магазині.")

def process_name_order(message, order_number):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton('↩️ Назад до меню')
    markup.row(button2)
    name_order = message.text
    reply_text = f"Ти надіслав назву до замовлення #{order_number}: {name_order}!"
    bot.send_message(message.chat.id, reply_text, reply_markup=markup)  # Відправка разом з кнопкою

    # Збереження номера ТТН у базу даних
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE photos SET name_order = ? WHERE order_number = ? AND user_id = ?',
                   (name_order, order_number, message.from_user.id))
    conn.commit()
    conn.close()

    # Відправляємо відповідь користувачу
    user_id = message.from_user.id
    est_time = get_global_time()
    bot.send_message(message.chat.id, '✅ *Твої фото та назва* були успішно завантажені 😌\n\n'
                                      '📍*Щоб переглянути статус* вашого товару перейди до розділу "Мої замовлення".\n\n'
                                      '📍Один з наших працівників розгляне твою пропозицію та запропонує тобі найкращу ціну, роблячи це максимально швидко 🚀', parse_mode='Markdown')
    hide_markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, f'* Середній час очікування: {est_time} хвилин *', parse_mode='Markdown')



    conn2 = sqlite3.connect('photos.db')
    cursor2 = conn2.cursor()

    cursor2.execute('''
                SELECT status, order_number
                FROM photos
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT 1
            ''', (user_id,))

    row = cursor2.fetchone()

    if row is not None:
        status, order_number = row
        if status == 8:
            cursor2.execute('UPDATE photos SET status = 9 WHERE order_number = ? AND user_id = ?',
                           (order_number, message.from_user.id))
            conn2.commit()




    # Приховуємо панель з кнопками
    reply_text2 = f"Користувач @{message.from_user.username} назву до замовлення #{order_number}: {name_order}!"

    chatid='-917631518'
    bot.send_message(chatid, reply_text2, reply_markup=markup)
    bot.send_message('-4009484644', reply_text2, reply_markup=markup)



def check_photos_sent(user_id):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()

    # Отримуємо поточний час
    current_time = datetime.datetime.now()

    # Отримуємо час, який був 30 секунд тому
    thirty_seconds_ago = current_time - datetime.timedelta(seconds=15)

    # Перевіряємо, чи є фотографії, які були збережені для даного користувача у проміжку від thirty_seconds_ago до current_time
    cursor.execute('SELECT COUNT(*) FROM photos WHERE user_id = ? AND datetime(date_order) >= datetime(?) AND datetime(date_order) <= datetime(?)',
                   (user_id, thirty_seconds_ago, current_time))
    result = cursor.fetchone()[0]
    conn.close()
    #fds
    return result > 0

@bot.message_handler(commands=['start', 'help', 'anything'])
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    time.sleep(2)

    if not check_photos(message):
        # Відправляємо повідомлення користувачеві, якщо немає фотографій
        bot.send_message(message.chat.id, "Надішліть фотографії речей, які ви хочете продати.")
    else:
        # Тут ви можете обробити повідомлення з фотографіями
        # Наприклад, зберегти фотографії або відповісти щось інше
        bot.send_message(message.chat.id, "Дякую! Ви надіслали фотографії. Тепер можемо продовжити.")

# Обробник натискання кнопки "Я відправив усі фото"


# @bot.message_handler(func=lambda message: message.text == 'Я відправив усі фото')
# def handle_all_photos_sent(message):
#     user_id = message.from_user.id
#
#     # Викликаємо функцію для перевірки, чи користувач відправив фотографії за останні 30 секунд
#     photos_sent = check_photos_sent(user_id)
#
#     if photos_sent:
#      send_all_photos(message)
#     else:
#         bot.send_message(chat_id=message.chat.id, text="Вибачте виникла помилка. Спробуйте ще раз!")
#         sentPhotoChapter(message)
#         global last_order_number
#         last_order_number = None
#
#         @bot.message_handler(content_types='photo')
#         def get_photo(message):
#             conn = sqlite3.connect('photos.db')
#             cursor = conn.cursor()
#
#             # Створення таблиці для збереження фотографій, якщо вона ще не існує
#             cursor.execute('''
#                         CREATE TABLE IF NOT EXISTS photos (
#                             id INTEGER PRIMARY KEY AUTOINCREMENT,
#                             user_id INTEGER,
#                             file BLOB,
#                             order_number INTEGER,
#                             price INTEGER,
#                             status INTEGER,
#                             delivery TEXT,
#                             date_order DATETIME,
#                             nomer_ttn INTEGER
#                         )
#                     ''')
#             conn.commit()
#
#             if message.photo:
#                 # Отримання ідентифікатора користувача
#                 user_id = message.from_user.id
#
#                 # Отримання фотографії з повідомлення
#                 photo = message.photo[-1]
#
#                 # Отримання файлу фотографії
#                 file_info = bot.get_file(photo.file_id)
#                 file = bot.download_file(file_info.file_path)
#
#                 # Кодування фотографії в base64
#                 encoded_photo = base64.b64encode(file)
#
#                 global last_order_number
#
#                 # Якщо це перше фото або кнопка "Відправити фото" була натиснута, створюємо новий номер замовлення
#                 if last_order_number is None or message.text == 'Відправити фото речей':
#                     # Оновлюємо номер замовлення
#                     cursor.execute('SELECT MAX(order_number) FROM photos')
#                     result = cursor.fetchone()[0]
#                     if result is None:
#                         last_order_number = 1
#                     else:
#                         last_order_number = int(result) + 1
#
#                 # Збереження фотографії в базу даних з номером замовлення та поточною датою і часом
#                 current_datetime = datetime.datetime.now()
#                 cursor.execute('INSERT INTO photos (user_id, file, order_number, date_order) VALUES (?, ?, ?, ?)',
#                                (user_id, encoded_photo, last_order_number, current_datetime))
#                 conn.commit()
#
#                 # Відправлення повідомлення про замовлення до групи
#                 order_message = f"Користувач @{message.from_user.username} хоче продати річ\n" \
#                                 f"Номер замовлення #{last_order_number}"
#                 bot.send_message(chat_id='-917631518', text=order_message)
#
#                 # Відправлення фотографії до групи
#                 bot.send_photo(chat_id='-917631518', photo=photo.file_id)
#
#             cursor.close()
#             conn.close()
# # Функция, отвечающая за раздел помощи
def sentPhotoChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton('✅ Я відправив усі фото')
    markup.row(button2)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button3 = types.KeyboardButton('↩️ Назад до меню')
    markup.row(button2,button3)
    bot.send_message(message.chat.id, '''📍 Відправ нам наступні фото:

1️⃣ Надішли фото товару (речі) *ззаду та спереду*.

2️⃣ Надішли фото *верхніх бирок.*

3️⃣ Надішли фото *нижніх бирок* (якщо такі присутні).

4️⃣ Надішли фото *недоліків.*''', parse_mode='Markdown')

    text = "*‼️Відправляйте лише правдиві фото та всі недоліки‼️*\nНе гайте ні нашого, ні вашого часу. Кожна річ буде ретельно перевірена на пошті."
    text2 = "Після того як *завантажив необхідні фото, натисни* “✅ Я відправив усі фото”."


    bot.send_message(message.chat.id, text,reply_markup=markup,parse_mode='Markdown')
    bot.send_message(message.chat.id, text2,reply_markup=markup,parse_mode='Markdown')



def infoChapter(message):
        word1 = "  "
        bot.send_message(message.chat.id, f'''        
                {word1}Про нас 🙃

Ми - команда експертів, які спеціалізуються на скупці різного "вінтажного" та "кежуального" шмоту. Наша мета - надати вам зручну та вигідну можливість продати непотрібні речі та отримати за них реальну вартість. 💰

*Чому обрати нас?* 🌟

*Широкий спектр речей:* Ми приймаємо до розгляду різноманітні види одягу, включаючи верхній одяг, штани, інколи взуття, аксесуари та багато іншого. 👕👖👟

*Справедлива оцінка:* Ми цінуємо ваші товари і ретельно оцінюємо їх, враховуючи бренд, стан та популярність. Наші професіонали гарантують справедливу вартість для ваших речей. 💎📈

*Простий процес продажу:* Ми зробили процес продажу максимально простим і зручним для вас. Ви надсилаєте нам фото товару, отримуєте оцінку, погоджуєтеся з ціною та обираєте спосіб доставки. Ми стежимо за кожним кроком, щоб ви отримали гарну взаємовигідну угоду. 📸✅🚚

*Надійна та швидка оплата:* Після прийняття вашого товару та підтвердження угоди, ми швидко перераховуємо гроші на ваш рахунок. Ми розуміємо, що час - цінний ресурс, тому ми робимо все можливе, щоб оплата була здійснена швидко та надійно. 💸⏱️

Ми пишаємося нашою командою експертів, яка зосереджена на вашому задоволенні та впевнена, що забезпечить вам зручний та вигідний досвід продажу. Приєднуйтесь до нашої спільноти і давайте разом знайдемо нове призначення для вашого непотрібного одягу! 💼''',
                         parse_mode='Markdown')





def send_all_photos(message):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()

    # Отримання останнього номера замовлення
    cursor.execute('SELECT MAX(order_number) FROM photos')
    result = cursor.fetchone()[0]
    if result is None:
        last_order_number = 1
    else:
        last_order_number = int(result)

    # Вибірка фотографій для певного номера замовлення
    cursor.execute('SELECT file FROM photos WHERE order_number = ?', (last_order_number,))
    photo_records = cursor.fetchall()

    if len(photo_records) > 0:
        for photo_record in photo_records:
            encoded_photo = photo_record[0]
            photo_data = base64.b64decode(encoded_photo)

            # Відправлення фотографій до групи
            # bot.send_photo(chat_id='-917631518', photo=io.BytesIO(photo_data))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button2 = types.KeyboardButton('↩️ Назад до меню')
        markup.row(button2)
        bot.send_message(message.chat.id, '✅ Ваші фото були успішно завантажені 😌\n\n'
                                          '📍Щоб переглянути статус пропозиції перейди до розділу "Мої замовлення".\n\n'
                                          '📍Один з наших працівників розгляне вашу пропозицію та запропонує вам найкращу ціну, роблячи це максимально швидко 🚀',
                         reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Надіслати фото')
        markup.row(button1)

        bot.send_message(message.chat.id, 'Ви не надіслали жодної фотографії! Надішліть фото.',
                         reply_markup=markup)

    cursor.close()
    conn.close()


def OrestLoh(message):
    bot.send_message(message.chat.id, 'Так я з вами згоден,що Орест Лох, а також він МАВПА!')


def OtsinkaTovaru(message):
    text2 = "‼️*Як проходить оцінка товару?  🤔*\n\n" \
            "При оцінці вашого товару ми звертаємо увагу на три основні фактори:\n\n" \
            "*Фірма (модель):* Один з ключових аспектів - це бренд та модель товару. Відомі фірми та популярні моделі зазвичай мають більшу вартість. Якщо ваш товар належить до відомої фірми або популярної моделі, це вплине позитивно на оцінку. 👍\n\n" \
            "*Розмір:* Розмір товару також має значення при оцінці. Деякі розміри можуть бути більш популярними або рідкісними, що впливає на їхню ціну. Наприклад, розмір, який важко знайти або дуже популярний, може мати вищу ціну порівняно зі звичайними розмірами. 📏\n\n" \
            "*Стан:* Стан товару є важливим чинником в оцінці. Чим кращий стан товару, тим більша ймовірність, що його оцінять вище. Товари у відмінному стані, майже нові або з мінімальними ознаками використання, зазвичай мають вищу оцінку. 😊\n\n" \
            "" \
            "*‼️ Зверніть свою увагу на розділ “Речі які ми купуємо”‼️* \n" \
            "(”Продати” ➡️ ”Речі які ми купуємо”), у цьому розділі ви зможете побачити речі які ми скуповуємо з найвищим пріоритетом, на той чи інший час." \
            "" \
            ""
    bot.send_message(message.chat.id, text2 ,parse_mode='Markdown')




@bot.message_handler(func=lambda message: message.text.startswith('Мої речі'))
def my_items(message):
        conn = sqlite3.connect('photos.db')
        cursor = conn.cursor()

        # Отримання ідентифікатора користувача
        user_id = message.from_user.id

        # Отримання унікальних order_id користувача з бази даних
        cursor.execute('SELECT DISTINCT order_number FROM photos WHERE user_id = ?', (user_id,))
        order_numbers = cursor.fetchall()

        if order_numbers:
            for order_number in order_numbers:
                order_number = order_number[0]

                # Отримання статусу для кожного order_id користувача
                cursor.execute(
                    'SELECT status, price, file, nomer_ttn,delivery, nomer_card,name_order FROM photos WHERE user_id = ? AND order_number = ?',
                    (user_id, order_number))
                status_record = cursor.fetchone()
                name_order = status_record[6] if status_record[6] is not None else 'Ще немає'

                if status_record:
                    status = status_record[0]
                    price = status_record[1] if status_record[1] is not None else 'Ще немає'
                    photo_data = base64.b64decode(status_record[2])
                    ttn_number = status_record[3] if status_record[3] is not None else 'Ще немає'
                    delivery_field = status_record[4] if status_record[4] is not None else 'Ще немає'
                    card_number = status_record[5] if status_record[5] is not None else 'Ще немає'
                    name_order = status_record[6] if status_record[6] is not None else 'Ще немає'
                    ttn_status20 = get_ttn_status(order_number)
                    card_status20 = get_card_status(order_number)
                    ttn_and_card_status20 = get_ttn_and_card_status(order_number)
                    if status == 1:
                        caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️  *Статус:* Пропозицію була подана на розгляд 😼\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}"
                        bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                       reply_markup=markup, parse_mode='Markdown')
                    elif status == 2:
                        caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Ціна очікує вашого підтвердження 👀\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}"
                        bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                       parse_mode='Markdown')
                    elif status == 3:
                        caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Ціну було підтверджено ✅\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}"
                        bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                       parse_mode='Markdown')
                    elif get_ttn_status(order_number) is None and delivery_field == 'Доставка наложним платежем':
                        caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Замовлення очікує на відправку 😶‍🌫️\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}"

                        # Створення кнопки "Відправити номер ТТН"
                        markup = types.InlineKeyboardMarkup()
                        ttn_button = types.InlineKeyboardButton("Прикріпити номер накладної",
                                                                callback_data=f"ttn_{order_number}")
                        markup.add(ttn_button)

                        # Відправка повідомлення з фото, текстом та кнопкою
                        bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                       reply_markup=markup, parse_mode='Markdown')

                    elif ttn_status20 is not None and delivery_field == 'Доставка наложним платежем' and status == 25:
                        caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Товар в дорозі 📦\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}"

                        # Створення кнопки "Відправити номер ТТН"
                        markup = types.InlineKeyboardMarkup()
                        ttn_button = types.InlineKeyboardButton("Редагувати номер накладної",
                                                                callback_data=f"ttn1_{order_number}")
                        markup.add(ttn_button)

                        # Відправка повідомлення з фото, текстом та кнопкою
                        bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                       reply_markup=markup, parse_mode='Markdown')
                    elif ttn_status20 is None and card_status20 is None and delivery_field == 'Доставка через систему':
                        # Створення першого об'єкту markup і додавання до нього першої кнопки
                        markup = types.InlineKeyboardMarkup()
                        ttn_button = types.InlineKeyboardButton("Прикріпити номер накладної",
                                                                callback_data=f"ttn_{order_number}")
                        markup.add(ttn_button)

                        # Створення другого об'єкту markup і додавання до нього другої кнопки
                        ttn_button2 = types.InlineKeyboardButton('Прикріпити номер вашої карти',
                                                                 callback_data=f"card_{order_number}")
                        markup.add(ttn_button2)

                        # Ваш підготовлений caption
                        caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Замовлення очікує на відправку 😶‍🌫️\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер карти:* {card_number}"

                        # Відправка повідомлення з фото, текстом та об'єктом markup
                        bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                       reply_markup=markup, parse_mode='Markdown')
                    elif ttn_status20 is not None and card_status20 is None and delivery_field == 'Доставка через систему':
                        # Створення першого об'єкту markup і додавання до нього першої кнопки
                        markup = types.InlineKeyboardMarkup()
                        ttn_button = types.InlineKeyboardButton("Редагувати номер накладної",
                                                                callback_data=f"ttn1_{order_number}")
                        markup.add(ttn_button)

                        # Створення другого об'єкту markup і додавання до нього другої кнопки
                        ttn_button2 = types.InlineKeyboardButton('Прикріпити номер вашої карти',
                                                                 callback_data=f"card_{order_number}")
                        markup.add(ttn_button2)

                        # Ваш підготовлений caption
                        caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Товар в дорозі 📦\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер карти:* {card_number}"

                        # Відправка повідомлення з фото, текстом та об'єктом markup
                        bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                       reply_markup=markup, parse_mode='Markdown')
                    elif ttn_status20 is None and card_status20 is not None and delivery_field == 'Доставка через систему':
                        # Створення першого об'єкту markup і додавання до нього першої кнопки
                        markup = types.InlineKeyboardMarkup()
                        ttn_button = types.InlineKeyboardButton("Прикріпити номер накладної",
                                                                callback_data=f"ttn_{order_number}")
                        markup.add(ttn_button)

                        # Створення другого об'єкту markup і додавання до нього другої кнопки
                        ttn_button2 = types.InlineKeyboardButton('Редагувати номер вашої карти',
                                                                 callback_data=f"card1_{order_number}")
                        markup.add(ttn_button2)

                        # Ваш підготовлений caption
                        caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Товар в дорозі 📦\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер карти:* {card_number}"

                        # Відправка повідомлення з фото, текстом та об'єктом markup
                        bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                       reply_markup=markup, parse_mode='Markdown')
                    elif ttn_status20 is not None and card_status20 is not None and delivery_field == 'Доставка через систему':
                        # Створення першого об'єкту markup і додавання до нього першої кнопки
                        markup = types.InlineKeyboardMarkup()
                        ttn_button = types.InlineKeyboardButton("Редагувати номер накладної",
                                                                callback_data=f"ttn1_{order_number}")
                        markup.add(ttn_button)

                        # Створення другого об'єкту markup і додавання до нього другої кнопки
                        ttn_button2 = types.InlineKeyboardButton('Редагувати номер вашої карти',
                                                                 callback_data=f"card1_{order_number}")
                        markup.add(ttn_button2)

                        # Ваш підготовлений caption
                        caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Товар в дорозі 📦\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер карти:* {card_number}"

                        # Відправка повідомлення з фото, текстом та об'єктом markup
                        bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                       reply_markup=markup, parse_mode='Markdown')

                    # elif status==5:
                    #     # Створення першого об'єкту markup і додавання до нього першої кнопки
                    #     markup = types.InlineKeyboardMarkup()
                    #     ttn_button = types.InlineKeyboardButton("Відправте номер накладної", callback_data=f"ttn_{order_number}")
                    #     markup.add(ttn_button)
                    #
                    #     # Створення другого об'єкту markup і додавання до нього другої кнопки
                    #     ttn_button2 = types.InlineKeyboardButton('Відправте номер вашої карти',callback_data=f"card_{order_number}")
                    #     markup.add(ttn_button2)
                    #
                    #     # Ваш підготовлений caption
                    #     caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Відправлення в дорозі 📦\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер карти:* {card_number}"
                    #
                    #     # Відправка повідомлення з фото, текстом та об'єктом markup
                    #     bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                    #                    reply_markup=markup, parse_mode='Markdown')

                    # elif status==6:
                    #     # Створення першого об'єкту markup і додавання до нього першої кнопки
                    #     markup = types.InlineKeyboardMarkup()
                    #     ttn_button = types.InlineKeyboardButton("Прикріпити номер накладної", callback_data=f"ttn_{order_number}")
                    #     markup.add(ttn_button)
                    #
                    #     # Створення другого об'єкту markup і додавання до нього другої кнопки
                    #     ttn_button2 = types.InlineKeyboardButton('Відправте номер вашої карти',callback_data=f"card_{order_number}")
                    #     markup.add(ttn_button2)
                    #
                    #     # Ваш підготовлений caption
                    #     caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Відправлення в дорозі 📦\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер карти:* {card_number}"
                    #
                    #     # Відправка повідомлення з фото, текстом та об'єктом markup
                    #     bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                    #                    reply_markup=markup, parse_mode='Markdown')

                    elif get_card_status(order_number) is None and delivery_field == 'Доставка через систему':
                        # Створення першого об'єкту markup і додавання до нього першої кнопки
                        markup = types.InlineKeyboardMarkup()

                        # Створення другого об'єкту markup і додавання до нього другої кнопки
                        ttn_button2 = types.InlineKeyboardButton('Прикріпити номер вашої карти',
                                                                 callback_data=f"card_{order_number}")
                        markup.add(ttn_button2)

                        # Ваш підготовлений caption
                        caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Замовлення очікує на відправку 😶‍🌫️\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер карти:* {card_number}"

                        # Відправка повідомлення з фото, текстом та об'єктом markup
                        bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                       reply_markup=markup, parse_mode='Markdown')
                    elif card_status20 is not None and delivery_field == 'Доставка через систему' and status == 25:
                        # Створення першого об'єкту markup і додавання до нього першої кнопки
                        markup = types.InlineKeyboardMarkup()

                        # Створення другого об'єкту markup і додавання до нього другої кнопки
                        ttn_button2 = types.InlineKeyboardButton('Редагувати номер вашої карти',
                                                                 callback_data=f"card1_{order_number}")
                        markup.add(ttn_button2)

                        # Ваш підготовлений caption
                        caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Товар в дорозі 📦\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер карти:* {card_number}"

                        # Відправка повідомлення з фото, текстом та об'єктом markup
                        bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                       reply_markup=markup, parse_mode='Markdown')
                    else:
                        caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Назва товару:* {name_order}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Пропозиція на розгляді 😼\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Запропонована ціна:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}"

                        # Отримання першого фото для кожного order_id користувача
                        cursor.execute('SELECT file FROM photos WHERE user_id = ? AND order_number = ? LIMIT 1',
                                       (user_id, order_number))
                        photo_record = cursor.fetchone()

                        if photo_record:
                            encoded_photo = photo_record[0]
                            photo_data = base64.b64decode(encoded_photo)

                            # Формування повідомлення з фото та текстом
                            bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                           parse_mode='Markdown')
                        else:
                            bot.reply_to(message, f"Не знайдено фото для замовлення з номером {order_number}")

                else:
                    bot.reply_to(message, f"Не знайдено статусу для замовлення з номером {order_number}")
        else:
            bot.reply_to(message,
                         f"*У тебе ще немає жодного замовлення.* \n\n*Щоб створити замовлення* натисни:      \n”Продати” ➡️ “Відправити фото”.",
                         parse_mode="Markdown")







@bot.callback_query_handler(func=lambda call: call.data.startswith('ttn_'))
def handle_ttn_number(call):
    order_number = call.data.split('_')[1]

    if get_ttn_status(order_number) is None:
        bot.send_message(call.message.chat.id, 'Прикріпити номер накладної\n               ⬇️⬇️⬇️')

        # Реєструємо функцію, яка буде обробляти наступне повідомлення користувача
        bot.register_next_step_handler(call.message, save_ttn_number, order_number)
    else:
        bot.send_message(call.message.chat.id, 'Ви уже відправляли номер ТТН!')



@bot.callback_query_handler(func=lambda call: call.data.startswith('ttn1_'))
def handle_edit_ttn_number(call):
    order_number = call.data.split('_')[1]

    if get_ttn_status(order_number) is not None:
        bot.send_message(call.message.chat.id, 'Редагувати номер накладної\n               ⬇️⬇️⬇️')

        # Реєструємо функцію, яка буде обробляти наступне повідомлення користувача
        bot.register_next_step_handler(call.message, edit_ttn_number, order_number)
    else:
        bot.send_message(call.message.chat.id, 'УПС.... Виникла помилка!')


def save_ttn_number(message, order_number):
        # Отримуємо введений користувачем номер ТТН
        if get_ttn_status(order_number) is None:

            ttn_number = message.text
            # Збереження номера ТТН у базу даних
            conn = sqlite3.connect('photos.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE photos SET nomer_ttn = ?, status = 25 WHERE order_number = ? AND user_id = ?',
                           (ttn_number, order_number, message.from_user.id))
            conn.commit()
            conn.close()

            # Відправляємо відповідь користувачу
            reply_text = f"Ти надіслав номер накладної ТТН: {ttn_number}. Номер ТТН збережено."
            bot.send_message(message.chat.id, reply_text)
            bot.send_message(-917631518,
                             f"Користувач @{message.chat.username} відправив номер накладної {ttn_number}. Номер замовлення: #{order_number}")
            bot.send_message(-4009484644,
                             f"Користувач @{message.chat.username} відправив номер накладної {ttn_number}. Номер замовлення: #{order_number}")
        else:
            bot.send_message(message.chat.id,
                             f"Номер ТТН уже було збережено")


def edit_ttn_number(message, order_number):

    # Отримуємо введений користувачем номер ТТН
    if get_ttn_status(order_number) is not None:

        ttn_number = message.text
        # Збереження номера ТТН у базу даних
        conn = sqlite3.connect('photos.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE photos SET nomer_ttn = ?, status = 13 WHERE order_number = ? AND user_id = ?',
                       (ttn_number, order_number, message.from_user.id))
        conn.commit()
        conn.close()

        # Відправляємо відповідь користувачу
        reply_text = f"Твій новий номер накладної ТТН: {ttn_number}. Номер ТТН збережено."
        bot.send_message(message.chat.id, reply_text)
        bot.send_message(-917631518,
                         f"Користувач @{message.chat.username} відредагував номер накладної {ttn_number}. Номер замовлення: #{order_number}")
        bot.send_message(-4009484644,
                         f"Користувач @{message.chat.username} відредагував номер накладної {ttn_number}. Номер замовлення: #{order_number}")
    else:
        bot.send_message(message.chat.id,
                         f"Номер ТТН уже було збережено")



@bot.callback_query_handler(func=lambda call: call.data.startswith('card_'))
def handle_card_number(call):
    order_number = call.data.split('_')[1]

    if get_card_status(order_number) is None:
        bot.send_message(call.message.chat.id, 'Прикріпити номер вашої карти\n '
                                               '                    ⬇️⬇️⬇️'
                         )

        # Реєструємо функцію, яка буде обробляти наступне повідомлення користувача
        bot.register_next_step_handler(call.message, save_card_number, order_number)
    else:
        bot.send_message(call.message.chat.id,
                         f"УПС....Виникла помилка!")
@bot.callback_query_handler(func=lambda call: call.data.startswith('card1_'))
def handle_card_edit_number(call):
    order_number = call.data.split('_')[1]

    if get_card_status(order_number) is not None:
        bot.send_message(call.message.chat.id, 'Редагувати номер вашої карти\n '
                                               '                    ⬇️⬇️⬇️'
                         )

        # Реєструємо функцію, яка буде обробляти наступне повідомлення користувача
        bot.register_next_step_handler(call.message, edit_card_number, order_number)
    else:
        bot.send_message(message.chat.id,
                         f"УПС....Виникла помилка!")
def save_card_number(message, order_number):

    # Отримуємо введений користувачем номер ТТН
    if get_card_status(order_number) is None:

        card_number = message.text

        # Збереження номера ТТН у базу даних
        conn = sqlite3.connect('photos.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE photos SET nomer_card = ?, status = 25 WHERE order_number = ? AND user_id = ?',
                       (card_number, order_number, message.from_user.id))
        conn.commit()
        conn.close()

        # Відправляємо відповідь користувачу
        reply_text = f"Ти надіслав номер своєї карти: {card_number}. Номер карти збережено."
        bot.send_message(message.chat.id, reply_text)
        bot.send_message(-917631518,
                         f"Користувач @{message.chat.username} з ід {message.chat.id} відправив номер своєї карти: {card_number}\nНомер замовлення: {order_number}"
                         )

        bot.send_message(-4009484644,
                         f"Користувач @{message.chat.username} з ід {message.chat.id} відправив номер своєї карти: {card_number}\nНомер замовлення: {order_number}"
                         )
    else:
        bot.send_message(message.chat.id,
                         f"Номер карти уже було збережено")


def edit_card_number(message, order_number):

    # Отримуємо введений користувачем номер ТТН
    if get_card_status(order_number) is not None:

        card_number = message.text

        # Збереження номера ТТН у базу даних
        conn = sqlite3.connect('photos.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE photos SET nomer_card = ?, status = 13 WHERE order_number = ? AND user_id = ?',
                       (card_number, order_number, message.from_user.id))
        conn.commit()
        conn.close()

        # Відправляємо відповідь користувачу
        reply_text = f"Ти надіслав новий номер своєї карти: {card_number}. Номер карти збережено."
        bot.send_message(message.chat.id, reply_text)
        bot.send_message(-917631518,
                         f"Користувач @{message.chat.username} з ід {message.chat.id} відредагував номер своєї карти: {card_number}\nНомер замовлення: {order_number}"
                         )

        bot.send_message(-4009484644,
                         f"Користувач @{message.chat.username} з ід {message.chat.id} відредагував номер своєї карти: {card_number}\nНомер замовлення: {order_number}"
                         )
    else:
        bot.send_message(message.chat.id,
                         f"Номер карти уже було збережено")

@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def handle_callback_query(call):
    message = call.message
    status1 = get_price_status(current_order_number)

    owner_id = message.chat.id
    group_id = '-917631518'  # Замініть на фактичний ID вашої групи
    if call.data == 'yes':
        if status1 == 15 or status1 is None :
            send_delivery_options(message, owner_id, group_id)
            update_price_status(current_order_number, 14)  # Змінити статус на 4

        elif status1==14 :
            bot.send_message(message.chat.id,"Ти вже зробив вибір")


    elif call.data == 'no':
        if get_price_status(current_order_number) is None:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button3 = types.KeyboardButton('↩️ Назад до меню')

            markup.row(button3)
            bot.send_message(message.chat.id,
                             "Ми поважаємо твоє рішення. \n\n📍Один з працівників ознайомиться з твоїм замовленням, та *можливо буде запропонована інша ціна*.",parse_mode='Markdown', reply_markup=markup)
            update_price_status(current_order_number, 14)  # Змінити статус на 3

            propose_price(message, owner_id, group_id)
            handle_your_price(message)
            # bot.register_next_step_handler(message, handle_your_price)


        else:
            bot.send_message(message.chat.id,"Ти вже зробив вибір")




def handle_your_price(message):
    hide_markup = types.ReplyKeyboardRemove()

    bot.reply_to(message, 'Введіть бажану ціну: ',reply_markup=hide_markup )
    bot.register_next_step_handler(message, process_your_price,current_order_number)


def process_your_price(message, current_order_number):
    if message.text.isdigit():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button2 = types.KeyboardButton('↩️ Назад до меню')
        markup.row(button2)
        group_id = '-917631518'
        price = message.text  # Отримуємо ідентифікатор користувача з повідомлення
        bot.send_message(group_id,
                         f"Користувач @{message.chat.username} запропонував свою ціну {price} грн\nНомер замовлення: {current_order_number}")

        bot.send_message(-4009484644,
                         f"Користувач @{message.chat.username} запропонував свою ціну {price} грн\nНомер замовлення: {current_order_number}")
        bot.reply_to(message, '📍Один з працівників ознайомиться з твоєю пропозицію і повідомить тебе!', reply_markup=markup)
    elif message.text=="↩️ Назад до меню":
        welcome(message)



def send_delivery_options(message, owner_id, group_id):
    # Відправити повідомлення з вибором способу доставки
    markup = types.InlineKeyboardMarkup(row_width=2)
    delivery_option1 = types.InlineKeyboardButton('Доставка #1', callback_data='delivery_option1')
    delivery_option2 = types.InlineKeyboardButton('Доставка #2', callback_data='delivery_option2')
    markup.add(delivery_option1, delivery_option2)
    bot.send_message(owner_id, 'Обери спосіб доставки:', reply_markup=markup)


def propose_price(message, owner_id, group_id):
    global current_order_number
    if current_order_number:
        bot.send_message(group_id,
                         f"@{message.chat.username} не погодився з ціною менеджера. Зв'яжіться з ним\nНомер замовлення: {current_order_number}")
    else:
        bot.send_message(group_id, f"@{message.chat.username} не погодився з ціною менеджера. Зв'яжіться з ним")


@bot.message_handler(commands=['send_price'])
def handle_send_price(message):
    if message.from_user.id == 788388571 or message.from_user.id == 5792353056 or message.from_user.id ==5792353056:
        bot.reply_to(message, 'Введіть id користувача')
        bot.register_next_step_handler(message, process_order_number)
    else:
        bot.reply_to(message, 'У вас немає доступу до цієї команди.')

@bot.message_handler(commands=['send_price'])
def handle_send_money(message):
    if message.from_user.id == 788388571 or message.from_user.id == 5792353056 or message.from_user.id ==5792353056:
        bot.reply_to(message, 'Введіть id користувача')
        bot.register_next_step_handler(message, process_order_number_money)
    else:
        bot.reply_to(message, 'У вас немає доступу до цієї команди.')
def send_db_command(update, context):
    send_database(update.message)
def send_database(message):
    if message.from_user.id == 788388571 or message.from_user.id == 5792353056 or message.from_user.id == 5792353056:
        chat_id = message.chat.id
        bot = message.bot

        # Шлях до вашої бази даних SQLite
        db_path = 'photos.db'

        # Перевірка, чи існує файл бази даних
        if not os.path.exists(db_path):
            bot.send_message(chat_id, 'Файл бази даних не знайдено.')
            return

        # Відправка файлу бази даних
        with open(db_path, 'rb') as db_file:
            bot.send_document(chat_id=chat_id, document=InputFile(db_file))

        bot.send_message(chat_id, 'База даних відправлена.')
    else:
        bot.reply_to(message, 'У вас немає доступу до цієї команди.')
@bot.message_handler(commands=['send_price'])
def handle_cancel_order(message):
    if message.from_user.id == 788388571 or message.from_user.id == 5792353056 or message.from_user.id ==5792353056:
        bot.reply_to(message, 'Введіть id користувача')
        bot.register_next_step_handler(message, process_order_number_cancel)
    else:
        bot.reply_to(message, 'У вас немає доступу до цієї команди.')
@bot.message_handler(commands=['send_price'])
def handle_bad_ttn(message):
    if message.from_user.id == 788388571 or message.from_user.id == 5792353056 or message.from_user.id ==5792353056:
        bot.reply_to(message, 'Введіть id користувача')
        bot.register_next_step_handler(message, process_order_ttn_bad)
    else:
        bot.reply_to(message, 'У вас немає доступу до цієї команди.')
def send_broadcast_message(message):
    if message.from_user.id == 788388571 or message.from_user.id == 5792353056 or message.from_user.id ==5792353056:
        bot.send_message(message.chat.id, "Введи текст розсилки: ")
        bot.register_next_step_handler(message, send_broadcast_message2)
    else:
        bot.reply_to(message, 'У вас немає доступу до цієї команди.')



def send_broadcast_message2(message):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    message_text = message.text
    # Отримуємо список унікальних ідентифікаторів користувачів з бази даних
    cursor.execute("SELECT DISTINCT user_id FROM photos")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Надсилаємо повідомлення кожному користувачу
    for user_id in user_ids:
        bot.send_message(chat_id=user_id, text=message_text)


def process_order_number_money(message):
    user_id = message.text  # Отримуємо ідентифікатор користувача з повідомлення

    conn2 = sqlite3.connect('photos.db')
    cursor2 = conn2.cursor()
    cursor2.execute('SELECT * FROM photos WHERE user_id = ?', (user_id,))
    result2 = cursor2.fetchone()
    conn2.close()

    if result2:
        bot.reply_to(message, 'Введіть номер замовлення:')
        bot.register_next_step_handler(message, process_order_number_input_money, user_id)
    else:
        bot.reply_to(message, 'Номер користувача не знайдено')


def process_order_number_input_money(message, user_id):
    order_number = message.text

    # Перевірка наявності номера замовлення у базі даних
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM photos WHERE order_number = ?', (order_number,))
    result = cursor.fetchone()

    if result:
      process_money(message, order_number, user_id)

    else:
        bot.reply_to(message, 'Номер замовлення не знайдено')

    conn.close()
def process_order_number(message):
    user_id = message.text  # Отримуємо ідентифікатор користувача з повідомлення

    conn2 = sqlite3.connect('photos.db')
    cursor2 = conn2.cursor()
    cursor2.execute('SELECT * FROM photos WHERE user_id = ?', (user_id,))
    result2 = cursor2.fetchone()
    conn2.close()

    if result2:
        bot.reply_to(message, 'Введіть номер замовлення:')
        bot.register_next_step_handler(message, process_order_number_input, user_id)
    else:
        bot.reply_to(message, 'Номер користувача не знайдено')
def process_order_number_cancel(message):
    user_id = message.text  # Отримуємо ідентифікатор користувача з повідомлення

    conn2 = sqlite3.connect('photos.db')
    cursor2 = conn2.cursor()
    cursor2.execute('SELECT * FROM photos WHERE user_id = ?', (user_id,))
    result2 = cursor2.fetchone()
    conn2.close()

    if result2:
        bot.reply_to(message, 'Введіть номер замовлення:')
        bot.register_next_step_handler(message, process_order_number_cancel2, user_id)
    else:
        bot.reply_to(message, 'Номер користувача не знайдено')

def process_order_ttn_bad(message):
    user_id = message.text  # Отримуємо ідентифікатор користувача з повідомлення

    conn2 = sqlite3.connect('photos.db')
    cursor2 = conn2.cursor()
    cursor2.execute('SELECT * FROM photos WHERE user_id = ?', (user_id,))
    result2 = cursor2.fetchone()
    conn2.close()

    if result2:
        bot.reply_to(message, 'Введіть номер замовлення:')
        bot.register_next_step_handler(message, process_order_ttn_bad2, user_id)
    else:
        bot.reply_to(message, 'Номер користувача не знайдено')
# Функція для обробки введеного номера замовлення
def handle_find_order(message):
    if message.from_user.id == 788388571 or message.from_user.id==5792353056:
        bot.reply_to(message, 'Введіть id замовника')
        bot.register_next_step_handler(message, process_order_search)
    else:
        bot.reply_to(message, 'У вас немає доступу до цієї команди.')
def process_order_search(message):
    user_id = message.text  # Отримуємо ідентифікатор користувача з повідомлення

    conn2 = sqlite3.connect('photos.db')
    cursor2 = conn2.cursor()
    cursor2.execute('SELECT * FROM photos WHERE user_id = ?', (user_id,))
    result2 = cursor2.fetchone()
    conn2.close()

    if result2:
        bot.reply_to(message, 'Введіть номер замовлення:')
        bot.register_next_step_handler(message, process_order_search_input, user_id)
    else:
        bot.reply_to(message, 'Номер користувача не знайдено')
def process_order_search_input(message, user_id):
    order_number = message.text

    # Перевірка наявності номера замовлення у базі даних
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM photos WHERE order_number = ?', (order_number,))
    result = cursor.fetchone()
    conn.close()

    if result:
        checkItems(message,user_id,order_number)
        # Реєструємо функцію checkItems як обробник наступного кроку

    else:
        bot.reply_to(message, 'Номер замовлення не знайдено')
def checkItems(message, user_id, order_number):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()

    # Отримання ідентифікатора користувача


    # Отримання унікальних order_id користувача з бази даних
    cursor.execute('SELECT * FROM photos WHERE user_id = ? AND order_number = ?', (user_id, order_number))
    result = cursor.fetchone()

    if result:


            # Отримання статусу для кожного order_id користувача
            cursor.execute(
                'SELECT status, price, file, nomer_ttn,delivery, nomer_card FROM photos WHERE user_id = ? AND order_number = ?',
                (user_id, order_number))
            status_record = cursor.fetchone()

            if status_record:
                status = status_record[0]
                price = status_record[1]
                photo_data = base64.b64decode(status_record[2])
                ttn_number = status_record[3]
                delivery_field = status_record[4]
                card_number = status_record[5]
                caption = f"🟢 *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n🟢 *Ціна запропонована нами:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n🟢 *Номер накладної:* {ttn_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n🟢 *Номер карти:* {card_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n🟢Тип доставки: {delivery_field}"

                # Відправка повідомлення з фото, текстом та об'єктом markup
                bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                               parse_mode='Markdown')
            else:
                bot.reply_to(message, f"Не знайдено статусу для замовлення з номером {order_number}")
def process_order_number_input(message, user_id):
    order_number = message.text

    # Перевірка наявності номера замовлення у базі даних
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM photos WHERE order_number = ?', (order_number,))
    result = cursor.fetchone()

    if result:
        owner_id = result[1]  # Припускаємо, що ідентифікатор власника замовлення є в другому стовпці
        bot.reply_to(message, 'Введіть ціну')
        bot.register_next_step_handler(message, lambda msg: process_price(msg, order_number, user_id))

    else:
        bot.reply_to(message, 'Номер замовлення не знайдено')

    conn.close()
def process_order_number_cancel2(message, user_id):
    order_number = message.text

    # Перевірка наявності номера замовлення у базі даних
    conn2 = sqlite3.connect('photos.db')
    cursor2 = conn2.cursor()
    cursor2.execute(
        'SELECT status, price, file, nomer_ttn,delivery, nomer_card,name_order FROM photos WHERE user_id = ? AND order_number = ?',
        (user_id, order_number))
    status_record = cursor2.fetchone()
    name_order = status_record[6]

    if status_record:
        bot.send_message(user_id, f"‼️*На жаль ми не можемо тобі нічого запропонувати за замовлення  #{order_number}: {name_order}*.\n\nОднією з причин відмови могли стати наступні фактори:\n1️⃣ Не автентичність одягу.\n2️⃣ Стан або розмір.\n3️⃣ Відсутність потреби.",
                         parse_mode='Markdown')


    else:
        bot.reply_to(message, 'Номер замовлення не знайдено')
def process_order_ttn_bad2(message, user_id):
    order_number = message.text

    # Перевірка наявності номера замовлення у базі даних
    conn2 = sqlite3.connect('photos.db')
    cursor2 = conn2.cursor()
    cursor2.execute(
        'SELECT status, price, file, nomer_ttn,delivery, nomer_card,name_order FROM photos WHERE user_id = ? AND order_number = ?',
        (user_id, order_number))
    status_record = cursor2.fetchone()
    name_order = status_record[6]
    nomer_ttn = status_record[3]

    if status_record:
        bot.send_message(user_id, f"‼️*На жаль ви надали нам неправильний номер ТТН [{nomer_ttn}]  до замовлення #{order_number}: {name_order}*.\n\nЗміни його, у розділі \"Мої речі\", натиснувши на кнопку Змінити номер ТТН",
                         parse_mode='Markdown')


    else:
        bot.reply_to(message, 'Номер замовлення не знайдено')
# Функція для обробки ціни та збереження її до користувача

def process_price(message,order_number, user_id):
    try:
        # Відкриття з'єднання з базою даних
        conn = sqlite3.connect('photos.db')
        cursor = conn.cursor()

        # Отримання статусу та інформації з бази даних
        cursor.execute(
            'SELECT status, price, file, nomer_ttn, delivery, nomer_card, name_order FROM photos WHERE user_id = ? AND order_number = ?',
            (user_id, order_number))
        status_record = cursor.fetchone()
        name_order = status_record[6]
        update_price_status(order_number, None)
        group_id = '-4009484644'
        price = message.text

        # Відправлення повідомлень
        bot.send_message(user_id,
                         f"‼️*Запропонована нами ціна* за замовлення #{order_number} '{name_order}': *{price}  грн*",
                         parse_mode='Markdown')
        bot.send_message(group_id,
                         f"‼️*Запропонована нами ціна* за замовлення #{order_number} '{name_order}': *{price}  грн*",
                         parse_mode='Markdown')

        # Оновлення запису у базі даних
        cursor.execute('UPDATE photos SET status = 2, Price = ? WHERE user_id = ? AND order_number = ?',
                       (price, user_id, order_number))
        conn.commit()

        # Закриття з'єднання
        cursor.close()
        conn.close()

        # Збереження номеру замовлення
        global current_order_number
        current_order_number = order_number

        # Відправка повідомлення з кнопками
        markup = types.InlineKeyboardMarkup(row_width=2)
        yes_button = types.InlineKeyboardButton('✅ Так', callback_data='yes')
        no_button = types.InlineKeyboardButton('❌ Ні', callback_data='no')
        markup.add(yes_button, no_button)
        bot.send_message(user_id, 'Погоджуєшся з ціною?', reply_markup=markup)
    except Exception as e:
        print(f"An error occurred: {str(e)}")



def process_money(message,order_number, user_id):
    conn2 = sqlite3.connect('photos.db')
    cursor2 = conn2.cursor()
    cursor2.execute(
        'SELECT status, price, file, nomer_ttn,delivery, nomer_card,name_order FROM photos WHERE user_id = ? AND order_number = ?',
        (user_id, order_number))
    status_record = cursor2.fetchone()
    price_text = status_record[1]
    nomer_card = status_record[5]
    name_order = status_record[6]


    update_price_status(order_number, None)

    price = message.text
    bot.send_message(user_id, f"‼️*Кошти були перераховані * за замовлення #{order_number} '{name_order}' на карту {nomer_card} у розмірі *{price_text}  грн*", parse_mode='Markdown')



def propose_price(message, owner_id, group_id):
    global current_order_number
    if current_order_number:
        bot.send_message(group_id,
                         f"@{message.chat.username} не погодився з ціною менеджера. Зв'яжіться з ним\nНомер замовлення: {current_order_number}")
    else:
        bot.send_message(group_id, f"@{message.chat.username} не погодився з ціною менеджера. Зв'яжіться з ним")


def send_delivery_options(message, owner_id, group_id):
    global current_order_number
    if current_order_number:
        # Відправити повідомлення з кнопками доставки
        markup = types.InlineKeyboardMarkup(row_width=2)
        delivery1_button = types.InlineKeyboardButton('🚚 Наложкою', callback_data='delivery1')
        delivery2_button = types.InlineKeyboardButton('💳 Через систему', callback_data='delivery2')
        markup.add(delivery1_button, delivery2_button)
        bot.send_message(owner_id, 'Обери спосіб доставки:', reply_markup=markup)
    else:
        bot.send_message(group_id, f"@{message.chat.username} не погодився з ціною менеджера. Зв'яжіться з ним")


@bot.callback_query_handler(func=lambda call: call.data in ['delivery1', 'delivery2'])
def handle_delivery_selection(call):
    message = call.message
    owner_id = message.chat.id
    group_id = '-917631518'  # Замініть на фактичний ID вашої групи

    if call.data == 'delivery1':

        if get_delivery_status(current_order_number) is None:
            update_order_status(current_order_number, 4)  # Змінити статус на 4

            # Відправити повідомлення про доставку №1
            delivery1_message = """
                 *🚚 Доставка наложним платежем*

‼️ При обранні цього виду доставки при відправці товару, *треба вказати таку ціну,* яку ми запропонували вам при оцінці товару.
‼️ Вартість товару разом з вартістю доставки *буде сплачуватися* при отриманні товару. 
‼️ Дані для відправки будуть переслані після того, як натиснеш *“✅ Обрати доставку наложним платежем”.*
 \n*Недоліки:*
 📍 Ти зможеш *отримати гроші* лише після того, як ми *оплатимо товар на пошті.*"""

            markup = types.InlineKeyboardMarkup(row_width=1)
            choose_cod_button = types.InlineKeyboardButton('✅ Обрати доставку наложним платежем',
                                                           callback_data='choose_cod')
            markup.add(choose_cod_button)
            bot.send_message(owner_id, delivery1_message, reply_markup=markup, parse_mode='Markdown')

        else:
            bot.send_message(owner_id, "Ти вже обрав спосіб доставки.")

    elif call.data == 'delivery2':

        if get_delivery_status(current_order_number) is None:
            update_order_status(current_order_number, 4)  # Змінити статус на 4

            # Відправити повідомлення про доставку №2
            delivery2_message = """
*💳 Доставка через систему*

‼️ Доставка здійснюється також *наложним платежем.*
‼️ При відправці ти *не вказуєш ціни за товар.*
‼️ Як тільки ми отримаємо товар, *гроші будуть моментально перечислені на твою карту.*

‼️ *Дані куди відправляти твоє замовлення* будуть переслані після того, як натиснеш *“✅ Обрати доставку через систему”.*
               """

            markup = types.InlineKeyboardMarkup(row_width=1)
            choose_system_delivery_button = types.InlineKeyboardButton('✅ Обрати доставку через систему',
                                                                       callback_data='choose_system_delivery')
            markup.add(choose_system_delivery_button)
            bot.send_message(owner_id, delivery2_message, reply_markup=markup,parse_mode="Markdown")

        else:
            bot.send_message(owner_id, "Ти вже обрав спосіб доставки.")


@bot.callback_query_handler(func=lambda call: call.data == 'choose_cod')
def handle_choose_cod(call):
    message = call.message
    owner_id = message.chat.id
    group_id = '-917631518'  # Замініть на фактичний ID вашої групи

    if get_delivery_status(current_order_number) is None:
        # Оновити поле delivery на "Доставка наложним платежем" у базі даних
        update_delivery(current_order_number, "Доставка наложним платежем")
        text2 = "‼️*Відправ свій товар за нижче вказаною адресою:*\n\n" \
                "🏢 Присяжнюк Орест Ігорович\n" \
                "☎️ +380679770216\n" \
                "📍 Рівне, Рівненська область\n" \
                "📮 Відділення Нової Пошти номер 2"
        bot.send_message(message.chat.id, text2, parse_mode='Markdown')
        bot.send_message(message.chat.id,
                         '''‼️Як тільки відправиш замовлення, *прикріпи накладну*, натиснувши:

"Мої замовлення" ➡️ "Прикріпити номер накладної".''',
                         parse_mode='Markdown')
        bot.send_message(group_id,
                         f"@{message.chat.username} з ід {message.chat.id} обрав доставку наложним платежем\n Номер замовлення: {current_order_number}")
        bot.send_message('-4009484644',
                         f"@{message.chat.username} з ід {message.chat.id} обрав доставку наложним платежем\n Номер замовлення: {current_order_number}")
    else:
        bot.send_message(owner_id, "Ти вже обрав спосіб доставки.")


@bot.callback_query_handler(func=lambda call: call.data == 'choose_system_delivery')
def handle_choose_system_delivery(call):
    message = call.message
    owner_id = message.chat.id
    group_id = '-917631518'  # Замініть на фактичний ID вашої групи

    if get_delivery_status(current_order_number) is None:
        # Оновити поле delivery на "Доставка наложним платежем" у базі даних
        update_delivery(current_order_number, "Доставка через систему")

        text2 = "‼️*Відправ свій товар за нижче вказаною адресою:*\n\n" \
                "🏢 Присяжнюк Орест Ігорович\n" \
                "☎️ +380679770216\n" \
                "📍 Рівне, Рівненська область\n" \
                "📮 Відділення Нової Пошти номер 2"
        bot.send_message(message.chat.id, text2, parse_mode='Markdown')
        bot.send_message(message.chat.id,
                         f'‼️Як тільки ви відправите замовлення, *прикріпіть накладну*, натиснувши:\n"Мої замовлення" ➡️ "Відправити номер накладної". \nТам ж само ви можете прикріпити *номер карти.*',
                         parse_mode='Markdown')
        bot.send_message(group_id,
                         f"@{message.chat.username} з ід {message.chat.id} обрав доставку через систему\n Номер замовлення: {current_order_number}")

        bot.send_message(-4009484644,
                         f"@{message.chat.username} з ід {message.chat.id} обрав доставку через систему\n Номер замовлення: {current_order_number}")
    else:
        bot.send_message(owner_id, "Ти вже обрав спосіб доставки.")


def send_database(update, context):
    chat_id = update.effective_chat.id
    bot = context.bot

    # Шлях до вашої бази даних SQLite
    db_path = 'photos.db'

    # Перевірка, чи існує файл бази даних
    if not os.path.exists(db_path):
        update.message.reply_text('Файл бази даних не знайдено.')
        return

    # Відправка файлу бази даних
    with open(db_path, 'rb') as db_file:
        bot.send_document(chat_id=chat_id, document=InputFile(db_file))

    update.message.reply_text('База даних відправлена.')
def get_delivery_status(order_number):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT delivery FROM photos WHERE order_number = ?', (order_number,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    else:
        return None


def get_ttn_status(order_number):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nomer_ttn FROM photos WHERE order_number = ?', (order_number,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def get_ttn_and_card_status(order_number):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nomer_ttn,nomer_card FROM photos WHERE order_number = ?', (order_number,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0],result[1]
    else:
        return None
def get_card_status(order_number):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nomer_card FROM photos WHERE order_number = ?', (order_number,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    else:
        return None


def get_price_status(order_number):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT price_status FROM photos WHERE order_number = ?', (order_number,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    else:
        return None
def update_delivery(order_number, delivery):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE photos SET delivery = ? WHERE order_number = ?', (delivery, order_number))
    conn.commit()
    cursor.close()
    conn.close()


def update_order_status(order_number, status):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE photos SET status = ? WHERE order_number = ?', (status, order_number))
    conn.commit()

    cursor.close()
    conn.close()

def update_price_status(order_number, status):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE photos SET price_status = ? WHERE order_number = ?', (status, order_number))
    cursor.close()
    conn.close()

# current_order_number = 1


@bot.message_handler(func=lambda message: message.text == 'Речі, які ми купуємо')
def handle_buying_items(message):
    markup = create_inline_keyboard()
    bot.send_message(message.chat.id, 'Ось речі, які ми купуємо *з найвищим пріоритетом:*\n\n*Натисніть на кнопки* знизу,щоб дізнатися більше про список речей!', reply_markup=markup,parse_mode="Markdown")


def create_inline_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_nike = types.InlineKeyboardButton('Nike', callback_data='buying_item_nike')
    button_adidas = types.InlineKeyboardButton('Adidas', callback_data='buying_item_adidas')
    button_reebok = types.InlineKeyboardButton('Reebok', callback_data='buying_item_reebok')
    button_champion = types.InlineKeyboardButton('Fila', callback_data='buying_item_champion')
    button_carhartt = types.InlineKeyboardButton('Carhartt', callback_data='buying_item_carhartt')
    button_tommy_hilfiger = types.InlineKeyboardButton('Tommy Hilfiger', callback_data='buying_item_tommy_hilfiger')
    button_Yves_Saint_Laurent  = types.InlineKeyboardButton('Yves Saint Laurent ', callback_data='buying_item_Yves_Saint_Laurent')
    button_lacoste = types.InlineKeyboardButton('Lacoste', callback_data='buying_item_lacoste')
    button_ralph_lauren = types.InlineKeyboardButton('Ralph Lauren', callback_data='buying_item_ralph_lauren')
    button_dickies = types.InlineKeyboardButton('Dickies', callback_data='buying_item_dickies')
    button_stussy = types.InlineKeyboardButton('Stüssy', callback_data='buying_item_stussy')
    button_champion = types.InlineKeyboardButton('Champion', callback_data='buying_item_champion')
    button_patagonia = types.InlineKeyboardButton('Patagonia', callback_data='buying_item_patagonia')
    button_the_north_face = types.InlineKeyboardButton('The North Face', callback_data='buying_item_the_north_face')

    markup.add(
        button_nike, button_adidas, button_reebok, button_champion,
        button_lacoste, button_ralph_lauren, button_carhartt, button_dickies, button_stussy,button_tommy_hilfiger,button_Yves_Saint_Laurent,button_patagonia,button_the_north_face
    )

    return markup


@bot.callback_query_handler(func=lambda call: call.data.startswith('buying_item_'))
def handle_buying_item_callback(call):
    item_name = call.data.replace('buying_item_', '')

    if item_name == 'nike':
        message = '''
*Одяг*
• *Вінтажні кофти*, (світшоти, худаки, олімпійки, фліски).
• *Вінтажні футболки.*
• *Нейлонові штани.*
• *Вінтажні пухани та жилетки.* 
\n*Аксесуари* 
• *Різні сумки.*
• *Часи.*
        '''

    elif item_name == 'adidas':
        message = '''
        *Одяг*
• *Вінтажні кофти*, (світшоти, худаки, фліски, олімпійки)
• *Вінтажні футболки.*
• *Нейлонові штани.*'''



    elif item_name == 'fila':

        message = '''
*Одяг*
• *Вінтажні кофти,* (світшоти, худаки).в'''
    elif item_name == 'tommy_hilfiger':
        message = '''
*Одяг*
• *Вінтажні кофти*, (світшоти, худаки, фліски).'''
    elif item_name == 'reebok':
        message = '''*Одяг*
• *Вінтажні кофти*, (світшоти, худаки).'''
    elif item_name == 'fila ':
        message = '''
*Одяг*
• *Вінтажні кофти*, (світшоти, худаки).
'''
    elif item_name == 'lacoste':
        message = '''
*Одяг*
• *Вінтажні светри,* (світшоти).
• *Вінтажні поло футболки.*'''
    elif item_name == 'ralph_lauren':
        message = '''
*Одяг*
• *Кофти*, (світшоти, зіпки, регбійки, 1/4 1/3 зіп).
• *Футболки* (поло, не поло).
• *Куртани, пухани, Harrington jackets.*

*Акссесуари *
• *Різні сумки.*'''
    elif item_name == 'carhartt':
        message = '''
*Одяг*
• *Кофти* (світшоти, худаки, зіпки).
• *Active jackets, Harrington jackets.*
• *Футболки.*

*Акссесуари *
• *Різні сумки.*'''
    elif item_name == 'dickies':
        message = '''
*Одяг*
• *Кофти*, (світшоти, худаки).
• *Harrington jackets.*
• *Футболки.*'''
    elif item_name == 'Yves_Saint_Laurent':
        message = '''
       *Одяг*
• *Вінтажні светри*, (світшоти).
• *Вінтажні поло футболки.*'''

    elif item_name == 'champion':
        message = '''
       *Одяг*
• *Вінтажні кофти*, (світшоти, худаки).'''
    elif item_name == 'patagonia':
        message = '''
       *Одяг*
• *Кофти* (фліски).
• *Куртани* (вітряки).'''

    elif item_name == 'the_north_face':
        message = '''
       *Одяг*
• *Кофти*, (світшоти, худаки, фліски).
• *Куртани, пухани, вітряки, жилетки.* '''


    elif item_name == 'stussy':
        message = '''
*Одяг*
• *Кофти*, (світшоти, худаки).
• *Футболки.*
• *Куртани.*

*Акссесуари*
• *Різні сумки.*'''



    else:
        message = 'Невідома річ'

    bot.send_message(call.message.chat.id, message, parse_mode="Markdown")
#     917631518

bot.polling(none_stop=True)