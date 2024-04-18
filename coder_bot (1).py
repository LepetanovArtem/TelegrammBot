from aiogram import types
from aiogram.utils import executor
#from gollands_test import *
#from lenguage_jokes import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random

db = sqlite3.connect("database/coderbot.db")
sql = db.cursor()

bot = Bot(token='6065623460:AAFcAI9C0hVIScm9YCn3QJFx0nmL61QNWC0')
dp = Dispatcher(bot)

def start_table_generating():
    sql.execute("""CREATE TABLE IF NOT EXISTS users (user_id TEXT, dialog INTEGER, coding INTEGER, key TEXT, keylist TEXT, passname TEXT)""")
    db.commit()

start_table_generating()

btnRemakeTest = KeyboardButton("Библиотека ключей")
btnVievTestResult = KeyboardButton("Закодировать сообщение")
btnVievTestResult2 = KeyboardButton("Раскодировать сообщение")
testRemakeMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnRemakeTest, btnVievTestResult, btnVievTestResult2)

lib_men1 = KeyboardButton("Создать новый ключ")
lib_men2 = KeyboardButton("Добавить ключ вручную")
lib_men3 = KeyboardButton("На главную")
lib_men = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(lib_men1, lib_men2, lib_men3)

gen_key_but = KeyboardButton("Создать ключ")
gen_key_men = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(gen_key_but)

def coding(alpha, ids, n):
    sql.execute("SELECT passname FROM users WHERE user_id = ?", [ids])
    data = sql.fetchone()[0]
    res = ''
    for c in data:
        res += alpha[(alpha.index(c) + n) % len(alpha)]
    return res

def creating_key():
    alph = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnmёйцукенгшщзхъфывапролджэячсмитьбю1234567890ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ!"№#;$^:?&*()[]{}/.,`~'
    a = "".join(random.sample(list(alph), len(alph)))
    return a

def list_rewrite(ids):
    sql.execute("SELECT keylist FROM users WHERE user_id = ?", [ids])
    data = sql.fetchone()[0]
    data = data.split("devide")
    str_gen = 'Ваши ключи: \n\n'
    for i in range(len(data)-1):
        str_gen += str(data[i+1][:150]) + ' - ' + str(data[i+1][150:]) + '\n' + '\n'
    return str_gen

def choose_list(ids, txt):
    sql.execute("SELECT keylist FROM users WHERE user_id = ?", [ids])
    data = sql.fetchone()[0]
    data = data.split("devide")
    str_gen = []
    for i in range(len(data)-1):
        str_gen.append(str(data[i+1][150:]))
    if txt in str_gen:
        strings = []
        for i in range(len(data) - 1):
           strings.append(str(data[i + 1][:150]) + ' - ' + str(data[i + 1][150:]) + '\n')
        for i in range(len(strings)):
            if txt in strings[i]:
                return str(strings[i][:150])
    else:
        return 0

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    sql.execute("SELECT user_id FROM users")
    if sql.fetchone() is None:
        sql.execute("INSERT INTO users(user_id, dialog, key, keylist, passname) VALUES(?, ?, ?, ?, ?)", [str(message.from_user.id), 1, '', '', ''])
        db.commit()
    else:
        sql.execute("DELETE FROM users WHERE user_id = ?", [str(message.from_user.id)])
        sql.execute("INSERT INTO users(user_id, dialog, key, keylist, passname) VALUES(?, ?, ?, ?, ?)", [str(message.from_user.id), 1, '', '', ''])
        db.commit()
    await message.reply("Привет, я Шифровальщик. \nЯ помогу тебе кодировать твои сообщения. опираясь на шифр Цезаря, но с разными ключами. Давай создадим тебе ключ для шифровки", reply_markup=gen_key_men)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Я помогу тебе кодировать и декодировать твои сообщения")

