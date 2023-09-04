import base64
import json
import random
from io import BytesIO
import io
import re
import datetime

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
    button1 = types.KeyboardButton('👕➡️💵 Продати')
    button2 = types.KeyboardButton('🧳 Мої замовлення 🧳')
    button6 = types.KeyboardButton('✏️ Звернутися до підтримки ✏️')

    button3 = types.KeyboardButton('❓Як все працює❓')
    button4 = types.KeyboardButton('👥 Про нас 👥')
    button5 = types.KeyboardButton("Відправити ціну")
    # Разделяю кнопки по строкам так, чтобы товары были отдельно от остальных кнопок
    markup.row(button1)
    markup.row(button2)
    markup.row(button3, button4)
    markup.row(button6)
    if user_id == 788388571 or user_id==5792353056 or user_id==5792353056:
        button7 = types.KeyboardButton("Адмін панель")
        markup.row(button7)

    if message.text == '/start':
        bold_text = f"Привіт , *{message.from_user.first_name}*! Це *жирний* і *ще один* жирний текст."

        # bot.send_message(message.chat_id, text=bold_text, parse_mode=telegram.ParseMode.MARKDOWN)
        # Отправляю приветственный текст
        bot.send_message(message.chat.id,
                         f'Привіт 👋, *{message.from_user.first_name}*!\nЛаскаво просимо до нашого інноваційного телеграм-бота "SndSkup"! Тут тобі вдасться продати свій товар всього за декілька кліків.',reply_markup=markup,
                         parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, 'Закинув тебе в головне меню,вибирай!', reply_markup=markup)


# Обработка обычных текстовых команд, описанных в кнопках
@bot.message_handler()
def info(message):
    if message.text == '👕➡️💵 Продати':
        goodsChapter(message)
    elif message.text == '❓Як все працює❓':
        settingsChapter(message)
    elif message.text == '🧳 Мої замовлення 🧳':
        my_items(message)
    elif message.text == '👥 Про нас 👥':
        infoChapter(message)
    elif message.text == 'Орест лох':
        OrestLoh(message)
    elif message.text == "Відправити ціну":
        handle_send_price(message)
    elif message.text=="Пошук замовлень":
        handle_find_order(message)
    elif message.text=="Відправити розсилку":
        send_broadcast_message(message)
    elif message.text == "✅ Речі які ми купуємо ✅":
        handle_buying_items(message)
    elif message.text == "✅ Я відправив усі фото":
         check_and_update_status(message)
    elif message.text=="Адмін панель":
        adminPanel(message)
    elif message.text == '❓Як ми оцінюємо товар❓':
        OtsinkaTovaru(message)







    elif message.text == '📷 Відправити фото 📸':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button2 = types.KeyboardButton('✅ Я відправив усі фото')
        # markup.row(button2)
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button3 = types.KeyboardButton('↩️ Назад до меню')
        markup.row(button2, button3)

        global last_order_number
        last_order_number = None
        sentPhotoChapter(message)

        @bot.message_handler(content_types='photo')
        def get_photo(message):
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
                               price_status TEXT
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

                global last_order_number

                # Якщо це перше фото або кнопка "Відправити фото" була натиснута, створюємо новий номер замовлення
                if last_order_number is None or message.text == '📷 Відправити фото 📸':
                    # Оновлюємо номер замовлення
                    cursor.execute('SELECT MAX(order_number) FROM photos')
                    result = cursor.fetchone()[0]
                    if result is None:
                        last_order_number = 1
                    else:
                        last_order_number = int(result) + 1

                status = 8  # Значення статусу 8

                cursor.execute(
                    'INSERT INTO photos (user_id, file, order_number, price, status, delivery, nomer_ttn,price_status) '
                    'VALUES (?, ?, ?, ?, ?, ?,  ?,?)',
                    (user_id, encoded_photo, last_order_number, None, status, None, None,None))
                conn.commit()
                conn.commit()

                order_message = f"Користувач @{message.from_user.username} з ід `{message.chat.id}` хоче продати річ\n" \
                                f"Номер замовлення: {last_order_number}"
                bot.send_message(chat_id='-917631518', text=order_message,parse_mode='MarkdownV2')


                # Відправлення фотографії до групи
                bot.send_photo(chat_id='-917631518', photo=photo.file_id)

            cursor.close()
            conn.close()













    elif message.text == '✏️ Звернутися до підтримки ✏️':
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




