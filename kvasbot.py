import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ChatMember
import sqlite3
from datetime import datetime, timedelta
#from background import keep_alive_live
import pytz
import time
import random
import asyncio
import re
import progress.bar as pb
from colorama import init, Style, Fore

bar = pb.ShadyBar("Загрузка", max=100)
for i in range(100):
   bar.next()
   time.sleep(0.01)
bar.finish()
init()
print(Fore.GREEN + "Бот готов к работе!")

bot = Bot(token="YourToken")
dp = Dispatcher(bot)

conn = sqlite3.connect('testing2.db')
cursor = conn.cursor()

#cursor.execute("""ALTER TABLE user_data
#ADD COLUMN kamnojby VARCHAR(100)
#""")
#conn.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS user_data(
first_name VARCHAR(50),
last_name VARCHAR(50),
user_name VARCHAR(50),
custom_name VARCHAR(50),
user_id INTEGER PRIMARY KEY,
date_exit FLOAT,
active INTEGER,
mir_poyas VARCHAR(20),
timer INTEGER,
kvas_up FLOAT,
online_up FLOAT,
num_one INTEGER,
num_two INTEGER,
num_tree INTEGER,
num_four INTEGER,
num_five INTEGER,
num_six INTEGER,
num_seven INTEGER,
hoursmine INTEGER,
minutemine INTEGER,
secondmine INTEGER,
cabimet TEXT,
stavka1 FLOAT,
time_os VARCHAR(20),
kamnojby VARCHAR(100)
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS chat_id(
id INTEGER PRIMARY KEY,
chat TEXT
)""")
conn.commit()

timers = {}
status = [""]
chaty = []

#Начало настройки часового пояса----------

UA_kiev_tz = pytz.timezone('Europe/Kiev')
RU_moscow_tz = pytz.timezone('Europe/Moscow')
KZ_almaty_tz = pytz.timezone('Asia/Almaty')

#Конец настройки часового пояса------------

list_info = ["Напишите в чат /help чтобы узнать подробные команды", "В личном сообщении бота можно настроить часовой пояс чтобы подробно узнать точное время окончания кд", "можно активировать промокод написав в чат 'промо #новый_квас_на_час' чтобы получить бонус от создателя", "Наберите больше 100 литр чтобы войти в топы", "включите уведомления, чтобы это сделать напишите в чат 'уведомления 1', вы всегда сможете их отключить написав в чат 'уведомления 0, либо же можете перейти в личку бота нажать на настройки и нажать на 'уведомления 1'/'уведомления 0'", "поставьте часовой пояс на ваш регион, всего существуют на данный момент UA_kiev/RU_moscow/KZ_almaty, подробнее о часовом поясе в команде /help", "Старайтесь не сильно рисковать в азартных играх, вообще если вам не повезло с какого то раза то лучше остановится ведь последствия будут не очень приятными", "Скоро добавим ещё больше регионов в  часовом поясе", "Спасибо @FJHGGP за галактическую аву"]

async def check_db(message: types.Message):
   conn = sqlite3.connect('testing2.db')
   cursor = conn.cursor()
   id = message.from_user.id
   firstname = message.from_user.first_name
   lastname = message.from_user.last_name
   username = message.from_user.username
   chat_id = message.chat.id
      
   cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (id,))
   data = cursor.fetchone()
   if data is None:
      cursor.execute("INSERT INTO user_data (first_name, last_name, user_name, custom_name, user_id, date_exit, active, mir_poyas, timer, kvas_up, online_up, num_one, num_two, num_tree, num_four, num_five, num_six, num_seven, hoursmine, minutemine, secondmine, cabimet, stavka1, time_os, kamnojby) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (firstname, lastname, username, "empty", id, 0, 1, "Df", 0, 0, 0, 0, 0, 0, 0, 0, chat_id, 0, 1, 0, 0, "None", 0, "None", "None"))
      conn.commit()
   else:
      if data[6] == 1:
         pass
      elif data[6] == 0:
         activn = 1
         cursor.execute("UPDATE user_data SET active = ? WHERE user_id = ?", (activn, id))
         conn.commit()
   if data:
      if data[7] == "Df":
         markup = types.InlineKeyboardMarkup(row_width=1)
         markup.add(types.InlineKeyboardButton(text="Квасометр", url="https://t.me/Kvaso_metrbot"))
         await message.reply("Пожалуйста свяжитесь со мной чтобы выбрать часовой пояс!Иначе бот будет работать некоректно.", reply_markup=markup)
      else:
         pass
   conn = sqlite3.connect('testing2.db')
   cursor = conn.cursor()
   cursor.execute("SELECT chat FROM chat_id WHERE id = ?", (0,))
   data_chat = cursor.fetchone()
   if message.chat.type == "group" or message.chat.type == "supergroup":
      if data_chat is None:
         cursor.execute("INSERT INTO chat_id (id, chat) VALUES (?, ?)", (0, chat_id))
         conn.commit()
      else:
         pass
      if data:
         if str(data[16]).startswith("-"):
            if str(data[16]) not in str(data_chat[0]):
               if data_chat[0]:
                  my_string = f"{data[16]}"
                  my_chat = [data_chat[0], my_string]
                  cursor.execute("UPDATE chat_id SET chat = ? WHERE id = ?", (f", ".join(my_chat), 0))
                  conn.commit()
               else:
                  my_chat = [data[16]]
                  cursor.execute("UPDATE chat_id SET chat = ? WHERE id = ?", (f", ".join(my_chat), 0))
                  conn.commit()
            else:
               pass
   if data:
      if data[0] != message.from_user.first_name:
         cursor.execute("UPDATE user_data SET first_name = ? WHERE user_id = ?", (message.from_user.first_name, id))
         conn.commit()
      else:
         pass
      if data[1] != message.from_user.last_name:
         cursor.execute("UPDATE user_data SET last_name = ? WHERE user_id = ?", (message.from_user.last_name, id))
         conn.commit()
      else:
         pass
      if data[2] != message.from_user.username:
         cursor.execute("UPDATE user_data SET first_name = ? WHERE user_id = ?", (message.from_user.username, id))
         conn.commit()
      else:
         pass

@dp.message_handler(commands=["drop", "droptable"])
async def dropping(message: types.Message):
   await message.answer("hi")
   conn = sqlite3.connect('testing2.db')
   cursor = conn.cursor()
   cursor.execute("DELETE FROM user_data")
#   cursor.execute("DELETE FROM chat_id")
   conn.commit()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
   if message.chat.type == "private":
      await check_db(message)
      await bot.send_sticker(message.from_user.id, random.choice(["CAACAgIAAxkBAAEKVpplCgbYDHiL5mmGfBnEdP-dEG00hQACPxUAApRF2UvlLdme07UyVzAE", "CAACAgQAAxkBAAEKVqBlCgiLKubaxw7oJqyQkHHGlmh-LgACdAsAApMNuFMOGzz8EcFY_jAE"]))
      markup = types.InlineKeyboardMarkup()
      markup.add(types.InlineKeyboardButton("Добавить меня", url="https://t.me/Kvaso_metrbot?startgroup=invite"))
      await message.answer("Также вы можете меня добавить в вашу группу нажав на кнопку 'Добавить меня'", reply_markup=markup)
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      markup.add('🍻Выпить кваса')
      markup.add('📈Топ', '🧰Помощь', '⚙️Настройки', '🎮Игры', "📝Сообщить о ошибке")
      if message.chat.id == 1017848661:
         markup.add('⌨️ Админ панель')
      await message.answer("Добро пожаловать, чтобы узнать все команды напишите /help", reply_markup=markup)
   elif message.chat.type == "channel":
      await message.answer("К сожалению на канале нельзя взаимодействовать с ботом...")
      await check_db(message)
   elif message.chat.type == "supergroup" or message.chat.type == "group":
         markup = types.InlineKeyboardMarkup(row_width=1)
         markup.add(types.InlineKeyboardButton(text="Квасометр", url="https://t.me/Kvaso_metrbot"))
         await message.answer("Привет всем!Подробные команды можно узнать написав команду /help", reply_markup=markup)

@dp.message_handler(commands=['help'])
async def start(message: types.Message):
   if message.chat.type == "private":
         await message.answer("Нажмите на кнопку '🧰Помощь'")
   elif message.chat.type == "channel":
      await message.reply("К сожалению на канале нельзя взаимодействовать с ботом...")
      await check_db(message)
   elif message.chat.type == "supergroup" or "group":
      await check_db(message)
      markup = types.InlineKeyboardMarkup(row_width=1)
      markup.add(types.InlineKeyboardButton("зачем нужен часовой пояс?", callback_data="mir_poyasq"))
      await message.answer("Тут собраны все команды и пояснения...\n\n/help - команда для пояснений\n/kvas_up - выпить кваса\n/top_in_group - топ литров этого чата \n/top - топ всех людей начиная с 100л.\n", reply_markup=markup)

@dp.message_handler(commands=['kvas_up'])
async def kvasingup (message: types.Message):
   if message.chat.type == "group" or "supergroup":
      conn = sqlite3.connect('testing2.db')
      cursor = conn.cursor()
      id = message.from_user.id
      cursor.execute("SELECT active, mir_poyas, kvas_up, timer, hoursmine, minutemine, secondmine, num_two, time_os FROM user_data WHERE user_id = ?", (id,))
      data = cursor.fetchone()
      await check_db(message)
      if id not in timers:
         randoms = round(random.uniform(0.01, 5.00), 2)
         kvas_up = data[2] + randoms
         ranwor = random.choice(list_info)
         cursor.execute("UPDATE user_data SET kvas_up = ? WHERE user_id = ?", (kvas_up, id))
         conn.commit()
         istimer = 1
         cursor.execute("UPDATE user_data SET timer = ? WHERE user_id = ?", (istimer, id))
         conn.commit()
         timers[id] = True
         if data[1] == "UA_kiev":
            ua_now = datetime.now(UA_kiev_tz).time()
            delta = timedelta(hours=1)
            new_ua_time = (datetime.combine(datetime.min, ua_now) + delta).time()
            new_ua_nsw = new_ua_time.strftime("%H:%M:%S")
            cursor.execute("UPDATE user_data SET time_os = ? WHERE user_id = ?", (new_ua_nsw, id))
            conn.commit()
         elif data[1] == "RU_moscow":
            ru_now = datetime.now(RU_moscow_tz)
            ru_time = ru_now.time()
            delta = timedelta(hours=1)
            new_ru_time = (datetime.combine(datetime.min, ru_time) + delta).time()
            new_ru_nsw = new_ru_time.strftime("%H:%M:%S")
            cursor.execute("UPDATE user_data SET time_os = ? WHERE user_id = ?", (new_ru_nsw, id))
            conn.commit()
         elif data[1] == "KZ_almaty":
             kz_now = datetime.now(KZ_almaty_tz)
             kz_time = kz_now.time()
             delta = timedelta(hours=1)
             new_kz_time = (datetime.combine(datetime.min, kz_time) + delta).time()
             new_kz_nsw = new_kz_time.strftime("%H:%M:%S")
             cursor.execute("UPDATE user_data SET time_os = ? WHERE user_id = ?", (new_kz_nsw, id))
             conn.commit()
         else:
            current_time_seconds = time.time()
            current_time_struct = time.localtime(current_time_seconds)
            real_time = [current_time_struct.tm_hour, current_time_struct.tm_min, current_time_struct.tm_sec]
            real_btime = real_time[0] + 1
            timing_is = f"{real_time[0]}:{real_time[1]}:{real_btime}"
            cursor.execute("UPDATE user_data SET time_os = ? WHERE user_id = ?", (timing_is, id))
            conn.commit()
         if data[1] == "UA_kiev":
            await message.reply(f"Игрок <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> выпил(а) <b>{randoms}л</b>\nВы сможете выпить в " + str(new_ua_nsw) + f"\n\n<i>советы:</i> {ranwor}", parse_mode="html", disable_web_page_preview=True)
            await asyncio.sleep(3600)
            del timers[id]
            if data[7] == 0:
               await message.answer(f"@{message.from_user.username} время подошло к концу")
         elif data[1] == "RU_moscow":
            await message.reply(f"Игрок <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> выпил(а) <b>{randoms}л</b>\nВы сможете выпить в "+ str(new_ru_nsw) + f"\n\n<i>советы:</i> {ranwor}", parse_mode="html", disable_web_page_preview=True)
            await asyncio.sleep(3600)
            del timers[id]
            if data[7] == 0:
               await message.answer(f"@{message.from_user.username} время подошло к концу")
         elif data[1] == "KZ_almaty":
            await message.reply(f"Игрок <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> выпил(а) <b>{randoms}л</b>\nВы сможете выпить в " + str(new_kz_nsw) + f"\n\n<i>советы:</i> {ranwor}", parse_mode="html", disable_web_page_preview=True)
            await asyncio.sleep(3600)
            del timers[id]
            if data[7] == 0:
               await message.answer(f"@{message.from_user.username} время подошло к концу")
         else:
             await message.reply(f"Игрок <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> выпил(а) <b>{randoms}л</b>\nВы сможете выпить в {real_btime}:{real_time[1]}:{real_time[2]}\n\n<i>советы:</i> {ranwor}", parse_mode="html", disable_web_page_preview=True)
             await asyncio.sleep(3600)
             del timers[id]
             if data[7] == 0:
               await message.answer(f"@{message.from_user.username} время подошло к концу")
      else:
          if data[1] == "UA_kiev":
                 time_format = "%H:%M:%S"
                 ua_now = datetime.now(UA_kiev_tz)
                 time1 = datetime.strptime(data[8], time_format)
                 ua_str = ua_now.strftime(time_format)
                 time2 = datetime.strptime(ua_str, time_format)
                 if time1 < time2:
                    time1 = time1 + timedelta(days=1)
                 time_minus = time1 - time2
                 time_str = str(time_minus)
                 await message.answer("Время ещё не прошло, вы сможете снова выпить через {}".format(time_str))
          elif data[1] == "RU_moscow":
                 time_format = "%H:%M:%S"
                 ru_now = datetime.now(RU_moscow_tz)
                 time1 = datetime.strptime(data[8], time_format)
                 ru_str = ru_now.strftime(time_format)
                 time2 = datetime.strptime(ru_str, time_format)
                 if time1 < time2:
                    time1 = time1 + timedelta(days=1)
                 time_minus = time1 - time2
                 time_str = str(time_minus)
                 await message.answer("Время ещё не прошло, вы сможете снова выпить в {}".format(time_str))
          elif data[1] == "KZ_almaty":
                 time_format = "%H:%M:%S"
                 kz_now = datetime.now(KZ_almaty_tz)
                 time1 = datetime.strptime(data[8], time_format)
                 kz_str = kz_now.strftime(time_format)
                 time2 = datetime.strptime(kz_str, time_format)
                 if time1 < time2:
                    time1 = time1 + timedelta(days=1)
                 time_minus = time1 - time2
                 time_str = str(time_minus)
                 await message.answer("Время ещё не прошло, вы сможете снова выпить в {}".format(time_str))
          else:
                 await message.answer("Время ещё не прошло, вы сможете выпить в {}\n\nПочему вы всё ещё не выбрали регеон?".format(data[8]))

@dp.message_handler(commands=['top'])
async def topping (message: types.Message):
   if message.chat.type == "group" or "supergroup":
      conn = sqlite3.connect('testing2.db')
      cursor = conn.cursor()
      id = message.from_user.id
      first_name_0 = message.from_user.first_name
            
      cursor.execute("SELECT first_name, kvas_up FROM user_data ORDER BY kvas_up DESC")
      data = cursor.fetchall()
      await check_db(message)
      output = ""
      one_numer = 0
      for record in data:
         first_name, kvas_up = record
         kvas_up_float = float(kvas_up)
         if float(kvas_up) > 99.99:
            one_numer += 1
            if first_name == first_name_0:
               output += f"<u>{one_numer}. <b>{first_name}</b> - {round(kvas_up_float, 2)}л</u>\n"
            else:
               output += f"{one_numer}. <b>{first_name}</b> - {round(kvas_up_float, 2)}л\n"
      await message.answer(f"Вот статистика всех людей у кого больше 100л.\n\n{output}", parse_mode="html")
      cursor.execute("SELECT first_name, kvas_up FROM user_data WHERE user_id = ?", (id,))
      data = cursor.fetchone()
      await message.answer(f"У вас: {data[1]}л.")

@dp.message_handler(commands=['top_in_group'])
async def toppinggroup(message: types.Message):
    if message.chat.type in ["group", "supergroup"]:
        conn = sqlite3.connect('testing2.db')
        cursor = conn.cursor()
        chat_id = message.chat.id
        first_name_0 = message.from_user.first_name
        id = message.from_user.id

        cursor.execute("SELECT first_name, kvas_up, user_id, num_six FROM user_data ORDER BY kvas_up DESC")
        data = cursor.fetchall()
        cursor.execute("UPDATE user_data SET num_six = ? WHERE user_id = ?", (chat_id, id))
        conn.commit()
        cursor.execute("SELECT first_name, kvas_up, user_id, num_six FROM user_data ORDER BY kvas_up DESC")
        data = cursor.fetchall()
        await check_db(message)
        output = ""
        one_numer = 0

        for user_data in data:
            first_name, kvas_up, user_id, num_six = user_data
            kvas_up_float = float(kvas_up)
            
            if num_six == message.chat.id:
                one_numer += 1
                if first_name == first_name_0:
                   output += f"<u>{one_numer}. <b>{first_name}</b> - {round(kvas_up_float, 2)}л</u>\n"
                else:
                   output += f"<b>{one_numer}. {first_name}</b> - {round(kvas_up_float, 2)}л\n"
        
        await message.answer(f"Вот статистика всех людей, которые в этой группе:\n{output}", parse_mode="html")

@dp.message_handler(commands=['send'])
async def send(message: types.Message):
   if message.chat.type == "private":
       if message.from_user.id == 1017848661:
           try:
               args = message.get_args().split()
               argss = " ".join(args[1:])
               user = message.text.split()
               
               ua_naw = datetime.now(UA_kiev_tz)
               ru_naw = datetime.now(RU_moscow_tz)
               kz_naw = datetime.now(KZ_almaty_tz)
               
               ua_nsw = ua_naw.strftime("%H:%M:%S")
               ru_nsw = ru_naw.strftime("%H:%M:%S")
               kz_nsw = kz_naw.strftime("%H:%M:%S")
               
               await bot.send_message(user[1], "Вам было отправлено сообщение от модераторов\n{}\n⏰Time: \n🇺🇦UA:{}\n🇷🇺RU:{}\n🇵🇼KZ:{}".format(argss, ua_nsw, ru_nsw, kz_nsw))
               
               await message.answer("Вы успешно отправили сообщение")
               
           except Exception as e:
                await message.answer(f"Данный пользователь {user[1]} удалил чат с ботом или не активный\nОшибка: {e}")
       else:
            await message.answer("Вам запрещено использовать эту команду")

@dp.message_handler(commands=['bonus'])
async def send(message: types.Message):
   if message.chat.type == "private":
       if message.from_user.id == 1017848661:
           try:
               conn = sqlite3.connect('testing2.db')
               cursor = conn.cursor()
               id = message.from_user.id
               
               cursor.execute("SELECT kvas_up FROM user_data")
               args = message.get_args().split()
               user = int(args[0])
               count = str(args[1:])
               count_list = ' '.join(count).strip('[]')
               my_string = count_list.replace("'", "")
               my_super = my_string.replace(" ", "")
               await message.answer(f"{my_super}")
               cursor.execute("UPDATE user_data SET kvas_up = kvas_up + ? WHERE user_id = ?", (my_super, user))
               conn.commit()
               await bot.send_message(user, "Вам было выдано бонус за помощь в поиске ошибок")
               await message.answer("Вы успешно начислили пользователю бонус")
           except Exception as e:
               await message.answer(f"Данный пользователь {user} удалил чат с ботом или не активный\nОшибка: {e}")

@dp.message_handler(content_types=['text'])
async def texted(message: types.Message):
   if message.text == "🍻Выпить кваса":
      if message.chat.type == "private":
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
         firstname = message.from_user.first_name
         lastname = message.from_user.last_name
         username = message.from_user.username
         chat_id = message.chat.id
         
         cursor.execute("SELECT active, mir_poyas, kvas_up, timer, hoursmine, minutemine, secondmine, num_two, time_os FROM user_data WHERE user_id = ?", (id,))
         data = cursor.fetchone()
         if data[0] == 0:
               activn = 1
               cursor.execute("UPDATE user_data SET active = ? WHERE user_id = ?", (activn, id))
               conn.commit()
         else:
               pass
         if id not in timers:
                randoms = round(random.uniform(0.01, 5.00), 2)
                kvas_up = data[2] + randoms
                ranwor = random.choice(list_info)
                cursor.execute("UPDATE user_data SET kvas_up = ? WHERE user_id = ?", (kvas_up, id))
                conn.commit()
                istimer = 1
                cursor.execute("UPDATE user_data SET timer = ? WHERE user_id = ?", (istimer, id))
                conn.commit()
                timers[id] = True
                if data[1] == "UA_kiev":
                   ua_now = datetime.now(UA_kiev_tz)
                   ua_time = ua_now.time()
                   delta = timedelta(hours=1)
                   new_ua_time = (datetime.combine(datetime.min, ua_time) + delta).time()
                   new_ua_nsw = new_ua_time.strftime("%H:%M:%S")
                   cursor.execute("UPDATE user_data SET time_os = ? WHERE user_id = ?", (new_ua_nsw, id))
                   conn.commit()
                elif data[1] == "RU_moscow":
                   ru_now = datetime.now(RU_moscow_tz)
                   ru_time = ru_now.time()
                   delta = timedelta(hours=1)
                   new_ru_time = (datetime.combine(datetime.min, ru_time) + delta).time()
                   new_ru_nsw = new_ru_time.strftime("%H:%M:%S")
                   cursor.execute("UPDATE user_data SET time_os = ? WHERE user_id = ?", (new_ru_nsw, id))
                   conn.commit()
                elif data[1] == "KZ_almaty":
                   kz_now = datetime.now(KZ_almaty_tz)
                   kz_time = kz_now.time()
                   delta = timedelta(hours=1)
                   new_kz_time = (datetime.combine(datetime.min, kz_time) + delta).time()
                   new_kz_nsw = new_kz_time.strftime("%H:%M:%S")
                   cursor.execute("UPDATE user_data SET time_os = ? WHERE user_id = ?", (new_kz_nsw, id))
                   conn.commit()
                else:
                   current_time_seconds = time.time()
                   current_time_struct = time.localtime(current_time_seconds)
                   real_time = [current_time_struct.tm_hour, current_time_struct.tm_min, current_time_struct.tm_sec]
                   real_btime = real_time[0] + 1
                   timing_is = f"{real_time[0]}:{real_time[1]}:{real_btime}"
                   cursor.execute("UPDATE user_data SET time_os = ? WHERE user_id = ?", (timing_is, id))
                   conn.commit()
                if data[1] == "UA_kiev":
                   await message.reply(f"Игрок <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> выпил(а) <b>{randoms}л</b>\nВы сможете выпить в " + str(new_ua_nsw) + f"\n\n<i>советы:</i> {ranwor}", parse_mode="html", disable_web_page_preview=True)
                   await asyncio.sleep(3600)
                   del timers[id]
                   if data[7] == 0:
                      await message.answer(f"@{message.from_user.username} время подошло к концу")
                elif data[1] == "RU_moscow":
                   await message.reply(f"Игрок <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> выпил(а) <b>{randoms}л</b>\nВы сможете выпить в " + str(new_ru_nsw) + f"\n\n<i>советы:</i> {ranwor}", parse_mode="html", disable_web_page_preview=True)
                   await asyncio.sleep(3600)
                   del timers[id]
                   if data[7] == 0:
                      await message.answer(f"@{message.from_user.username} время подошло к концу")
                elif data[1] == "KZ_almaty":
                   await message.reply(f"Игрок <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> выпил(а) <b>{randoms}л</b>\nВы сможете выпить в " + str(new_kz_nsw) + f"\n\n<i>советы:</i> {ranwor}", parse_mode="html", disable_web_page_preview=True)
                   await asyncio.sleep(3600)
                   del timers[id]
                   if data[7] == 0:
                      await message.answer(f"@{message.from_user.username} время подошло к концу")
                else:
                    await message.reply(f"Игрок <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> выпил(а) <b>{randoms}л</b>\nВы сможете выпить в {real_btime}:{real_time[1]}:{real_time[2]}\n\n<i>советы:</i> {ranwor}", parse_mode="html", disable_web_page_preview=True)
                    await asyncio.sleep(3600)
                    del timers[id]
                    if data[7] == 0:
                      await message.answer(f"@{message.from_user.username} время подошло к концу")
         else:
                 if data[1] == "UA_kiev":
                       time_format = "%H:%M:%S"
                       ua_now = datetime.now(UA_kiev_tz)
                       time1 = datetime.strptime(data[8], time_format)
                       ua_str = ua_now.strftime(time_format)
                       time2 = datetime.strptime(ua_str, time_format)
                       if time1 < time2:
                          time1 = time1 + timedelta(days=1)
                       time_minus = time1 - time2
                       time_str = str(time_minus)
                       await message.answer("Время ещё не прошло, вы сможете снова выпить в {}".format(time_str))
                 elif data[1] == "RU_moscow":
                        time_format = "%H:%M:%S"
                        ru_now = datetime.now(RU_moscow_tz)
                        time1 = datetime.strptime(data[8], time_format)
                        ru_str = ru_now.strftime(time_format)
                        time2 = datetime.strptime(ru_str, time_format)
                        if time1 < time2:
                           time1 = time1 + timedelta(days=1)
                        time_minus = time1 - time2
                        time_str = str(time_minus)
                        await message.answer("Время ещё не прошло, вы сможете снова выпить в {}".format(data[8]))
                 elif data[1] == "KZ_almaty":
                        time_format = "%H:%M:%S"
                        kz_now = datetime.now(KZ_almaty_tz)
                        time1 = datetime.strptime(data[8], time_format)
                        kz_str = kz_now.strftime(time_format)
                        time2 = datetime.strptime(kz_str, time_format)
                        if time1 < time2:
                           time1 = time1 + timedelta(days=1)
                        time_minus = time1 - time2
                        time_str = str(time_minus)
                        await message.answer("Время ещё не прошло, вы сможете снова выпить в {}.".format(data[8]))
                 else:
                     await message.answer("Время ещё не прошло, вы сможете снова выпить в {}\n\nПочему вы всё ещё не выбрали регеон?".format(data[8]))
   elif message.text == "⚙️Настройки":
      if message.chat.type == "private":
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
         
         cursor.execute("SELECT num_one, mir_poyas, active, online_up, user_id, date_exit, num_seven, num_two FROM user_data WHERE user_id = ?", (id,))
         data = cursor.fetchone()
         cursor.execute("UPDATE user_data SET num_seven = ? WHERE user_id = ?", (1, id))
         conn.commit()
         await check_db(message)
         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
         if data[7] == 0:
            markup.add("уведомления 1")
         else:
            markup.add("уведомления 0")
         markup.add("выбрать часовой пояс")
         markup.add("Назад")
         await message.answer(f"Добро пожаловать {message.from_user.first_name} в ⚙️Настройки\n\n⚙️Все настройки:\n   🔔уведомления: {data[7]}\n   🕧Часовой пояс: {data[1]}", reply_markup=markup)
   elif message.text == "Назад":
      if message.chat.type == "private":
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
         
         cursor.execute("SELECT num_seven, num_two, mir_poyas FROM user_data WHERE user_id = ?", (id,))
         data = cursor.fetchone()
         await check_db(message)
         if data[0] == 1:
            cursor.execute("UPDATE user_data SET num_seven = ? WHERE user_id = ?", (0, id))
            conn.commit()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('🍻Выпить кваса')
            markup.add('📈Топ', '🧰Помощь', '⚙️Настройки', '🎮Игры', "📝Сообщить о ошибке")
            if message.chat.id == 1017848661:
               markup.add('⌨️ Админ панель')
            await message.answer("Добро пожаловать, скоро здесь появятся кнопки, soon...", reply_markup=markup)
         elif data[0] == 3:
            cursor.execute("UPDATE user_data SET num_seven = ? WHERE user_id = ?", (0, id))
            conn.commit()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('🍻Выпить кваса')
            markup.add('📈Топ', '🧰Помощь', '⚙️Настройки', '🎮Игры', "📝Сообщить о ошибке")
            if message.chat.id == 1017848661:
              markup.add('⌨️ Админ панель')
            await message.answer("Добро пожаловать, скоро здесь появятся кнопки, soon...", reply_markup=markup)
         elif data[0] == 2:
            cursor.execute("UPDATE user_data SET num_seven = ? WHERE user_id = ?", (1, id))
            conn.commit()
            await check_db(message)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            if data[1] == 0:
               markup.add("уведомления 1")
            else:
               markup.add("уведомления 0")
            markup.add("выбрать часовой пояс")
            markup.add("Назад")
            await message.answer(f"Добро пожаловать {message.from_user.first_name} в ⚙️Настройки\n\n⚙️Все настройки:\n   🔔уведомления: {data[1]}\n   🕧Часовой пояс: {data[2]}", reply_markup=markup)
   elif message.text == "уведомления 1":
      if message.chat.type == "private":
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
         
         cursor.execute("SELECT num_seven, num_two, mir_poyas FROM user_data WHERE user_id = ?", (id,))
         data = cursor.fetchone()
         await check_db(message)
         if data[0] == 1:
            if data[1] == 0:
               cursor.execute("UPDATE user_data SET num_two = ? WHERE user_id = ?", (1, id))
               conn.commit()
               await message.answer("Вы успешно установили значения уведомлений на 1")
               cursor.execute("SELECT num_seven, num_two, mir_poyas FROM user_data WHERE user_id = ?", (id,))
               data = cursor.fetchone()
               markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
               if data[1] == 0:
                  markup.add("уведомления 1")
               else:
                  markup.add("уведомления 0")
               markup.add("выбрать часовой пояс")
               markup.add("Назад")
               await message.answer(f"Добро пожаловать {message.from_user.first_name} в ⚙️Настройки\n\n⚙️Все настройки:\n   🔔уведомления: {data[1]}\n   🕧Часовой пояс: {data[2]}", reply_markup=markup)
   elif message.text == "уведомления 0":
      if message.chat.type == "private":
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
         
         cursor.execute("SELECT num_seven, num_two, mir_poyas FROM user_data WHERE user_id = ?", (id,))
         data = cursor.fetchone()
         await check_db(message)
         if data[0] == 1:
            if data[1] == 1:
               cursor.execute("UPDATE user_data SET num_two = ? WHERE user_id = ?", (0, id))
               conn.commit()
               await message.answer("Вы успешно установили значения уведомлений на 0")
               cursor.execute("SELECT num_seven, num_two, mir_poyas FROM user_data WHERE user_id = ?", (id,))
               data = cursor.fetchone()
               markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
               if data[1] == 0:
                  markup.add("уведомления 1")
               else:
                  markup.add("уведомления 0")
               markup.add("выбрать часовой пояс")
               markup.add("Назад")
               await message.answer(f"Добро пожаловать {message.from_user.first_name} в ⚙️Настройки\n\n⚙️Все настройки:\n   🔔уведомления: {data[1]}\n   🕧Часовой пояс: {data[2]}", reply_markup=markup)
   elif message.text == "выбрать часовой пояс":
      if message.chat.type == "private":
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
         
         cursor.execute("SELECT num_seven, mir_poyas FROM user_data WHERE user_id = ?", (id,))
         data = cursor.fetchone()
         await check_db(message)
         if data[0] == 1:
            cursor.execute("UPDATE user_data SET num_seven = ? WHERE user_id = ?", (2, id))
            conn.commit()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("UA_kiev", "RU_moscow")
            markup.add("KZ_almaty")
            markup.add("Назад")
            
            await message.answer(f"На данный момент у вас стоит\n🕧Часовой пояс: {data[1]}\n\nЕсли у вас стоит Df(Default) то нажмите на вариант из трёх кнопок: \n 🇺🇦 UA_kiev(Киев),\n 🇷🇺 RU_moscow(Москва),\n 🇰🇿 KZ_almaty(Алматы)", reply_markup=markup)
   elif message.text == "RU_moscow":
      if message.chat.type == "private":
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
         
         cursor.execute("SELECT num_seven, num_two, mir_poyas FROM user_data WHERE user_id = ?", (id,))
         data = cursor.fetchone()
         await check_db(message)
         if data[0] == 2:
            if data[2] != "RU_moscow":
               cursor.execute("UPDATE user_data SET mir_poyas = ? WHERE user_id = ?", ("RU_moscow", id))
               conn.commit()
               cursor.execute("SELECT num_seven, num_two, mir_poyas FROM user_data WHERE user_id = ?", (id,))
               data = cursor.fetchone()
               markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
               markup.add("UA_kiev", "RU_moscow")
               markup.add("KZ_almaty")
               markup.add("Назад")
               
               await message.answer(f"На данный момент у вас стоит\n🕧Часовой пояс: {data[2]}\n\nЕсли у вас стоит Df(Default) то нажмите на вариант из трёх кнопок: \n 🇺🇦 UA_kiev(Киев),\n 🇷🇺 RU_moscow(Москва),\n 🇰🇿 KZ_almaty(Алматы)\nВы всегда сможете сменить часовой пояс", reply_markup=markup)
   elif message.text == "UA_kiev":
      if message.chat.type == "private":
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
         
         cursor.execute("SELECT num_seven, num_two, mir_poyas FROM user_data WHERE user_id = ?", (id,))
         data = cursor.fetchone()
         await check_db(message)
         if data[0] == 2:
            if data[2] != "UA_kiev":
               cursor.execute("UPDATE user_data SET mir_poyas = ? WHERE user_id = ?", ("UA_kiev", id))
               conn.commit()
               cursor.execute("SELECT num_seven, num_two, mir_poyas FROM user_data WHERE user_id = ?", (id,))
               data = cursor.fetchone()
               markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
               markup.add("UA_kiev", "RU_moscow")
               markup.add("KZ_almaty")
               markup.add("Назад")
               
               await message.answer(f"На данный момент у вас стоит\n🕧Часовой пояс: {data[2]}\n\nЕсли у вас стоит Df(Default) то нажмите на вариант из трёх кнопок: \n 🇺🇦 UA_kiev(Киев),\n 🇷🇺 RU_moscow(Москва),\n 🇰🇿 KZ_almaty(Алматы)\nВы всегда сможете сменить часовой пояс", reply_markup=markup)
   elif message.text == "KZ_almaty":
      if message.chat.type == "private":
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
         
         cursor.execute("SELECT num_seven, num_two, mir_poyas FROM user_data WHERE user_id = ?", (id,))
         data = cursor.fetchone()
         await check_db(message)
         if data[0] == 2:
            if data[2] != "KZ_almaty":
               cursor.execute("UPDATE user_data SET mir_poyas = ? WHERE user_id = ?", ("KZ_almaty", id))
               conn.commit()
               cursor.execute("SELECT num_seven, num_two, mir_poyas FROM user_data WHERE user_id = ?", (id,))
               data = cursor.fetchone()
               markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
               markup.add("UA_kiev", "RU_moscow")
               markup.add("KZ_almaty")
               markup.add("Назад")
               
               await message.answer(f"На данный момент у вас стоит\n🕧Часовой пояс: {data[2]}\n\nЕсли у вас стоит Df(Default) то нажмите на вариант из трёх кнопок: \n 🇺🇦 UA_kiev(Киев),\n 🇷🇺 RU_moscow(Москва),\n 🇰🇿 KZ_almaty(Алматы)\nВы всегда сможете сменить часовой пояс", reply_markup=markup)
   elif message.text == "🧰Помощь":
      if message.chat.type == "private":
         await check_db(message)
         markup = types.InlineKeyboardMarkup(row_width=1)
         markup.add(types.InlineKeyboardButton("зачем нужен часовой пояс?", callback_data="mir_poyasq"))
         await message.answer("Тут собраны все команды и пояснения...\n\n/help - команда для пояснений\n/kvas_up - выпить кваса\n/top_in_group - топ литров этого чата \n/top - топ всех людей начиная с 100л.\n\n\n@FJHGGP спасибо за аву <3", reply_markup=markup)
   elif message.text == "📈Топ":
      if message.chat.type == "private":
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
         first_name_0 = message.from_user.first_name
         
         cursor.execute("SELECT first_name, kvas_up FROM user_data ORDER BY kvas_up DESC")
         data = cursor.fetchall()
         cursor.execute("SELECT first_name, kvas_up FROM user_data WHERE user_id = ?", (id,))
         data_user = cursor.fetchone()
         await check_db(message)
         output = ""
         one_numer = 0
         for record in data:
            first_name, kvas_up = record
            kvas_up_float = float(kvas_up)
            if float(kvas_up) > 99.99:
               one_numer += 1
               if first_name == first_name_0:
                  output += f"<u>{one_numer}. <b>{first_name}</b> - {round(kvas_up_float, 2)}л</u>\n"
               else:
                  output += f"{one_numer}. <b>{first_name}</b> - {round(kvas_up_float, 2)}л\n"
         await message.answer(f"Вот статистика всех людей у кого больше 100л.\n\n{output}", parse_mode="html")
         cursor.execute("SELECT first_name, kvas_up FROM user_data WHERE user_id = ?", (id,))
         data = cursor.fetchone()
         await message.answer(f"У вас: {data[1]}л.")
   elif message.text == "💬Отправить сообщение всем":
      if message.from_user.id == 1017848661:
         if message.chat.type == "private":
            global status
            status = "send"
            await message.answer("Отправьте любое сообщение которые хотите отправить всем")
   elif message.text.lower() == "бот":
      await check_db(message)
      await message.answer("✅ На месте")
   elif message.text == "⌨️ Админ панель":
      if message.from_user.id == 1017848661:
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
         
         markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
         
         markup.add("💬Отправить сообщение всем", "🗃️ Все данные пользователей", "📊 Опросы", "Назад")
         await message.answer("Админ панель", reply_markup=markup)
         cursor.execute("SELECT num_seven FROM user_data WHERE user_id = ?", (id,))
         cub = cursor.fetchone()
         cursor.execute("UPDATE user_data SET num_seven = ? WHERE user_id = ?", (1, id))
         conn.commit()
   elif message.text == "🗃️ Все данные пользователей":
      if message.from_user.id == 1017848661:
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
            
         cursor.execute("SELECT first_name, last_name, user_name, custom_name, user_id, active, mir_poyas, kvas_up, online_up FROM user_data")
         data = cursor.fetchall()
         output = ""
         for record in data:
            first_name, last_name, user_name, custom_name, user_id, active, mir_poyas, kvas_up, online_up = record
            output += f"Имя: <b>{first_name}</b>\nФамилия: <b>{last_name}</b>\nЮзер: <b>@{user_name}</b>\nПсевдоним: <b>{custom_name}</b>\nАйди: <b>{user_id}</b>\nАктив: <b>{active}</b>\nЧасовой пояс: <b>{mir_poyas}</b>\nВыпито кваса: <b>{kvas_up}</b>\nОнлайн: <b>{online_up}</b>ч.\n\n"
         await message.answer("Информация о всех пользователей:\n{}".format(output), parse_mode="html")
   elif message.text == "📊 Опросы":
      if message.from_user.id == 1017848661:
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         id = message.from_user.id
            
         cursor.execute("SELECT active, user_id, num_six FROM user_data")
         data = cursor.fetchall()
         cursor.execute("SELECT chat FROM chat_id WHERE id =  ?", (0,))
         data_chat = cursor.fetchone()
         await message.answer("{}".format(data[0]))
         print(data[0][1])
         chat_id = data[0][1]
         for user_data in data:
            try:
               active, user_id, num_six = user_data
               if active == 1:
                  await bot.send_poll(
                  chat_id = user_id,
                  question="Как настроение?",
                  options=["Не описать словами", "Супер", "Отлично", "Могло быть и хуже", "так себе", "ужасно"],
                  is_anonymous = False
                  )
               else:
                  await message.answer("Данный пользователь: {} не активный".format(user_id))
            except Exception as e:
               cursor.execute("UPDATE user_data SET active = ? WHERE user_id = ?", (0, user_id))
               conn.commit()
               await message.answer(f"Ошибка доставки сообщение пользователю: {user_id}\n\nОшибка: {e}")
         chat_ids = data_chat[0].split(", ")
         print(chat_ids)
         for chat in chat_ids:
             try:
                await message.answer(chat)
                await bot.send_poll(
                  chat_id = chat,
                  question="Как настроение?",
                  options=["Не описать словами", "Супер", "Отлично", "Могло быть и хуже", "Так себе", "Ужасно", "Хочу стереть этот жалкий мирок"],
                  is_anonymous = False
                  )
             except Exception as e:
                await message.answer(f"Такого чата нет либо пользователь удалил его оттуда\nОшибка: {e}")
   elif message.from_user.id == 1017848661:
         if status == "send":
            if message.chat.type == "private":
               global chaty
               conn = sqlite3.connect('testing2.db')
               cursor = conn.cursor()
               id = message.from_user.id
               msg = message.text
               
               cursor.execute("SELECT active, user_id, num_six FROM user_data")
               data = cursor.fetchall()
               cursor.execute("SELECT chat FROM chat_id WHERE id = ?", (0,))
               data_chat = cursor.fetchone()
               chat_id = data[0][2]
               status = "None"
               for user_data in data:
                  try:
                     active, user_id, num_six = user_data
                     if active == 1:
                        await bot.send_message(user_id, "{}".format(msg))
                     else:
                        await message.answer("Данный пользователь: {} не активный".format(user_id))
                  except Exception as e:
                     cursor.execute("UPDATE user_data SET active = ? WHERE user_id = ?", (0, user_id))
                     conn.commit()
                     await message.answer(f"Ошибка доставки сообщение пользователю: {user_id}\n\nОшибка: {e}")
                     
               chat_ids = data_chat[0].split(", ")
               for chat in chat_ids:
                  try:
                     await message.answer(chat)
                     await bot.send_message(chat, "{}".format(msg))
                  except Exception as e:
                     await message.answer(f"Такого чата нет либо пользователь удалил его оттуда\nОшибка: {e}")
   if message.text == "промо #новый_квас_на_час":
            await check_db(message)
            conn = sqlite3.connect('testing2.db')
            cursor = conn.cursor()
            id = message.from_user.id
               
            cursor.execute("SELECT num_tree, kvas_up FROM user_data WHERE user_id = ?", (id,))
            data = cursor.fetchone()
            if data[0] == 0:
               cursor.execute("UPDATE user_data SET num_tree = ?, kvas_up = kvas_up + ? WHERE user_id = ?", (1, 15.0, id))
               conn.commit()
               await message.answer("Вы успешно активировали промокод, вам было начислено <b>15.0л.</b>", parse_mode="html")
            else:
               await message.answer("К сожалению вы использовали промокод ранее")
   elif message.text == "📝Сообщить о ошибке":
       if message.chat.type == "private":
           await check_db(message)
           conn = sqlite3.connect('testing2.db')
           cursor = conn.cursor()
           id = message.from_user.id
               
           cursor.execute("SELECT num_seven, first_name, user_name, user_id FROM user_data WHERE user_id = ?", (id,))
           data = cursor.fetchone()
           await message.answer("Вы можете отправить сообщение, подробно опишите ошибку, после отправки,  сообщение перейдёт в модерацию, если ошибка была действительной то вам будет зачислен бонус за помощь, если по случайности вы нажали сюда то напишите 'отмена'")
           cursor.execute("UPDATE user_data SET num_seven = ? WHERE user_id = ?", (3, id))
           conn.commit()
   elif message.chat.type == "private":
        await check_db(message)
        conn = sqlite3.connect('testing2.db')
        cursor = conn.cursor()
        id = message.from_user.id
               
        cursor.execute("SELECT num_seven, first_name, user_name, user_id FROM user_data WHERE user_id = ?", (id,))
        data = cursor.fetchone()
        if data[0] == 3:
            if message.text.lower() == "отмена":
               cursor.execute("UPDATE user_data SET num_seven = ? WHERE user_id = ?", (0, id))
               conn.commit()
               markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
               markup.add('🍻Выпить кваса')
               markup.add('📈Топ', '🧰Помощь', '⚙️Настройки', '🎮Игры', "📝Сообщить о ошибке")
               if message.chat.id == 1017848661:
                  markup.add('⌨️ Админ панель')
               await message.answer("Добро пожаловать, скоро здесь появятся кнопки, soon...", reply_markup=markup)
            else:
               msg = message.text
               ua_new = datetime.now(UA_kiev_tz)
               format_ua = ua_new.strftime("%H:%M:%S")
               await bot.send_message(1017848661, f"Имя пользователя: {data[1]}\nЮзер пользователя: @{data[2]}\nАйди пользователя: {data[3]}\nINFO: {msg}\nTime: " + str(format_ua))
               cursor.execute("UPDATE user_data SET num_seven = ? WHERE user_id = ?", (0, id))
               conn.commit()
               await message.answer("Вы успешно сообщили о ошибке, ждите сообщение...")
   if message.text ==  "🎮Игры":
      if message.chat.type == "private":
         markup = types.InlineKeyboardMarkup(row_width=3)
         
         markup.add(types.InlineKeyboardButton("🥃3 стакана", callback_data="stakan"), types.InlineKeyboardButton("🪨✂️🧻", callback_data="kamnojby"))
         await message.answer("Вы нажали на кнопку '🎮Игры'\nИгры: 🥃3 стакана, 🪨✂️🧻", reply_markup=markup)
   elif message.chat.type == "private":
      conn = sqlite3.connect('testing2.db')
      cursor = conn.cursor()
      
      id = message.from_user.id
      msg = message.text
      cursor.execute("SELECT cabimet, kvas_up FROM user_data WHERE user_id = ?", (id,))
      data = cursor.fetchone()
      if data[0] == "stakan":
         if float(msg) < 1.00:
            await message.answer("К сожалению нельзя ставить ставку ниже 1-го литра")
         elif float(msg) >= float(data[1]):
            await message.answer("К сожалению у вас недостаточно литров")
         else:
            cursor.execute("UPDATE user_data SET stavka1 = ? WHERE user_id = ?", (float(msg), id))
            conn.commit()
            markup = types.InlineKeyboardMarkup(row_width=3)
            
            stk = types.InlineKeyboardButton("🥃", callback_data="vubor_stakan")
            
            markup.add(stk, stk, stk)
            print(f"{data[0]}")
            await message.answer("Выберите один из стаканов", reply_markup=markup)
            cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("None", id))
            conn.commit()
   elif message.text.lower() == "л":
      if message.chat.type in ["group", "supergroup"]:
         await check_db(message)
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         
         id = message.from_user.id
         msg = message.text
         cursor.execute("SELECT kvas_up FROM user_data WHERE user_id = ?", (id,))
         data = cursor.fetchone()
         await message.answer(f"{round(data[0], 2)}")
   elif message.text.lower() == "кто это":
      await check_db(message)
      if not message.reply_to_message:
         await message.reply("Это сообщение должно быть ответом на сообщение")
      else:
         conn = sqlite3.connect('testing2.db')
         cursor = conn.cursor()
         reply_id = message.reply_to_message.from_user.id
         cursor.execute("SELECT first_name, last_name, user_name, custom_name, user_id, kvas_up FROM user_data WHERE user_id = ?", (reply_id,))
         data_reply = cursor.fetchone()
         if reply_id == 1017848661:
            await message.reply("Имя: {}\nФамилия: {}\n🌐Юзер: {}\nПсевдоним: <b>DEV</b>\n🆔Айди: {}\n🍺Выпито литров: {}".format(data_reply[0], data_reply[1], data_reply[2], data_reply[4], round(data_reply[5], 2)), parse_mode="html")
         else:
            await message.reply("Имя: {}\nФамилия: {}\n🌐Юзер: {}\nПсевдоним: (скоро)\n🆔Айди: {}\n🍺Выпито литров: {}".format(data_reply[0], data_reply[1], data_reply[2], data_reply[4], round(data_reply[5], 2)))
   if message.chat.type == "private":
      conn = sqlite3.connect('testing2.db')
      cursor = conn.cursor()
      
      id = message.from_user.id
      cursor.execute("SELECT cabimet, kvas_up, stavka1 FROM user_data WHERE user_id = ?", (id,))
      data = cursor.fetchone()
      msg = message.text
      if data[0] == "kamnojbystavka":
         if float(msg) >= 1:
            if float(msg) <= float(data[1]):
               cursor.execute("UPDATE user_data SET stavka1 = ? WHERE user_id = ?", (msg, id))
               conn.commit()
               markup = types.InlineKeyboardMarkup()
               markup.add(types.InlineKeyboardButton("🪨", callback_data="stone"), types.InlineKeyboardButton("✂️", callback_data="nojnicu"), types.InlineKeyboardButton("🧻", callback_data="bymaga"))
               markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
               await message.answer("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: \n🤖Бот: ", reply_markup=markup)
               cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("kamnojbygame", id))
               conn.commit()
            else:
               await message.answer("К сожалению у вас недостаточно баланса")
         else:
            await message.answer("К сожалению нельзя ставить ставку ниже 1-го литра")

@dp.callback_query_handler(lambda call: True)
async def calling(call: types.CallbackQuery):
   if call.data == "mir_poyasq":
      if call.message.chat.type == "private" or "group" or "supergroup":
         markup = types.InlineKeyboardMarkup(row_width=1)
         markup.add(types.InlineKeyboardButton("←", callback_data="back"))
         await call.message.edit_text("<b>Зачем нужен часовой пояс?</b>\nЧасовой пояс нужен чтобы определить когда таймер закончится, если же часовой пояс будет с значением Df(Default) то время окончание таймера не будет совподать с вашим временем",parse_mode="html",  reply_markup=markup)
   elif call.data == "back":
      if call.message.chat.type == "private" or "group" or "supergroup":
         markup = types.InlineKeyboardMarkup(row_width=1)
         markup.add(types.InlineKeyboardButton("зачем нужен часовой пояс?", callback_data="mir_poyasq"))
         await call.message.edit_text("Тут собраны все команды и пояснения...\n\n/help - команда для пояснений\n/kvas_up - выпить кваса\n/top_in_group - топ литров этого чата \n/top - топ всех людей начиная с 100л.\n", reply_markup=markup)
   elif call.data == "stakan":
      conn = sqlite3.connect('testing2.db')
      cursor = conn.cursor()
      
      id = call.from_user.id
      cursor.execute("SELECT cabimet FROM user_data WHERE user_id = ?", (id,))
      data = cursor.fetchone()
      await call.message.answer("Прежде чем играть в стакан вы должны поставить ставку, ставка не должна быть меньше 1 литра")
      cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("stakan", id))
      conn.commit()
   elif call.data == "vubor_stakan":
      conn = sqlite3.connect('testing2.db')
      cursor = conn.cursor()
      
      id = call.from_user.id
      cursor.execute("SELECT cabimet, stavka1, kvas_up FROM user_data WHERE user_id = ?", (id,))
      data = cursor.fetchone()
      await call.message.delete()
      stkan = random.randint(1, 3)
      if stkan == 1:
         priz = random.randint(3, 5)
         v_priz = data[1] * priz
         cursor.execute("UPDATE user_data SET kvas_up = kvas_up + ? WHERE user_id = ?", (priz, id))
         conn.commit()
         markup = types.InlineKeyboardMarkup()
         markup.add(types.InlineKeyboardButton("Испытать свою удачу снова", callback_data="stakan"))
         await call.message.answer("✅Вы успешно умножили вашу ставку на {}х\n\nВы можете снова попробовать но советую быть осторожным".format(priz), reply_markup=markup)
         cursor.execute("UPDATE user_data SET stavka1 = ? WHERE user_id = ?", (0, id))
         conn.commit()
      elif stkan == 2:
         cursor.execute("UPDATE user_data SET stavka1 = ? WHERE user_id = ?", (0, id))
         conn.commit()
         await call.message.answer("0️⃣Вы остались в нуле\n\nВы можете снова попробовать но советую быть осторожным")
      else:
         priz = random.randint(1, 2)
         if int(priz) == 1:
            priz = 1.5
            v_priz = data[1] * 1.5
         else:
            v_priz = data[1] * priz
         cursor.execute("UPDATE user_data SET kvas_up = kvas_up - ? WHERE user_id = ?", (v_priz, id))
         conn.commit()
         await call.message.answer("❌К сожалению ваша ставка уменьшилась в {}х\n\nПредлагаю на этом остановится".format(priz))
         cursor.execute("UPDATE user_data SET stavka1 = ? WHERE user_id = ?", (0, id))
         conn.commit()
   elif call.data == "kamnojby":
      conn = sqlite3.connect('testing2.db')
      cursor = conn.cursor()
      
      id = call.from_user.id
      cursor.execute("SELECT game_online_kam FROM user_data")
      data = cursor.fetchall()
      
      markup = types.InlineKeyboardMarkup(row_width=1)
      markup.add(types.InlineKeyboardButton("PvB", callback_data="PvB"))
      
      online_game = 0
      for online in data:
         game_online_kam = online
         if game_online_kam == 1:
            online_game += 1
      
      await call.message.answer(f"Добро пожаловать в игру: <b>🪨Камень ✂️Ножницы 🧻Бумага</b>, надеюсь правила вы знаете\n\nПожалуйста выберите режим в котором будете играть\n<b>------------</b>\n1 режим 🤖PvB(player vs bot), в этом режиме вы будете играть с ботом\n<b>------------</b>\n\n‼️<b>вы всегда сможете отменить игру</b>, но учтите что <b>если во время игры вы захотите отказаться от игры то вы потеряете 1 литр</b>\n\nВыберайте и ставьте ставку!\n\n<b>Веселитесь!</b>\n\nИгроки ждущих игр: <b>{online_game}</b>", parse_mode="html", reply_markup=markup)
   elif call.data == "PvB":
      conn = sqlite3.connect('testing2.db')
      cursor = conn.cursor()
      
      id = call.from_user.id
      cursor.execute("SELECT cabimet, stavka1, kvas_up FROM user_data WHERE user_id = ?", (id,))
      data = cursor.fetchone()
      cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("kamnojbystavka", id))
      conn.commit()
      markup = types.InlineKeyboardMarkup()
      markup.add(types.InlineKeyboardButton("Отмена", callback_data="cancel"))
      await call.message.answer("Прежде чем играть поставьте ставку, ставка должна быть не ниже 1-го литра, учтите, вы можете в любой момент отказатся от игры но вам снимут 1 литр с вашего счёта", reply_markup=markup)
   elif call.data == "stone":
      conn = sqlite3.connect('testing2.db')
      cursor = conn.cursor()
      
      id = call.from_user.id
      cursor.execute("SELECT cabimet, stavka1, kvas_up FROM user_data WHERE user_id = ?", (id,))
      data = cursor.fetchone()
      kamnojby = random.choice(["🪨", "✂️", "🧻"])
      await call.message.edit_text("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: 🪨\n🤖Бот: ")
      
      if kamnojby == "🪨":
         await asyncio.sleep(1)
         await call.message.edit_text("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: 🪨\n🤖Бот: 🪨")
         await asyncio.sleep(1)
         
         markup = types.InlineKeyboardMarkup()
         
         markup.add(types.InlineKeyboardButton("Играть снова", callback_data="PvB"))
         
         await call.message.answer("Вам повезло, но в следущий раз вам может не повезти...", reply_markup=markup)
         
         cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("None", id))
         conn.commit()
      elif kamnojby == "✂️":
         await asyncio.sleep(1)
         await call.message.edit_text("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: 🪨\n🤖Бот: ✂️")
         await asyncio.sleep(1)
         
         markup = types.InlineKeyboardMarkup()
         
         markup.add(types.InlineKeyboardButton("Играть снова", callback_data="PvB"))
         
         await call.message.answer("Вам крупно повезло, но в следущий раз вам может не повезти...", reply_markup=markup)
         
         minus_stvka = data[1] * 2
         
         cursor.execute("UPDATE user_data SET kvas_up = kvas_up + ? WHERE user_id = ?", (minus_stvka, id))
         conn.commit()
         
         await call.message.answer("✅Вы успешно умножили вашу ставку на 2х\n\nВы можете снова попробовать но советую быть осторожным")
         
         cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("None", id))
         conn.commit()
      else:
         await asyncio.sleep(1)
         await call.message.edit_text("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: 🪨\n🤖Бот: 🧻️")
         await asyncio.sleep(1)
         
         markup = types.InlineKeyboardMarkup()
         
         markup.add(types.InlineKeyboardButton("Играть снова", callback_data="PvB"))
         
         await call.message.answer("Вам крупно повезло, но в следущий раз вам может не повезти...", reply_markup=markup)
         
         minus_stvka = data[1] * 2
         
         cursor.execute("UPDATE user_data SET kvas_up = kvas_up - ? WHERE user_id = ?", (minus_stvka, id))
         conn.commit()
         
         await call.message.answer("❌К сожалению ваша ставка уменьшилась в 2х\n\nПредлагаю на этом остановится")
         
         cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("None", id))
         conn.commit()

   elif call.data == "nojnicu":
      conn = sqlite3.connect('testing2.db')
      cursor = conn.cursor()
      
      id = call.from_user.id
      cursor.execute("SELECT cabimet, stavka1, kvas_up FROM user_data WHERE user_id = ?", (id,))
      data = cursor.fetchone()
      kamnojby = random.choice(["🪨", "✂️", "🧻"])
      await call.message.edit_text("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: ✂️\n🤖Бот: ")
      
      if kamnojby == "✂️":
         await asyncio.sleep(1)
         await call.message.edit_text("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: ✂️\n🤖Бот: ✂️")
         await asyncio.sleep(1)
         
         markup = types.InlineKeyboardMarkup()
         
         markup.add(types.InlineKeyboardButton("Играть снова", callback_data="PvB"))
         
         await call.message.answer("Вам повезло, но в следущий раз вам может не повезти...", reply_markup=markup)
         
         cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("None", id))
         conn.commit()
      elif kamnojby == "🪨":
         await asyncio.sleep(1)
         await call.message.edit_text("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: ✂️\n🤖Бот: 🪨")
         await asyncio.sleep(1)
         
         markup = types.InlineKeyboardMarkup()
         
         markup.add(types.InlineKeyboardButton("Играть снова", callback_data="PvB"))
         
         await call.message.answer("Вам крупно повезло, но в следущий раз вам может не повезти...", reply_markup=markup)
         
         minus_stvka = data[1] * 2
         
         cursor.execute("UPDATE user_data SET kvas_up = kvas_up - ? WHERE user_id = ?", (minus_stvka, id))
         conn.commit()
         await call.message.answer("❌К сожалению ваша ставка уменьшилась в 2х\n\nПредлагаю на этом остановится")
         
         cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("None", id))
         conn.commit()
      else:
         await asyncio.sleep(1)
         await call.message.edit_text("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: ✂️\n🤖Бот: 🧻️")
         await asyncio.sleep(1)
         
         markup = types.InlineKeyboardMarkup()
         
         markup.add(types.InlineKeyboardButton("Играть снова", callback_data="PvB"))
         
         await call.message.answer("Вам крупно повезло, но в следущий раз вам может не повезти...", reply_markup=markup)
         
         minus_stvka = data[1] * 2
         
         cursor.execute("UPDATE user_data SET kvas_up = kvas_up + ? WHERE user_id = ?", (minus_stvka, id))
         conn.commit()
         
         await call.message.answer("✅Вы успешно умножили вашу ставку на 2х\n\nВы можете снова попробовать но советую быть осторожным")
         
         cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("None", id))
         conn.commit()

   elif call.data == "bymaga":
      conn = sqlite3.connect('testing2.db')
      cursor = conn.cursor()
      
      id = call.from_user.id
      cursor.execute("SELECT cabimet, stavka1, kvas_up FROM user_data WHERE user_id = ?", (id,))
      data = cursor.fetchone()
      kamnojby = random.choice(["🪨", "✂️", "🧻"])
      await call.message.edit_text("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: 🧻\n🤖Бот: ")
      
      if kamnojby == "🧻":
         await asyncio.sleep(1)
         await call.message.edit_text("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: 🧻\n🤖Бот: 🧻️")
         await asyncio.sleep(1)
         
         markup = types.InlineKeyboardMarkup()
         
         markup.add(types.InlineKeyboardButton("Играть снова", callback_data="PvB"))
         
         await call.message.answer("Вам повезло, но в следущий раз вам может не повезти...", reply_markup=markup)
         
         cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("None", id))
         conn.commit()
      elif kamnojby == "🪨":
         await asyncio.sleep(1)
         await call.message.edit_text("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: 🧻\n🤖Бот: 🪨")
         await asyncio.sleep(1)
         
         markup = types.InlineKeyboardMarkup()
         
         markup.add(types.InlineKeyboardButton("Играть снова", callback_data="PvB"))
         
         await call.message.answer("Вам крупно повезло, но в следущий раз вам может не повезти...", reply_markup=markup)
         
         minus_stvka = data[1] * 2
         
         cursor.execute("UPDATE user_data SET kvas_up = kvas_up + ? WHERE user_id = ?", (minus_stvka, id))
         conn.commit()
         await call.message.answer("✅Вы успешно умножили вашу ставку на 2х\n\nВы можете снова попробовать но советую быть осторожным")
         
         cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("None", id))
         conn.commit()
      else:
         await asyncio.sleep(1)
         await call.message.edit_text("Нажмите вариант из трёх кнопок и ждите результата\n\n🧍Вы: 🧻\n🤖Бот: ✂️️")
         await asyncio.sleep(1)
         
         markup = types.InlineKeyboardMarkup()
         
         markup.add(types.InlineKeyboardButton("Играть снова", callback_data="PvB"))
         
         await call.message.answer("Вам крупно повезло, но в следущий раз вам может не повезти...", reply_markup=markup)
         
         minus_stvka = data[1] * 2
         
         cursor.execute("UPDATE user_data SET kvas_up = kvas_up - ? WHERE user_id = ?", (minus_stvka, id))
         conn.commit()
         
         await call.message.answer("❌К сожалению ваша ставка уменьшилась в 2х\n\nПредлагаю на этом остановится")
         
         cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("None", id))
         conn.commit()

   elif call.data == "cancel":
      conn = sqlite3.connect('testing2.db')
      cursor = conn.cursor()
      
      id = call.from_user.id
      cursor.execute("SELECT cabimet, stavka1, kvas_up FROM user_data WHERE user_id = ?", (id,))
      data = cursor.fetchone()
      
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      markup.add('🍻Выпить кваса')
      markup.add('📈Топ', '🧰Помощь', '⚙️Настройки', '🎮Игры', "📝Сообщить о ошибке")
      if call.message.chat.id == 1017848661:
         markup.add('⌨️ Админ панель')
      await call.message.answer("Добро пожаловать, скоро здесь появятся кнопки, soon...", reply_markup=markup)
      
      if data[0] == "kamnojbygame":
         cursor.execute("UPDATE user_data SET kvas_up = kvas_up - ? WHERE user_id = ?", (1, id))
         conn.commit()
         await call.message.answer("Вы отменили игру, за это вам было снято 1 литр, постарайтесь больше не отменять игры пожалуйста")
      
      cursor.execute("UPDATE user_data SET cabimet = ? WHERE user_id = ?", ("None", id))
      conn.commit()

#keep_alive_live()
executor.start_polling(dp)