@dp.message_handler()
async def echo_message(msg: types.Message):
    try:
        db = sqlite3.connect("database/coderbot.db")
        sql = db.cursor()
        sql.execute("SELECT dialog FROM users WHERE user_id = ?", [str(msg.from_user.id)])
        dialog = sql.fetchone()[0]
        if dialog == 1:
            if msg.text == "Библиотека ключей":
                    sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [7, str(msg.from_user.id)])
                    db.commit()
                    await msg.answer(list_rewrite(msg.from_user.id), reply_markup=lib_men)
            if msg.text == "Создать ключ":
                sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [2, str(msg.from_user.id)])
                db.commit()
                await msg.answer("Придумайте название ключа, чтобы его не потерять. Лучше сделай его не слишком длинным")
            if msg.text == "Закодировать сообщение":
                sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [3, str(msg.from_user.id)])
                db.commit()
                await msg.answer("Введите текст")
            if msg.text == "Раскодировать сообщение":
                sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [5, str(msg.from_user.id)])
                db.commit()
                await msg.answer("Введите текст")
        elif dialog == 2:
            sql.execute("SELECT keylist FROM users WHERE user_id = ?", [str(msg.from_user.id)])
            kl = str(sql.fetchone()[0])
            gencey = str(creating_key())
            print(kl)
            sql.execute("UPDATE users SET keylist = ? WHERE user_id = ?", [kl+'devide'+gencey+str(msg.text), str(msg.from_user.id)])
            sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [7, str(msg.from_user.id)])
            db.commit()
            await msg.answer(list_rewrite(str(msg.from_user.id)), reply_markup=lib_men)
        elif dialog == 3:
            sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [4, str(msg.from_user.id)])
            sql.execute("UPDATE users SET passname = ? WHERE user_id = ?", [str(msg.text), str(msg.from_user.id)])
            db.commit()
            await msg.answer("Введите введите название ключа из библиотки")
        elif dialog == 4:
            if choose_list(msg.from_user.id, msg.text) != 0:
                await msg.answer(str(coding(choose_list(msg.from_user.id, msg.text), msg.from_user.id, 3)), reply_markup=testRemakeMenu)
                sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [1, str(msg.from_user.id)])
                db.commit()
            else:
                await msg.answer("Такого ключа нет в библиотеке")
                sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [7, str(msg.from_user.id)])
                db.commit()
                await msg.answer(list_rewrite(msg.from_user.id), reply_markup=lib_men)
        elif dialog == 5:
            sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [6, str(msg.from_user.id)])
            sql.execute("UPDATE users SET passname = ? WHERE user_id = ?", [str(msg.text), str(msg.from_user.id)])
            db.commit()
            await msg.answer("Введите введите название ключа из библиотки")
        elif dialog == 6:
            if choose_list(msg.from_user.id, msg.text) != 0:
                await msg.answer(str(coding(choose_list(msg.from_user.id, msg.text), msg.from_user.id, 147)), reply_markup=testRemakeMenu)
                sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [1, str(msg.from_user.id)])
                db.commit()
            else:
                await msg.answer("Такого ключа нет в библиотеке")
                sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [7, str(msg.from_user.id)])
                db.commit()
                await msg.answer(list_rewrite(msg.from_user.id), reply_markup=lib_men)
        elif dialog == 7:
            if msg.text == "Создать новый ключ":
                sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [2, str(msg.from_user.id)])
                db.commit()
                await msg.answer("Придумайте название ключа, чтобы него не потерять. Лучше сделай его не слишком длинным")
            elif msg.text == "На главную":
                sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [1, str(msg.from_user.id)])
                db.commit()
                await msg.answer("Вы перемещены на главную", reply_markup=testRemakeMenu)
            elif msg.text == "Добавить ключ вручную":
                sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [8, str(msg.from_user.id)])
                db.commit()
                await msg.answer("Введите новый ключ")
        elif dialog == 8:
            nkl = str(msg.text)
            if len(nkl) == 150:
                sql.execute("UPDATE users SET key = ? WHERE user_id = ?", [msg.text, str(msg.from_user.id)])
                sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [9, str(msg.from_user.id)])
                await msg.answer("Введите название нового ключа")
            else:
                await msg.answer("Введите корректный ключ (суммарно должен включать в себя 150 символов)")
            db.commit()
        elif dialog == 9:
            sql.execute("SELECT keylist FROM users WHERE user_id = ?", [str(msg.from_user.id)])
            data = sql.fetchone()[0]
            sql.execute("SELECT key FROM users WHERE user_id = ?", [str(msg.from_user.id)])
            key_for = sql.fetchone()[0]
            print(data)
            print(key_for)
            sql.execute("UPDATE users SET keylist = ? WHERE user_id = ?", [data+'devide'+key_for+str(msg.text), msg.from_user.id])
            sql.execute("UPDATE users SET dialog = ? WHERE user_id = ?", [7, str(msg.from_user.id)])
            db.commit()
            await msg.answer(list_rewrite(msg.from_user.id), reply_markup=lib_men)
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        sql.close()
        db.close()


if __name__ == '__main__':
    executor.start_polling(dp)