def check_and_update_status(message):
    user_id = message.from_user.id

    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()

    # Вибірка останнього замовлення користувача
    cursor.execute('''
            SELECT status, order_number
            FROM photos
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 1
        ''', (user_id,))

    # Отримання результату запиту
    row = cursor.fetchone()

    if row is not None:
        status, order_number = row
        if status == 8:
            cursor.execute('UPDATE photos SET status = 9 WHERE order_number = ? AND user_id = ?',
                           ( order_number, message.from_user.id))
            conn.commit()

            conn.commit()  # Застосування змін до бази даних

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button2 = types.KeyboardButton('↩️ Назад до меню')
            markup.row(button2)

            bot.send_message(message.chat.id, '✅ Твої фото були успішно завантажені 😌\n\n'
                                              '📍Щоб переглянути статус вашого товару перейди до розділу "Мої замовлення".\n\n'
                                              '📍Один з наших працівників розгляне твою пропозицію та запропонує тобі найкращу ціну, роблячи це максимально швидко 🚀',
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'УПС.... Ти не завантажив фотографій!')
    else:
        bot.send_message(message.chat.id, 'УПС.... Ти не завантажив фотографій!')

    conn.close()
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
        button4 = types.KeyboardButton('↩️ Назад до меню')
        markup.row(button1, button2)
        markup.row(button3)
        markup.row(button4)
        bot.send_message(message.chat.id, 'Ти перейшов у розділ Адмін панель', reply_markup=markup)


def goodsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('✅ Речі які ми купуємо ✅')
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
    bot.send_message(message.chat.id, 'Натисни "Продати" ➡️ ”Відправити фото” та надішли нам потрібні фото своєї речі.\n\n'
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

    return result > 0

# Обробник натискання кнопки "Я відправив усі фото"




# def check_photos_in_previous_message(update: Update, context: CallbackContext):
#     # Визначаємо функцію перевірки фотографій
#     def check_photos():
#         # Отримуємо об'єкт попереднього повідомлення
#         previous_message = update.effective_message.reply_to_message
#
#         # Перевіряємо, чи є фотографії у попередньому повідомленні
#         if previous_message and (previous_message.photo or previous_message.document):
#             update.message.reply_text("Ви надсилали фото у попередньому повідомленні.")
#         else:
#             update.message.reply_text("Ви не надсилали фото у попередньому повідомленні.")
#
#     # Запускаємо функцію перевірки через 2 секунди
#     context.job_queue.run_once(check_photos, 2)
#

# def check_photos_command(update: Update, context: CallbackContext):
#     # Викликаємо функцію check_photos_in_previous_message
#     check_photos_in_previous_message(update, context)
#
# # Додаємо обробник команди "/check_photos"

# def check_photos(message):
#     time.sleep(2)
#
#     # Перевіряємо, чи містить повідомлення фотографії
#     if message.photo:
#         return True
#     else:
#         return False

# Функція для створення розмітки кнопки


# Обробник команди /start або будь-якого текстового повідомлення
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

4️⃣ Надішли фото *недоліків.*

5️⃣ Після того *як завантажив необхідні фото*, натисни “✅ Я відправив усі фото”.''', parse_mode='Markdown')

    text = "*‼️Відправляйте лише правдиві фото та всі недоліки‼️*\nНе гайте ні нашого, ні вашого часу. Кожна річ буде ретельно перевірена на пошті."


    bot.send_message(message.chat.id, text,reply_markup=markup,parse_mode='Markdown')




        # def info2Chapter(message):


#     user_id = message.from_user.id
#
#
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button2 = types.KeyboardButton('↩️ Назад до меню')
#     markup.row( button2)
#
#     bot.send_message(message.chat.id, '✅ Ваші фото були успішно завантажені 😌\n\n'
#                                       '📍Щоб переглянути статус вашого товару перейдіть до розділу "Мої речі".\n\n'
#                                       '📍Один з наших працівників розгляне вашу пропозицію та запропонує вам найкращу ціну, роблячи це максимально швидко 🚀',
#                      reply_markup=markup)
def infoChapter(message):
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # button2 = types.KeyboardButton('↩️ Назад до меню')
    # markup.row( button2)
    word1 = "  "
    bot.send_message(message.chat.id, f'''        
        {word1}Про нас 🙃

Ми - команда експертів, які спеціалізуються на скупці різного "вінтажного" та "кежуального" шмоту. Наша мета - надати вам зручну та вигідну можливість продати непотрібні речі та отримати за них реальну вартість. 💰

Чому обрати нас? 🌟

1️⃣ *Широкий спектр речей:* Ми приймаємо до розгляду різноманітні види одягу, включаючи верхній одяг, штани, інколи взуття, аксесуари та багато іншого. 👕👖👟

2️⃣ *Справедлива оцінка:* Ми цінуємо ваші товари і ретельно оцінюємо їх, враховуючи бренд, стан та популярність. Наші професіонали гарантують справедливу вартість для ваших речей. 💎📈

3️⃣ *Простий процес продажу:* Ми зробили процес продажу максимально простим і зручним для вас. Ви надсилаєте нам фото товару, отримуєте оцінку, погоджуєтеся з ціною та обираєте спосіб доставки. Ми стежимо за кожним кроком, щоб ви отримали гарну взаємовигідну угоду. 📸✅🚚

4️⃣ *Надійна та швидка оплата:* Після прийняття вашого товару та підтвердження угоди, ми швидко перераховуємо гроші на ваш рахунок. Ми розуміємо, що час - цінний ресурс, тому ми робимо все можливе, щоб оплата була здійснена швидко та надійно. 💸⏱️

Ми пишаємося нашою командою експертів, яка зосереджена на вашому задоволенні та впевнена, що забезпечить вам зручний та вигідний досвід продажу. Приєднуйтесь до нашої спільноти і давайте разом знайдемо нове призначення для вашого непотрібного одягу! 💼''',
                     parse_mode='Markdown')


# def info2Chapter(message):
#     user_id = message.from_user.id
#
#
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button2 = types.KeyboardButton('↩️ Назад до меню')
#     markup.row( button2)
#
#     bot.send_message(message.chat.id, '✅ Ваші фото були успішно завантажені 😌\n\n'
#                                       '📍Щоб переглянути статус вашого товару перейдіть до розділу "Мої речі".\n\n'
#                                       '📍Один з наших працівників розгляне вашу пропозицію та запропонує вам найкращу ціну, роблячи це максимально швидко 🚀',
#                      reply_markup=markup)

# def check_previous_photo(update: Update, context: CallbackContext):
#     message = update.message  # Отримуємо поточне повідомлення
#     photos = message.photo  # Отримуємо список фото з повідомлення
#
#     if not photos:
#         message.reply_text('Ви не відправили жодного фото!')
#     else:
#         # Виконуємо додаткові дії, якщо фото було відправлено
#         info2Chapter(message)

# def handle_message(update: Update, context: CallbackContext):
#     check_previous_photo(update, context)
# def send_all_photos(message):
#     conn = sqlite3.connect('photos.db')
#     cursor = conn.cursor()
#
#     # Отримання останнього номера замовлення
#     cursor.execute('SELECT MAX(order_number) FROM photos')
#     result = cursor.fetchone()[0]
#     if result is None:
#         last_order_number = 1
#     else:
#         last_order_number = int(result)
#
#     # Вибірка фотографій для певного номера замовлення
#     cursor.execute('SELECT file FROM photos WHERE order_number = ?', (last_order_number,))
#     photo_records = cursor.fetchall()
#
#     if photo_records:
#         for photo_record in photo_records:
#             encoded_photo = photo_record[0]
#             photo_data = base64.b64decode(encoded_photo)
#
#             # Відправлення фотографій до групи
#             bot.send_photo(chat_id='-917631518', photo=io.BytesIO(photo_data))
#
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         button2 = types.KeyboardButton('↩️ Назад до меню')
#         markup.row(button2)
#
#         bot.send_message(message.chat.id, '✅ Ваші фото були успішно завантажені 😌\n\n'
#                                           '📍Щоб переглянути статус вашого товару перейдіть до розділу "Мої речі".\n\n'
#                                           '📍Один з наших працівників розгляне вашу пропозицію та запропонує вам найкращу ціну, роблячи це максимально швидко 🚀',
#                          reply_markup=markup)
#     else:
#         bot.send_message(message.chat.id, 'Ви не відправили жодного фото!')
#
#     cursor.close()
#     conn.close()


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
    text2 = "‼*Як проходить оцінка товару?  🤔*\n\n" \
            "При оцінці вашого товару ми звертаємо увагу на три основні фактори:\n\n" \
            "1. *Фірма (модель):* Один з ключових аспектів - це бренд та модель товару. Відомі фірми та популярні моделі зазвичай мають більшу вартість. Якщо ваш товар належить до відомої фірми або популярної моделі, це вплине позитивно на оцінку. 👍\n\n" \
            "2. *Розмір:* Розмір товару також має значення при оцінці. Деякі розміри можуть бути більш популярними або рідкісними, що впливає на їхню ціну. Наприклад, розмір, який важко знайти або дуже популярний, може мати вищу ціну порівняно зі звичайними розмірами. 📏\n\n" \
            "3. *Стан:* Стан товару є важливим чинником в оцінці. Чим кращий стан товару, тим більша ймовірність, що його оцінять вище. Товари у відмінному стані, майже нові або з мінімальними ознаками використання, зазвичай мають вищу оцінку. 😊\n\n" \
            "" \
            "*‼️ Зверніть свою увагу на розділ “Речі які ми купуємо”‼️* \n" \
            "(”Продати” ➡️ ”Речі які ми купуємо”), у цьому розділі ви зможете побачити речі які ми скуповуємо з найвищим пріоритетом, на той чи інший час." \
            "" \
            ""
    bot.send_message(message.chat.id, text2 ,parse_mode='Markdown')


# @bot.message_handler(commands=['send_photos'])
# def sendPhotoToGroup(message):
#     user_id = message.from_user.id
#
#     # Отримання фотографій користувача з бази даних
#     cursor.execute('SELECT file FROM photos WHERE user_id = ?', (user_id,))
#     photo_records = cursor.fetchall()
#
#     if len(photo_records) > 0:
#         photos = []
#         for record in photo_records:
#             # Розкодування фотографії з base64
#             encoded_photo = record[0]
#             photo_data = base64.b64decode(encoded_photo)
#             photos.append(BytesIO(photo_data))
#
#         # Відправка всіх фотографій в одному повідомленні
#         media_group = [types.InputMediaPhoto(media=photo) for photo in photos]
#         bot.send_media_group(chat_id='-917631518', media=media_group)
#     else:
#         bot.reply_to(message, 'Немає фотографій для відправлення!')


# Строчка, чтобы программа не останавливалась

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
            cursor.execute('SELECT status, price, file, nomer_ttn,delivery, nomer_card FROM photos WHERE user_id = ? AND order_number = ?',
                           (user_id, order_number))
            status_record = cursor.fetchone()

            if status_record:
                status = status_record[0]
                price = status_record[1] if status_record[1] is not None else 'Ще немає'
                photo_data = base64.b64decode(status_record[2])
                ttn_number = status_record[3] if status_record[3] is not None else 'Ще немає'
                delivery_field=status_record[4] if status_record[4] is not None else 'Ще немає'
                card_number=status_record[5] if status_record[5] is not None else 'Ще немає'

                if status == 1:
                    caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Пропозицію була подана на розгляд 😼\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Ціна запропонована нами:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}"
                    bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                   reply_markup=markup,parse_mode='Markdown')
                elif status == 2:
                    caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Запропонована нами ціна, очікує вашого підтвердження 👀\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Ціна запропонована нами:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}"
                    bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,parse_mode='Markdown')
                elif status == 3:
                    caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Ціну було підтверджено ✅\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Ціна запропонована нами:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}"
                    bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                    parse_mode='Markdown')
                elif status == 4 and delivery_field=='Доставка наложним платежем':
                    caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Замовлення в дорозі 📦\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Ціна запропонована нами:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}"

                    # Створення кнопки "Відправити номер ТТН"
                    markup = types.InlineKeyboardMarkup()
                    ttn_button = types.InlineKeyboardButton("Відправте номер накладної", callback_data=f"ttn_{order_number}")
                    markup.add(ttn_button)

                    # Відправка повідомлення з фото, текстом та кнопкою
                    bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                   reply_markup=markup,parse_mode='Markdown')
                elif status==4 and delivery_field=='Доставка через систему':
                    # Створення першого об'єкту markup і додавання до нього першої кнопки
                    markup = types.InlineKeyboardMarkup()
                    ttn_button = types.InlineKeyboardButton("Відправте номер накладної", callback_data=f"ttn_{order_number}")
                    markup.add(ttn_button)

                    # Створення другого об'єкту markup і додавання до нього другої кнопки
                    ttn_button2 = types.InlineKeyboardButton('Відправте номер вашої карти',callback_data=f"card_{order_number}")
                    markup.add(ttn_button2)

                    # Ваш підготовлений caption
                    caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Замовлення в дорозі 📦\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Ціна запропонована нами:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер карти:* {card_number}"

                    # Відправка повідомлення з фото, текстом та об'єктом markup
                    bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                   reply_markup=markup, parse_mode='Markdown')

                elif status==5 and delivery_field=='Доставка через систему':
                    # Створення першого об'єкту markup і додавання до нього першої кнопки
                    markup = types.InlineKeyboardMarkup()

                    # Створення другого об'єкту markup і додавання до нього другої кнопки
                    ttn_button2 = types.InlineKeyboardButton('Відправте номер вашої карти',callback_data=f"card_{order_number}")
                    markup.add(ttn_button2)

                    # Ваш підготовлений caption
                    caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Замовлення в дорозі 📦\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Ціна запропонована нами:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер карти:* {card_number}"

                    # Відправка повідомлення з фото, текстом та об'єктом markup
                    bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,
                                   reply_markup=markup, parse_mode='Markdown')
                else:
                    caption = f"➡️ *Номер замовлення:* {order_number}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Статус:* Пропозиція була подана на розгляд 😼\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Ціна запропонована нами:* {price} грн\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n➡️ *Номер накладної:* {ttn_number}"

                    # Отримання першого фото для кожного order_id користувача
                    cursor.execute('SELECT file FROM photos WHERE user_id = ? AND order_number = ? LIMIT 1',
                                   (user_id, order_number))
                    photo_record = cursor.fetchone()

                    if photo_record:
                        encoded_photo = photo_record[0]
                        photo_data = base64.b64decode(encoded_photo)

                        # Формування повідомлення з фото та текстом
                        bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption,parse_mode='Markdown')
                    else:
                        bot.reply_to(message, f"Не знайдено фото для замовлення з номером {order_number}")

            else:
                bot.reply_to(message, f"Не знайдено статусу для замовлення з номером {order_number}")
    else:
        bot.reply_to(message, f"У тебе ще немає жодного замовлення 😔. \n\n📍Щоб створити замовлення натисни:      \n”Продати” ➡️ “Відправити фото”.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('ttn_'))
def handle_ttn_number(call):
    if get_ttn_status(current_order_number) is None:
        order_number = call.data.split('_')[1]
        bot.send_message(call.message.chat.id, 'Відправте номер накладної\n               ⬇️⬇️⬇️')

        # Реєструємо функцію, яка буде обробляти наступне повідомлення користувача
        bot.register_next_step_handler(call.message, save_ttn_number, order_number)
    else:
        bot.send_message(call.message.chat.id, 'Ви уже відправляли номер ТТН!')



def save_ttn_number(message, order_number):
        # Отримуємо введений користувачем номер ТТН
        if get_ttn_status(current_order_number) is None:

            ttn_number = message.text
            # Збереження номера ТТН у базу даних
            conn = sqlite3.connect('photos.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE photos SET nomer_ttn = ?, status = 5 WHERE order_number = ? AND user_id = ?',
                           (ttn_number, order_number, message.from_user.id))
            conn.commit()
            conn.close()

            # Відправляємо відповідь користувачу
            reply_text = f"Ти надіслав номер накладної ТТН: {ttn_number}. Номер ТТН збережено."
            bot.send_message(message.chat.id, reply_text)
            bot.send_message(-917631518,
                             f"Користувач @{message.chat.username} відправив номер накладної {ttn_number}. Номер замовлення: #{order_number}")
        else:
            bot.send_message(message.chat.id,
                             f"Номер ТТН уже було збережено")




@bot.callback_query_handler(func=lambda call: call.data.startswith('card_'))
def handle_card_number(call):

    if get_card_status(current_order_number) is None:
        order_number = call.data.split('_')[1]
        bot.send_message(call.message.chat.id, 'Відправте номер вашої карти\n '
                                               '                    ⬇️⬇️⬇️'
                         )

        # Реєструємо функцію, яка буде обробляти наступне повідомлення користувача
        bot.register_next_step_handler(call.message, save_card_number, order_number)
    else:
        bot.send_message(message.chat.id,
                         f"Ти уже зберіг номер карти!")


def save_card_number(message, order_number):

    # Отримуємо введений користувачем номер ТТН
    if get_card_status(order_number) is None:

        card_number = message.text

        # Збереження номера ТТН у базу даних
        conn = sqlite3.connect('photos.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE photos SET nomer_card = ?, status = 6 WHERE order_number = ? AND user_id = ?',
                       (card_number, order_number, message.from_user.id))
        conn.commit()
        conn.close()

        # Відправляємо відповідь користувачу
        reply_text = f"Ти надіслав номер своєї карти: {card_number}. Номер карти збережено."
        bot.send_message(message.chat.id, reply_text)
        bot.send_message(-917631518,
                         f"Користувач @{message.chat.username} з ід `{message.chat.id}` відправив номер своєї карти: `{card_number}`\nНомер замовлення: {order_number}",
                         parse_mode="MarkdownV2")
    else:
        bot.send_message(message.chat.id,
                         f"Номер карти уже було збережено")
# def process_order_number(message):
#     order_number = message.text
#
#     # Перевірка наявності номера замовлення у базі даних
#     conn = sqlite3.connect('photos.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM photos WHERE order_number = ?', (order_number,))
#     result = cursor.fetchone()
#
#     if result:
#         owner_id = result[1]  # Припускаємо, що ідентифікатор власника замовлення є в другому стовпці
#         bot.reply_to(message, 'Введіть ціну')
#         bot.register_next_step_handler(message, lambda msg: process_price(msg, owner_id, order_number))
#     else:
#         bot.reply_to(message, 'Номер замовлення не знайдено')
#
#     cursor.close()
#     conn.close()
#
#
# def process_price(message, owner_id, order_number):
#     price = message.text
#
#     # Відправити ціну власнику замовлення
#     bot.send_message(owner_id, f"Ціна замовлення: {price}  грн")
#
#     # Оновлення статусу замовлення та збереження ціни в базі даних
#     conn = sqlite3.connect('photos.db')
#     cursor = conn.cursor()
#     cursor.execute('UPDATE photos SET status = 2, Price = ? WHERE order_number = ?', (price, order_number))
#     conn.commit()
#     cursor.close()
#     conn.close()
#
#     # Зберегти номер замовлення в змінну
#     global current_order_number
#     current_order_number = order_number
#
#     # Відправити повідомлення з кнопками
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     yes_button = types.InlineKeyboardButton('Так', callback_data='yes')
#     no_button = types.InlineKeyboardButton('Ні', callback_data='no')
#     markup.add(yes_button, no_button)
#     bot.send_message(owner_id, 'Поджуєтеся з ціною?', reply_markup=markup)


# @bot.callback_query_handler(func=lambda call: call.data in ['cash_on_delivery', 'system_delivery'])
# def handle_delivery_callback(call):
#     if call.data == 'cash_on_delivery':
#         delivery_message = '''🚚 Доставка наложним платежем
#
#             📍 При обранні цього виду доставки ви вказуєте ціну, яку ми запропонували вам при оцінці товару.
#             📍 Вартість товару разом з вартістю доставки буде сплачуватися при отриманні товару.
#             Мінуси 🛑
#             Ви отримаєте гроші тільки після того, як ми оплатимо товар на пошті.'''
#         bot.send_message(call.message.chat.id, delivery_message)
#
#         markup = types.InlineKeyboardMarkup(row_width=1)
#         continue_button = types.InlineKeyboardButton('Обрати доставку наложним платежем', callback_data='continue_cash_on_delivery')
#         markup.add(continue_button)
#         bot.send_message(call.message.chat.id, 'Оберіть дію:', reply_markup=markup)
#     elif call.data == 'system_delivery':
#         delivery_message = '''💳 Доставка через систему
#
#             📍 Доставка здійснюється також наложним платежем.
#             📍 При відправці ви не вказуєте ціни.
#             📍 Як тільки ми отримаємо товар, гроші будуть моментально перечислені на вашу карту.'''
#         markup = types.InlineKeyboardMarkup(row_width=1)
#         continue_button = types.InlineKeyboardButton('Обрати доставку наложним платежем', callback_data='continue_cash_on_delivery')
#         markup.add(continue_button)
#         bot.send_message(call.message.chat.id, delivery_message, reply_markup=markup)
# @bot.callback_query_handler(func=lambda call: call.data == 'continue_cash_on_delivery')
# def handle_continue_cash_on_delivery(call):
#     continue_message = 'Ви обрали доставку наложним платежем. Будь ласка, продовжте процес замовлення.'
#     bot.send_message(call.message.chat.id, continue_message)



# Цей код працює
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
            bot.send_message(message.chat.id,
                             "Ми поважаємо твоє рішення. \n\n📍Один з працівників ознайомиться з твоїм замовленням, та *можливо буде запропонована інша ціна*.")
            update_price_status(current_order_number, 14)  # Змінити статус на 3

            propose_price(message, owner_id, group_id)
        else:
            bot.send_message(message.chat.id,"Ти вже зробив вибір")




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

# Функція для обробки ціни та збереження її до користувача

def process_price(message,order_number, user_id):
    # conn2 = sqlite3.connect('photos.db')
    # cursor2 = conn2.cursor()
    # cursor2.execute('UPDATE photos SET price_status=None',
    #                (user_id, order_number))
    # conn2.commit()
    # conn2.close()
    update_price_status(order_number, None)

    price = message.text
    bot.send_message(user_id, f"‼️*Запропонована нами ціна* за замовлення #{order_number}: *{price}  грн*", parse_mode='Markdown')

    # Здійснюємо дії з ціною, наприклад, зберігаємо її в базі даних

    # Оновлюємо запис у базі даних, пов'язаний з користувачем і номером замовлення
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE photos SET status = 2, Price = ? WHERE user_id = ? AND order_number = ?', (price, user_id, order_number))
    conn.commit()
    conn.close()
    # Зберегти номер замовлення в змінну
    global current_order_number
    current_order_number = order_number

    # Відправити повідомлення з кнопками
    markup = types.InlineKeyboardMarkup(row_width=2)
    yes_button = types.InlineKeyboardButton('✅ Так', callback_data='yes')
    no_button = types.InlineKeyboardButton('❌ Ні', callback_data='no')
    markup.add(yes_button, no_button)
    bot.send_message(user_id, 'Погоджуєшся з ціною?', reply_markup=markup)

# def process_price(message, owner_id, order_number):
#     price = message.text
#
#     # Відправити ціну власнику замовлення
#     bot.send_message(owner_id, f"Ціна замовлення #{order_number}: {price}  грн")
#
#     # Оновлення статусу замовлення та збереження ціни в базі даних
#     conn = sqlite3.connect('photos.db')
#     cursor = conn.cursor()
#     cursor.execute('UPDATE photos SET status = 2, Price = ? WHERE order_number = ?', (price, order_number))
#     conn.commit()
#     cursor.close()
#     conn.close()
#
#     # Зберегти номер замовлення в змінну
#     global current_order_number
#     current_order_number = order_number
#
#     # Відправити повідомлення з кнопками
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     yes_button = types.InlineKeyboardButton('Так', callback_data='yes')
#     no_button = types.InlineKeyboardButton('Ні', callback_data='no')
#     markup.add(yes_button, no_button)
#     bot.send_message(owner_id, 'Погоджуєтесь з ціною?', reply_markup=markup)





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
                 🚚 Доставка наложним платежем

‼️ При обранні цього виду доставки при відправці товару, треба вказати таку ціну, яку ми запропонували вам при оцінці товару.
‼️ Вартість товару разом з вартістю доставки буде сплачуватися при отриманні товару. 
‼️ Дані для відправки будуть переслані після того, як натиснеш “✅ Обрати доставку наложним платежем”.
 *Недоліки:*
 📍 Ти зможеш отримати гроші лише після того, як ми оплатимо товар на пошті."""

            markup = types.InlineKeyboardMarkup(row_width=1)
            choose_cod_button = types.InlineKeyboardButton('✅ Обрати доставку наложним платежем',
                                                           callback_data='choose_cod')
            markup.add(choose_cod_button)
            bot.send_message(owner_id, delivery1_message, reply_markup=markup)

        else:
            bot.send_message(owner_id, "Ти вже обрав спосіб доставки.")

    elif call.data == 'delivery2':

        if get_delivery_status(current_order_number) is None:
            update_order_status(current_order_number, 4)  # Змінити статус на 4

            # Відправити повідомлення про доставку №2
            delivery2_message = """
💳 Доставка через систему

‼️ Доставка здійснюється також наложним платежем.
‼️ При відправці ти не вказуєш ціни за товар.
‼️ Як тільки ми отримаємо товар, гроші будуть моментально перечислені на твою карту.

‼️ Дані для відправки будуть переслані після того, як натиснеш “✅ Обрати доставку через систему”.
               """

            markup = types.InlineKeyboardMarkup(row_width=1)
            choose_system_delivery_button = types.InlineKeyboardButton('✅ Обрати доставку через систему',
                                                                       callback_data='choose_system_delivery')
            markup.add(choose_system_delivery_button)
            bot.send_message(owner_id, delivery2_message, reply_markup=markup)

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
                         f'‼️Як тільки ви відправите замовлення, *прикріпіть накладну*, натиснувши:\n"Мої замовлення" ➡️ "Відправити номер накладної".',
                         parse_mode='Markdown')
        bot.send_message(group_id,
                         f"@{message.chat.username} з ід `{message.chat.id}` обрав доставку наложним платежем\n Номер замовлення: {current_order_number}",parse_mode="MarkdownV2")
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
                         f'‼️Як тільки ви відправите замовлення, *прикріпіть накладну*, натиснувши:\n"Мої замовлення" ➡️ "Відправити номер накладної". \nТам ж само ви можете прикріпити номер карти.',
                         parse_mode='Markdown')
        bot.send_message(group_id,
                         f"@{message.chat.username} з ід `{message.chat.id}` обрав доставку через систему\n Номер замовлення: {current_order_number}",parse_mode="MarkdownV2")
    else:
        bot.send_message(owner_id, "Ти вже обрав спосіб доставки.")


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
    conn.commit()
    cursor.close()
    conn.close()
# def get_delivery_option(option):
#     if option == 'choose_delivery':
#         return 1  # Значення для доставки наложним платежем
#     elif option == 'delivery_option2':
#         return 2  # Значення для доставки через систему

# Очищення змінної current_order_number при перезапуску бота
current_order_number = 1


@bot.message_handler(func=lambda message: message.text == 'Речі, які ми купуємо')
def handle_buying_items(message):
    markup = create_inline_keyboard()
    bot.send_message(message.chat.id, 'Ось список речей, які ми купуємо:', reply_markup=markup)


def create_inline_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_nike = types.InlineKeyboardButton('Nike', callback_data='buying_item_nike')
    button_adidas = types.InlineKeyboardButton('Adidas', callback_data='buying_item_adidas')
    button_reebok = types.InlineKeyboardButton('Reebok', callback_data='buying_item_reebok')
    button_champion = types.InlineKeyboardButton('Champion', callback_data='buying_item_champion')
    button_lacoste = types.InlineKeyboardButton('Lacoste', callback_data='buying_item_lacoste')
    button_ralph_lauren = types.InlineKeyboardButton('Ralph Lauren', callback_data='buying_item_ralph_lauren')
    button_carhartt = types.InlineKeyboardButton('Carhartt', callback_data='buying_item_carhartt')
    button_dickies = types.InlineKeyboardButton('Dickies', callback_data='buying_item_dickies')
    button_stussy = types.InlineKeyboardButton('Stüssy', callback_data='buying_item_stussy')

    markup.add(
        button_nike, button_adidas, button_reebok, button_champion,
        button_lacoste, button_ralph_lauren, button_carhartt, button_dickies, button_stussy
    )

    return markup


@bot.callback_query_handler(func=lambda call: call.data.startswith('buying_item_'))
def handle_buying_item_callback(call):
    item_name = call.data.replace('buying_item_', '')

    if item_name == 'nike':
        message = '''
        Nike

- Вінтажні кофти, з маленьким та з великим лого.
- Вінтажні футболки, з маленьким та з великим лого.
- Вінтажні штани та шорти, на стяжках, карго.
        '''
    elif item_name == 'adidas':
        message = '''Adidas

- Вінтажні кофти, з маленьким та з великим лого.
- Вінтажні футболки, з маленьким та з великим лого.
- Adidas Equipment.'''
    elif item_name == 'reebok':
        message = '''Reebok

- Вінтажні кофти, з маленьким та з великим лого.'''
    elif item_name == 'champion':
        message = '''Champion

- Вінтажні кофти, з маленьким та з великим лого.
'''
    elif item_name == 'lacoste':
        message = '''Lacoste 

- Вінтажні кофти, светри.
- Футболки, поло.
- Бомбери.'''
    elif item_name == 'ralph_lauren':
        message = '''Ralph Lauren 

- 1/4 1/3 zip
- Harrington jackets.
- Поло футболки.
- Регбійки.
- Різні кофти.'''
    elif item_name == 'carhartt':
        message = '''Carhartt 

- Різні види штанів, джинсів, в будь якому стані.
- Active jackets.
- Harrington jackest.
- Кофти, худаки.
- Футболки.
- Різний Workwear.'''
    elif item_name == 'dickies':
        message = '''Dickies

- Різні види штанів, джинсів,  в будь якому стані.
- Harington Jackets.'''
    elif item_name == 'stussy':
        message = '''Stüssy

- Кофти.
- Футболки.'''
    else:
        message = 'Невідома річ'

    bot.send_message(call.message.chat.id, message)
#     917631518

bot.polling(none_stop=True)