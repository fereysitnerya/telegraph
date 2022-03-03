#!/usr/bin/python3
# region data const
import ast
import asyncio
import configparser
import logging
import os
import random
import sqlite3
import time
from contextlib import suppress
from aiogram import Bot, types
from aiogram import Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ParseMode
from aiogram.utils import exceptions
from aiogram.utils.exceptions import MessageNotModified
from telegraph import Telegraph

DEFAULT_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'db.db'))
DEFAULT_INI = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), 'config.ini')))
DEFAULT_MEDIA = os.path.abspath(os.path.join(os.path.dirname(__file__), 'MEDIA'))
LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '_l.txt'))
SECTION = 'CONFIG'
logging.basicConfig(level=logging.INFO)
config_parser = configparser.ConfigParser()
one_hour = 3600

class TelegraphToken(StatesGroup):
    tgphToken = State()

# endregion

# region data variable
API_TOKEN = '5092755664:AAHlNQH-b6xVyQSsCAXJNWMiebuunupH96w'
storage = MemoryStorage()
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
markupMain = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="прôмокôд 3127", row_width=2)
buttons = [
    KeyboardButton('🧊 Услўги'),     # 🗿 🥏 🧊👩‍🎓👩🏼‍💻👩🏼‍💼🙅🏼‍♀️🧏🏼‍♀️🤷🏻‍♂️🤷🏼‍♂️🙍🏼‍♀️🕸🦈🍃🪨🌚🌑🌘🌍🌏🔥🪐🌪💨🌬💫⭐️⚡️✨🌟💥☀️🌊🌫🫐🪁🗻🏔⛰🌠🌌🖲💎💠🌀🔆🔅❕❔🗯💭🀄️🇪🇺👀👩‍🎓👓🐋☘️🍀🍃🌱🌿🎋❄️💧
    KeyboardButton('📘 Материáлы'),  # 🌌 🪁 🫐 🕸  🖲 💠 🇪🇺
    KeyboardButton('⭐ Мой блôг'),
    KeyboardButton('🦋 О наč')
]
markupMain.add(*buttons)
bot_name = 'FerreyChatBot'
channel_name = 'https://t.me/ferey_channel'
chat_name = 'https://t.me/ferey_channel'
name_surname = 'Ferey'
username = 'ferey_official'
short_name = 'me'
author_name = username
author_url = 'https://t.me/ferey_official'


def createConfig():
    touch(DEFAULT_INI)
    config_parser.read(DEFAULT_INI)
    config_parser['CONFIG'] = {}
    writeConfigList('admin_id', ['418853095'])

    with open(DEFAULT_INI, 'w') as configfile:
        config_parser.write(configfile)

# endregion

# region db
def dbCREATE():
    con = sqlite3.connect(DEFAULT_BASE, timeout=10)
    con.execute('PRAGMA foreign_keys=ON;')
    cur = con.cursor()

    # USER
    cur.execute('''CREATE TABLE IF NOT EXISTS USER ( 
        USER_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                    UNIQUE
                                    NOT NULL,
        USER_TID        INTEGER     UNIQUE
                                    NOT NULL,
        USER_DATE       DATETIME,
        USER_USERNAME   VARCHAR,
        USER_ERROR      VARCHAR
    );''')

    # TGPH
    cur.execute('''CREATE TABLE IF NOT EXISTS TGPH (
        TGPH_ID             INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
        TGPH_SHORT_NAME     VARCHAR     NOT NULL,
        TGPH_AUTH_NAME      VARCHAR,
        TGPH_AUTH_URL       VARCHAR,
        TGPH_TOKEN          VARCHAR     UNIQUE,
        TGPH_EDIT_URL       VARCHAR,
        TGPH_PATH           VARCHAR,
        TGPH_VIEWS          VARCHAR,
        TGPH_ACTIVE         BOOLEAN,
        UNIQUE (TGPH_SHORT_NAME, TGPH_AUTH_NAME, TGPH_AUTH_URL, TGPH_TOKEN, TGPH_EDIT_URL, TGPH_ACTIVE)  
    );''')

    con.commit()
    cur.close()
    con.close()
    log("db ok")


