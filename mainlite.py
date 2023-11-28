# -*- coding: utf-8 -*-
import yaml
from telegram import *
from telegram.ext import *
import telegram
from yaml import *
import time as t

# IMPORTS OTHER FILES
from Lfunctions import *
from MySQL_Driver import *
from functions import *

# LOGGER SETTINGS
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("Lite_Extension")

with open('config.yaml', 'r') as file:
    token = yaml.safe_load(file)
    token = token['TOKEN']


async def start_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.full_name
    chat = update.effective_chat
    if chat.type != Chat.PRIVATE:
        return

    await update.effective_message.reply_text(
        f'Привіт {user_name}. Я Lite версія боту під назвою "Поклич мене", як ти розумієш з назви я допомагаю кликати в чат '
        f'користувачів.\n'
        f'/info щоб дізнатись додаткову інформацію\n'
        f'Вся детальна інформація по командам і чим відрізняється Lite версія від звичайної можна прочитати в моїй Wiki ⬇️',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Wiki', url='?*?????')]
        ]))


async def All(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.effective_message.reply_text("Ця команда може використовуватись тільки в чаті.")
        return
    CID = update.effective_chat.id
    info = LParseAllUsers(CID)
    if len(info) == 0:
        await update.effective_message.reply_text(
            "На жаль, список на пінг пустий. Для детальнішої інформації прочитайте Wiki - /info")
    PINGLIST = []
    PRINTLIST = []
    MV = 0
    GMV = 0
    for x in info:
        if x[2].startswith("!"):
            id = x[2].replace("!", "")
            PINGLIST.extend([f"[{update.effective_user.first_name}](tg://user?id={[id]})"])
            break
        else:
            PINGLIST.extend([f"@{x[2]}"])
    for x in range(len(PINGLIST)):
        print(f"MV: {MV}")
        if len(PINGLIST) == 0:
            print("PINGNULL")
            break
        PRINTLIST.extend([f"{PINGLIST[MV]}"])
        MV = MV + 1
        GMV = GMV + 1
        if (MV % 4) == 0:
            print("SENDMSG MV%")
            await update.effective_chat.send_message(' '.join(PRINTLIST))
            PRINTLIST.clear()
        elif (MV % 4) > 0:
            print("MV%>0")
            if (len(PINGLIST) - MV) <= 4:
                print("<4")
                for x in range(len(PINGLIST) - MV):
                    PRINTLIST.extend([f"{PINGLIST[MV]}"])
                    MV = MV + 1
                await update.effective_chat.send_message(' '.join(PRINTLIST))
                break

        print(f"{MV % 4} |||")
        t.sleep(0.2)

    print(PINGLIST)


async def Updater(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(update.effective_message.new_chat_members) != 0:
        for member in update.effective_message.new_chat_members:
            print(f"MEMBERU: {member.username} CBG: {context.bot.username}")
            if member.username == context.bot.username:
                await update.effective_chat.send_message(
                    'Всім привіт, тепер я буду кликати вас!\n'
                    'Я почну кликати користувача як тільки він напише хоч одне повідомлення!\n'
                    '*Вся інформація по використанню команд та моєму налаштуванню є в Wiki*',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text='Wiki',
                                              url='https://github.com/cheuS1-n/CallMeBotUA/wiki/%D0'
                                                  '%94%D0%BE%D0%BC%D1%96%D0%B2%D0%BA%D0%B0')],
                    ]), parse_mode=telegram.constants.ParseMode.MARKDOWN)
    UNick = update.effective_user.username
    UID = update.effective_user.id
    CID = update.effective_chat.id
    info = LParseUserInfoC(UID, CID)
    print(UID)
    print(CID)
    print(info)
    if update.effective_user.username is None:
        print("NONE")
        if str(info[0][1]).startswith("!"):
            if str(info[0][1]) == str(f"!{update.effective_user.id}"):
                print("Update not need, nicks are indentical | Alternative method")
                return
            else:
                if ChangeNick(update.effective_user.id, f"!{update.effective_chat.id}"):
                    print("NICK CHANGED! But user dont have nick, used alternative method.")
                    return
                else:
                    logger.error("NICKS DONT CHANGED, CHANGE ERROR! | Alternative method.")
                    return
    if len(info) == 0:
        print("LEN 0")
        LAddNewProfile(CID, UID, UNick)
    if str(info[0][2]) == str(UNick):
        print("Update not need, nicks are indentical")
        return


    if ChangeNick(UID, UNick):
        print("NICK CHANGED")
    else:
        print("Nick Dont changed")


def STARTL():
    while True:
        Lapplication = ApplicationBuilder().token(token).build()
        Lapplication.add_handler(CommandHandler('start', start_private_chat))
        Lapplication.add_handler(CommandHandler('all', All))
        Lapplication.add_handler(MessageHandler(filters.ALL, Updater))
        Lapplication.run_polling()

if startdbs():
    STARTL()
else:
    logger_mysql.error("Connection failed. Can`t start the bot.")
