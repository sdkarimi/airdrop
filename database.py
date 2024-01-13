import sqlite3

def create_table_users():
    with sqlite3.connect("botuser.db") as conn:
        cursor = conn.cursor()
        create_sql = """
            CREATE TABLE IF NOT EXISTS `user`(
                `chat_id` INTEGER NOT NULL PRIMARY KEY,
                `sub_number` INTEGER NOT NULL,
                `wallet` TEXT UNIQUE,
                `sub_number_beast` INTEGER NOT NULL,
                `referral` TEXT ,
                `bonus` INTEGER NOT NULL,
                `balance` INTEGER NOT NULL
            )
        """
        # `link` TEXT NOT NULL UNIQUE
        try:
            cursor.execute(create_sql)
        except sqlite3.ProgrammingError as e:
            print(e.with_traceback)
            print("Something wrong!")
        else:
            cursor.close()
            print("Table user created!")

def create_table_admins():
    with sqlite3.connect("bot.db") as conn:
        cursor = conn.cursor()
        create_sql = """
            CREATE TABLE IF NOT EXISTS `admins` (
                `username` TEXT NOT NULL PRIMARY KEY,
                `password` TEXT NOT NULL
            )
        """
        try:
            cursor.execute(create_sql)
        except sqlite3.ProgrammingError as e:
            print(e.with_traceback)
            print("Something wrong!")
        else:
            cursor.close()
            print("Table Created")


        
if __name__ == "__main__":
    create_table_users()
    create_table_admins()
    