def dbSELECT(sql, param=None):
    data = []
    try:
        con = sqlite3.connect(DEFAULT_BASE, timeout=10)
        con.execute('PRAGMA foreign_keys=ON;')
        cur = con.cursor()
        if param:
            cur.execute(sql, param)
        else:
            cur.execute(sql)
        data = cur.fetchall()

        cur.close()
        con.close()
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))
    finally:
        return data


def dbCHANGE(sql, param=None):
    result = '-1'
    try:
        con = sqlite3.connect(DEFAULT_BASE, timeout=10)
        con.execute('PRAGMA foreign_keys=ON;')
        cur = con.cursor()

        if param:
            cur.execute(sql, param)
        else:
            cur.execute(sql)
        con.commit()

        cur.close()
        con.close()
        result = str(cur.lastrowid)
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


# endregion

# region menu
@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    try:
        await bot.send_message(chat_id=message.chat.id, text="С ♥️, Ferey", reply_markup=markupMain)
        await asyncio.sleep(0.5)
        log('start ok')
    except exceptions.RetryAfter as e:
        log(f'RetryAfter {e.timeout}')
        await asyncio.sleep(e.timeout)
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))
        sql = "UPDATE USER SET USER_ERROR = ? WHERE USER_TID = ?;"
        usr_id = dbCHANGE(sql, (str(e), message.chat.id))

@dp.message_handler(lambda message: message.text in ['↩️ Меню', '🔙️ Меню'], state='*')
async def menu(message: types.Message, state: FSMContext):
    try:
        await state.finish()
        await asyncio.sleep(0.1)
        if message.chat.type != 'private': return

        await bot.send_message(chat_id=message.chat.id, text='menu', reply_markup=markupMain)
    except exceptions.RetryAfter as e:
        log(f'RetryAfter {e.timeout}')
        await asyncio.sleep(e.timeout)
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))
        sql = "UPDATE USER SET USER_ERROR = ? WHERE USER_TID = ?;"
        usr_id = dbCHANGE(sql, (str(e), message.chat.id))


# endregion

# region blog
async def showTgphPosts(chat_id):
    try:
        sql = "SELECT TGPH_TOKEN FROM TGPH"
        tokens = dbSELECT(sql, ())
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for token in tokens:
            telegraph = Telegraph(access_token=token[0])
            pages = telegraph.get_page_list()

            for item in pages['pages']:
                try:
                    page = telegraph.get_page(path=item['path'], return_content=True, return_html=True)
                    keyboard.add(types.InlineKeyboardButton(text=page['title'], url=page["url"]))
                except Exception as e:
                    log(e, 95)
                    time.sleep(round(random.uniform(1, 2), 2))
        await bot.send_message(chat_id=chat_id, text="⭐ Мои публикации", reply_markup=keyboard)
    except exceptions.RetryAfter as e:
        log(f'RetryAfter {e.timeout}')
        await asyncio.sleep(e.timeout)
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))
        sql = "UPDATE USER SET USER_ERROR = ? WHERE USER_TID = ?;"
        usr_id = dbCHANGE(sql, (str(e), chat_id,))

async def showLastPostIV(chat_id):
    active_id = active_token = None
    try:
        sql = "SELECT TGPH_ID,TGPH_TOKEN FROM TGPH WHERE TGPH_ACTIVE=?"
        data = dbSELECT(sql, (1,))
        if not data: return None
        telegraph = Telegraph(access_token=data[0][1])
        pages = telegraph.get_page_list()
        text = f"<a href='{pages['pages'][0]['url']}'>@{username}</a>"
        await bot.send_message(chat_id=chat_id, text=text)
        active_id, active_token = data[0][0], data[0][1]
    except exceptions.RetryAfter as e:
        log(f'RetryAfter {e.timeout}')
        await asyncio.sleep(e.timeout)
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))
        sql = "UPDATE USER SET USER_ERROR = ? WHERE USER_TID = ?;"
        usr_id = dbCHANGE(sql, (str(e), chat_id,))
    finally:
        return active_id, active_token

