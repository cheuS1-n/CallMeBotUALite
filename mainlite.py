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
loggerm = logging.getLogger("Lite_Extension")

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
    APINGLIST = []
    MV = 0
    for x in info:
        if x[2].startswith("!"):
            print("+++")
            id = x[1]
            nick = x[2].replace("!", "")
            APINGLIST.extend([f"[{nick}](tg://user?id={id})"])
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
        if (MV % 4) == 0:
            print("SENDMSG MV%")
            await update.effective_chat.send_message(' '.join(PRINTLIST))
            PRINTLIST.clear()
        elif (MV % 4) > 0:
            print("MV%>0")
            print(f"MV: {MV} | PL: {len(PINGLIST)}")
            if (len(PINGLIST) - MV) <= 2:
                print("<2")
                for x in range(len(PINGLIST) - MV):
                    PRINTLIST.extend([f"{PINGLIST[MV]}"])
                    MV = MV + 1
                await update.effective_chat.send_message(' '.join(PRINTLIST))
                break
        print(f"{MV % 4} |||")
    PINGLIST.clear()
    PRINTLIST.clear()
    MV = 0
    print(f"LENA: {len(APINGLIST)} | {APINGLIST}")
    if not len(APINGLIST) == 0:
        print(f"APL: {APINGLIST}")
        for x in APINGLIST:
            PRINTLIST.extend([f"{APINGLIST[MV]}"])
            MV = MV + 1
            if (MV % 4) == 0:
                print("ASENDMSG MV%")
                await update.effective_chat.send_message(' '.join(PRINTLIST),
                                                         parse_mode=telegram.constants.ParseMode.MARKDOWN)
                PRINTLIST.clear()
            elif (MV % 4) > 0:
                print("AMV%>0")
                if (len(PINGLIST) - MV) <= 4:
                    print("<4A")
                    for x in range(len(PINGLIST) - MV):
                        PRINTLIST.extend([f"{PINGLIST[MV]}"])
                        MV = MV + 1
                    await update.effective_chat.send_message(' '.join(PRINTLIST),
                                                             parse_mode=telegram.constants.ParseMode.MARKDOWN)
                    break

    print(PINGLIST)


async def Updater(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(update.effective_message.new_chat_members) != 0:
        for member in update.effective_message.new_chat_members:
            print(f"MEMBERU: {member.username} CBG: {context.bot.username}")
            if member.username == context.bot.username:
                await update.effective_chat.send_message(
                    'Всім привіт, тепер я буду кликати вас!\n'
                    'Я почну кликати користувача як тільки він напише хоч одне повідомлення!\n'
                    'Команда щоб покликати всіх /all | Ця команда також доступна з меню команд\n',
                    parse_mode=telegram.constants.ParseMode.MARKDOWN)
    UNick = update.effective_user.username
    UID = update.effective_user.id
    CID = update.effective_chat.id
    info = LParseUserInfoC(UID, CID)
    print(UID)
    print(CID)
    print(info)
    if len(info) == 0:
        print("LEN 0")
        if update.effective_user.username is None:
            if LAddNewProfile(CID, UID, f"!{update.effective_user.first_name}"):
                loggerm.info(
                    f"Added new user to DB:\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserFLName: {update.effective_user.full_name}\nAlternative method.")
                return
            else:
                loggerm.warning(
                    "DONT ADDED new user to DB:\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserFLName: {update.effective_user.full_name}\nAlternative method.")
                return
        LAddNewProfile(CID, UID, UNick)
        loggerm.info(
            f"Added new user to DB:\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserNickname: {UNick}")
        return 

    if update.effective_user.username is None:
        print("NONE")
        if str(info[0][2]).startswith("!"):
            if str(info[0][2]) == str(f"!{update.effective_user.first_name}"):
                loggerm.info(f"Update not need, nicks are indentical\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserFLName: {update.effective_user.full_name}\n Alternative method")
                return
            else:
                if ChangeNick(update.effective_user.id, f"!{update.effective_chat.first_name}"):
                    loggerm.info(f"NICK CHANGED!\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserFLName: {update.effective_user.full_name}\nAlternative method.")
                    return
                else:
                    logger.warning(f"NICKS DONT CHANGED, CHANGE ERROR!\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserFLName: {update.effective_user.full_name}\nAlternative method.")
                    return
    if str(info[0][2]) == str(UNick):
        loggerm.info(f"Update not need, nicks are indentical\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserNickname: {UNick}")
        return
    if ChangeNick(UID, UNick):
        loggerm.info(f"NICK CHANGED\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserNickname: {UNick}")
    else:
        loggerm.warning(f"Nick Dont changed\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserNickname: {UNick}")


async def Info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "Інформація про бота\n"
        'Бот "Поклич мене! Lite" є Вашим помічником, який покличе всіх у потрібний момент.\n'
        'Версія: 1.0\n'
        "Власник: @Quality2Length",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Github', url='https://github.com/cheuS1-n/CallMeBotUALite/')],
            [InlineKeyboardButton(text='Інші боти', url='https://t.me/cheus1_devs')]
        ])
    )


async def AllPingsUsers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.effective_message.reply_text("Використовуйте цю команду тільки в чаті групи!")
        return
    await update.effective_message.reply_text(
        f"Я можу покликати: {len(ParseAllUsers(update.effective_chat.id))} користувача(-ів).")


def STARTL():
    while True:
        Lapplication = ApplicationBuilder().token(token).build()
        Lapplication.add_handler(CommandHandler('start', start_private_chat))
        Lapplication.add_handler(CommandHandler('all', All))
        Lapplication.add_handler(CommandHandler('info', Info))
        Lapplication.add_handler(CommandHandler('userslist', AllPingsUsers))
        Lapplication.add_handler(MessageHandler(filters.ALL, Updater))
        Lapplication.run_polling()


if startdbs():
    STARTL()
else:
    logger_mysql.error("Connection failed. Can`t start the bot.")
