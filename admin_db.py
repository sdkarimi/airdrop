import sqlite3
import hashlib

DEFUALT_SAULT = "THisfjdkslm,8732@#"

def is_exist(username, password):
    pass_hash = get_hash(password)
    with sqlite3.connect("bot.db") as conn:
        cursor = conn.cursor()
        sql = "SELECT * FROM `admins` WHERE `username`=? AND `password`=?"
        try:
            cursor.execute(sql, (username, pass_hash))
        except sqlite3.ProgrammingError as ex:
            print(ex.with_traceback)
            print("Something wrong")
            return False
        else:
            rs = cursor.fetchall()
            print(rs)
            return True if rs else False

def get_hash(string: str) -> str:
    temp = DEFUALT_SAULT + string
    sha = hashlib.sha256()
    sha.update(temp.encode("utf-8"))
    return sha.hexdigest()


if __name__ == "__main__":
    print(get_hash("123"))
    