async def showAdminPanel(chat_id, active_id, active_token):
    try:
        telegraph = Telegraph(access_token=active_token)
        pages = telegraph.get_page_list()
        if str(chat_id) in readConfigList('admin_id'):
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [
                types.InlineKeyboardButton(text=f"Создать публикацию", url=telegraph.get_account_info(fields=["auth_url"])["auth_url"]),
                types.InlineKeyboardButton(text=f"Добавить аккаунт", callback_data="tghp_addToken"),
                types.InlineKeyboardButton(text=f"Переключить аккаунт [{active_id}]", callback_data="tghp_exchangeToken")
            ]
            keyboard.add(*buttons)
            await bot.send_message(chat_id=chat_id, text="🗝️ Вы зашли как администратор - вы можете создавать и редактировать блоги (*но не удалять их)",reply_markup=keyboard)


            text = "1 - Сначала нажмите на кнопку \n«🌱 Авторизация» (у нее короткое время жизни)\n2 - Затем нажмите на нужную ссылку (она скопируется), чтобы открыть ее в браузере для редактирования: \n\n"
            cnt = 1
            for item in pages['pages']:
                page = telegraph.get_page(path=item['path'], return_content=True, return_html=True)
                text += f"{cnt}. " + "<code>" + str(page['url']) + "</code>" + "\n"
                cnt += 1

            keyboard = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text="1. 🌱 Авторизация", url=telegraph.get_account_info(fields=["auth_url"])["auth_url"]))
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, disable_web_page_preview=True)
    except exceptions.RetryAfter as e:
        log(f'RetryAfter {e.timeout}')
        await asyncio.sleep(e.timeout)
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))
        sql = "UPDATE USER SET USER_ERROR = ? WHERE USER_TID = ?;"
        usr_id = dbCHANGE(sql, (str(e), chat_id,))

def trigger():
    try:
        sql = "SELECT TGPH_TOKEN, TGPH_ACTIVE  FROM TGPH"
        data = dbSELECT(sql, ())
        if not data or len(data) == 1: return None

        tmp_token = data[0][0]
        for i in range(0, len(data)):
            if data[i][1] == 1:
                tmp_token = data[(i + 1) % len(data)][0]
                sql = "UPDATE TGPH SET TGPH_ACTIVE=? WHERE TGPH_TOKEN=?"
                dbCHANGE(sql, (0, data[i][0],))
                break

        sql = "UPDATE TGPH SET TGPH_ACTIVE=? WHERE TGPH_TOKEN=?"
        dbCHANGE(sql, (1, tmp_token,))
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))

def isTGPH_TOKEN():
    try:
        sql = "SELECT TGPH_TOKEN FROM TGPH"
        data = dbSELECT(sql, ())
        if not data: return None

        if len(data) == 1:
            sql = "UPDATE TGPH SET TGPH_ACTIVE=?"
            dbCHANGE(sql, (1,))

        sql = "SELECT TGPH_TOKEN FROM TGPH WHERE TGPH_ACTIVE=?"
        data = dbSELECT(sql, (1,))
        if not data: return None
        return data[0][0]
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))

def createTelegraphInstance():
    telegraph = None
    try:
        TGPH_TOKEN = isTGPH_TOKEN()

        if TGPH_TOKEN == None:
            telegraph = Telegraph()
            account = telegraph.create_account(short_name=short_name, author_name=author_name, author_url=author_url)

            sql = "INSERT OR IGNORE INTO TGPH (TGPH_SHORT_NAME, TGPH_AUTH_NAME, TGPH_AUTH_URL, TGPH_TOKEN, TGPH_EDIT_URL, TGPH_ACTIVE) VALUES (?, ?, ?, ?, ?, ?);"
            dbCHANGE(sql, (account['short_name'], account['author_name'], account['author_url'], account['access_token'], account['auth_url'], 1,))
        else:
            telegraph = Telegraph(access_token=TGPH_TOKEN)
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))
    finally:
        return telegraph

@dp.message_handler(lambda message: '⭐ Мой блôг' in message.text)
async def blog(message: types.Message):
    try:
        # create instance
        telegraph = createTelegraphInstance()
        if telegraph.get_page_list()['total_count'] == 0:
            telegraph.create_page(title='first-page', html_content='This is my story', author_name=author_name, author_url=author_url, return_content=True)

        # show all posts
        await showTgphPosts(message.chat.id)

        # show last blog Instant View
        active_id, active_token = await showLastPostIV(message.chat.id)

        # admin
        await showAdminPanel(message.chat.id, active_id, active_token)
    except exceptions.RetryAfter as e:
        log(f'RetryAfter {e.timeout}')
        await asyncio.sleep(e.timeout)
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))
        sql = "UPDATE USER SET USER_ERROR = ? WHERE USER_TID = ?;"
        usr_id = dbCHANGE(sql, (str(e), message.chat.id))

