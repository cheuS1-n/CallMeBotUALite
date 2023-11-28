from MySQL_Driver import *


def LParseUserInfo(UID):
    try:
        info = executeSQL(f"SELECT * from MainLite WHERE UserID={UID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції ParseUserInfo. DEBUG:\n UserID: {UID}\nException: {e}")
        return False
    return info


def LParseUserInfoC(UID, CID):
    try:
        info = executeSQL(f"SELECT * from MainLite WHERE UserID={UID} AND ChannelID={CID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції ParseUserInfo. DEBUG:\n UserID: {UID}\nException: {e}")
        return False
    return info
def LAddNewProfile(CID, UID, UNickName):
    try:
        executeSQL(
            "INSERT INTO `MainLite` (`ChannelID`, `UserID`, `UserNickname`) "
            f"VALUES ('{CID}', '{UID}', '{UNickName}');")
    except Exception as e:
        logger.exception(f"Виникла помилка в функції AddNewProfile(Main). DEBUG:\nException: {e}")
        return False
    finally:
        DBCommit()
    return True

def LParseAllUsers(CID):
    try:
        info = executeSQL(f"SELECT * from MainLite WHERE ChannelID={CID}").fetchall()
    except Exception as e:
        logger.exception(f"Виникла помилка в функції ParseUserSettings. DEBUG:\n ChannelID: {CID}\nException: {e}")
        return False
    print(f"ParseAllUsers: {info}")
    return info
