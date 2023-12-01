from MySQL_Driver import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("Func_file")

def CheckAllUserChannels(UID):
    try:
        info = executeSQL(f"SELECT ChannelID from Main WHERE UserID={UID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції CheckAllUserChannels. DEBUG:\n UserID: {UID}\nException: {e}")
        return False
    return info


def ParseUserInfo(UID):
    try:
        info = executeSQL(f"SELECT * from Main WHERE UserID={UID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції ParseUserInfo. DEBUG:\n UserID: {UID}\nException: {e}")
        return False
    return info


def ParseUserInfoC(UID, CID):
    try:
        info = executeSQL(f"SELECT * from Main WHERE UserID={UID} AND ChannelID={CID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції ParseUserInfo. DEBUG:\n UserID: {UID}\nException: {e}")
        return False
    return info


def ParseUserSettings(UID):
    try:
        info = executeSQL(f"SELECT * from Settings WHERE UserID={UID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції ParseUserSettings. DEBUG:\n UserID: {UID}\nException: {e}")
        return False
    print(f"IFFO: {info}")
    return info


def ParseAllUsers(CID):
    try:
        info = executeSQL(f"SELECT * from Main WHERE ChannelID={CID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції ParseUserSettings. DEBUG:\n ChannelID: {CID}\nException: {e}")
        return False
    print(f"ParseAllUsers: {info}")
    return info


def ChangeNick(UID, NewNick):
    try:
        info = sendSQL(f"UPDATE Main SET UserNickname='{NewNick}' WHERE UserID={UID}")
    except Exception as e:
        logger.exception(
            f"Виникла помилка в функції ChangeNick. DEBUG:\n UserID: {UID}\n param: {NewNick}\nException: {e}")
        return False
    finally:
        DBCommit()
    print(f"ChangeNick: {info} | {NewNick}")
    return True


def RBS(Nick: str):
    BS = ['"', "'", '`', '*']
    n = Nick
    for x in BS:
        print(f"{x}")
        if x in n:
            print("YES")
            n = n.replace(f"{x}", "")
    return str(n)