@dp.callback_query_handler(text="tghp_exchangeToken", state='*')
async def tghp_exchangeToken(call: types.CallbackQuery, state: FSMContext):
    try:
        with suppress(MessageNotModified):
            trigger()
            # show last blog Instant View
            active_id, active_token = await showLastPostIV(call.message.chat.id)

            # admin
            await showAdminPanel(call.message.chat.id, active_id, active_token)
        await call.answer()
    except exceptions.RetryAfter as e:
        log(f'RetryAfter {e.timeout}')
        await asyncio.sleep(e.timeout)
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))
        sql = "UPDATE USER SET USER_ERROR = ? WHERE USER_TID = ?;"
        usr_id = dbCHANGE(sql, (str(e), call.message.chat.id))

@dp.callback_query_handler(text="tghp_addToken", state='*')
async def tghp_addToken(call: types.CallbackQuery, state: FSMContext):
    try:
        with suppress(MessageNotModified):
            await state.finish()
            await bot.send_message(chat_id=call.message.chat.id, text="Вставьте значение токена длиной в 60 символов")
            await TelegraphToken.tgphToken.set()
        await call.answer()
    except exceptions.RetryAfter as e:
        log(f'RetryAfter {e.timeout}')
        await asyncio.sleep(e.timeout)
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))
        sql = "UPDATE USER SET USER_ERROR = ? WHERE USER_TID = ?;"
        usr_id = dbCHANGE(sql, (str(e), call.message.chat.id))

@dp.message_handler(lambda message: message.text, state=TelegraphToken.tgphToken)
async def tgphToken(message: types.Message, state: FSMContext):
    try:
        if len(message.text) != 60:
            await bot.send_message(chat_id=message.chat.id, text="Вставьте значение токена длиной в 60 символов")
            return

        telegraph = Telegraph(access_token=message.text)
        account = telegraph.get_account_info(fields=["short_name", "author_name", "author_url", "auth_url"])
        sql = "INSERT OR IGNORE INTO TGPH (TGPH_SHORT_NAME, TGPH_AUTH_NAME, TGPH_AUTH_URL, TGPH_TOKEN, TGPH_EDIT_URL, TGPH_ACTIVE) VALUES (?, ?, ?, ?, ?, ?);"
        dbCHANGE(sql, (account['short_name'], account['author_name'], account['author_url'], message.text, account['auth_url'],0,))
        sql = 'UPDATE TGPH SET TGPH_SHORT_NAME = ?, TGPH_AUTH_NAME = ?, TGPH_AUTH_URL = ?, TGPH_EDIT_URL = ? WHERE TGPH_TOKEN = ?;'
        dbCHANGE(sql, (account['short_name'], account['author_name'], account['author_url'], account['auth_url'], message.text))

        trigger()
        await bot.send_message(chat_id=message.chat.id, text="Аккаунт добавлен и переключен! Нажмите снова на кнопку ⭐ Мой блог, чтобы увидеть статьи со всех аккаунтов")
        await state.finish()
    except exceptions.RetryAfter as e:
        log(f'RetryAfter {e.timeout}')
        await asyncio.sleep(e.timeout)
    except Exception as e:
        log(e, 95)
        time.sleep(round(random.uniform(1, 2), 2))
        sql = "UPDATE USER SET USER_ERROR = ? WHERE USER_TID = ?;"
        usr_id = dbCHANGE(sql, (str(e), message.chat.id))

# endregion

# region function

def log(txt, colour=92):
    logging.info(f'\033[{colour}m%s\033[0m' % (str(txt)))

def writeConfigList(key, val):
    config_parser.read(DEFAULT_INI)
    config_parser.set(SECTION, key, str(val))

    with open(DEFAULT_INI, 'w') as configfile:
        config_parser.write(configfile)

def readConfigList(key):
    my_list = ast.literal_eval(config_parser.get(SECTION, key))
    return my_list

def touch(path):
    if not os.path.exists(path):
        with open(path, 'a'):
            os.utime(path, None)

def init():
    os.makedirs(DEFAULT_MEDIA, exist_ok=True, mode=0o777)
    dbCREATE()
    createConfig()
    executor.start_polling(dp)


# endregion

def main():
    init()

main()
