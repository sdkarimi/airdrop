from re import S, U
import sqlite3
from sqlite3 import ProgrammingError as pe


def select(chat_id):
    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT * FROM `user` WHERE `chat_id`=?"
            cursor.execute(sql, (chat_id,))
        except pe:
            print(pe.with_traceback)
            print("Something wrong!")
        else:
            rs = cursor.fetchall()
            cursor.close()
          
            return rs
    return False


def delete_user(chat_id):
    with sqlite3.connect('botuser.db') as conn :
        try :
            cursor=conn.cursor()
            sql="DELETE FROM `user` WHERE `chat_id`=?"
            cursor.execute(sql,(chat_id,))
        except pe :
            print(pe.with_traceback)
            print("Something wrong!")

def all_user():
    with sqlite3.connect('botuser.db') as conn:
        try:
            cursor=conn.cursor()
            sql = "SELECT chat_id FROM `user`"
            cursor.execute(sql)
            rs = cursor.fetchall()

            return rs
        except pe:
            print(pe.with_traceback)
            print("Something wrong!")
            

def insert(chat_id, sub=0,best_sub=0 , wallet=None,referral=None,claim_bonus=0,balance=0):
    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO `user` (`chat_id`, `sub_number`, `wallet`,`sub_number_beast`,`referral` , `bonus`,`balance`) VALUES(? , ?, ?, ?, ?, ?,?)"
            cursor.execute(sql, (chat_id, sub, wallet ,best_sub,referral,claim_bonus,balance))
        except pe:
            print(pe.with_traceback)
            print("Something wrong!")
        else:
            cursor.close()
            # print("Fine")
            return True
    return False
def add_best_sub_number(chat_id):
    best_sub = select(chat_id)[0][3]
    best_sub += 1
    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE `user` SET `sub_number_beast`=? WHERE `chat_id`=?"
            cursor.execute(sql, (best_sub,chat_id))
           
        except pe:
            print(pe.with_traceback)
            print("Something wrong!")
        else:
            cursor.close()
        
            return True
    return False
def add_sub_number(chat_id):
    sub = select(chat_id)[0][1]
    sub += 1

    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE `user` SET `sub_number`=? WHERE `chat_id`=?"
            cursor.execute(sql, (sub,chat_id))
           
        except pe:
            print(pe.with_traceback)
            print("Something wrong!")
        else:
            cursor.close()
            # print("Fine")
            return True
    return False
def select_sub_ref(chat_id):
    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT `sub_number_beast` FROM `user` WHERE `chat_id`=?"
            p = (chat_id,)
            cursor.execute(sql, p)
            
        except sqlite3.ProgrammingError as p:
            print(p.with_traceback())
            return False
        else:
            rs = cursor.fetchall()
            # print(rs)
            return rs[0] 
def if_wallet_exist(chat_id):
    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT `wallet` FROM `user` WHERE `chat_id`=?"
            p = (chat_id,)
            cursor.execute(sql, p)
            
        except sqlite3.ProgrammingError as p:
            print(p.with_traceback())
            return False
        else:
            rs = cursor.fetchall()
            
            return rs[0] if rs[0][0] else False
        
def check_wallet(wallet):
    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT `chat_id` FROM `user` WHERE `wallet`=?"
            p = (wallet,)
            cursor.execute(sql, p)
            
        except sqlite3.ProgrammingError as p:
            print(p.with_traceback())
            return False
        else:
            rs = cursor.fetchall()
            return True if rs else False

def insert_wallet(wallet, chat_id):
    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE `user` SET `wallet`=? WHERE `chat_id`=?"
            p = (wallet,chat_id)
            cursor.execute(sql, p)
        except sqlite3.ProgrammingError as p:
        
            return False
        else:
            return True

def clear_sub_number(chat_id,new_blc):
    with sqlite3.connect("botuser.db") as conn:
        try:
            curosr = conn.cursor()
            sql = "UPDATE `user` SET `balance`=? WHERE `chat_id`=?"
            curosr.execute(sql, (new_blc,chat_id))
        except sqlite3.ProgrammingError as p:
            print(p.with_traceback())
            return False
        else:
        
            return True
def set_sub_number(chat_id,new_sub):
    new_sub=int(new_sub)
    with sqlite3.connect("botuser.db") as conn:
        try:
            curosr = conn.cursor()
            sql = "UPDATE `user` SET `sub_number`=? WHERE `chat_id`=?"
            curosr.execute(sql, (new_sub,chat_id))
        except sqlite3.ProgrammingError as p:
            print(p.with_traceback())
            return False
        else:
            print(f"Sub number has been set to {new_sub}")
            return True
 
 
def insert_ref(chat_id,id):
       
 
    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE `user` SET `referral`=? WHERE `chat_id`=?"
            cursor.execute(sql, (id,chat_id))
        except pe:
            print(pe.with_traceback)
            print("Something wrong!")
        else:
            cursor.close()
            
            return True
    return False  

def insert_bonus(bonus, chat_id):
    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE `user` SET `bonus`=? WHERE `chat_id`=?"
            p = (bonus,chat_id)
            cursor.execute(sql, p)
        except sqlite3.ProgrammingError as p:
        
            return False
        else:
            return True

def set_balance(chat_id):
    balance = select(chat_id)[0][6]
    balance += 50000
    #برای تغییر مقدار دریافتی هر رفرال  به جای 50000 عدد دلخواه خود را بزارید

    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE `user` SET `balance`=? WHERE `chat_id`=?"
            cursor.execute(sql, (balance,chat_id))
           
        except pe:
            print(pe.with_traceback)
            print("Something wrong!")
        else:
            cursor.close()
            
            return True
    return False
def select_ref(chat_id):
    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT `referral` FROM `user` WHERE `chat_id`=?"
            p = (chat_id,)
            cursor.execute(sql, p)
            
        except sqlite3.ProgrammingError as p:
            print(p.with_traceback())
            return False
        else:
            rs = cursor.fetchall()
            # print(rs)
            return rs[0] 
        
def select_balance(chat_id):
    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT `balance` FROM `user` WHERE `chat_id`=?"
            p = (chat_id,)
            cursor.execute(sql, p)
            
        except sqlite3.ProgrammingError as p:
            print(p.with_traceback())
            return False
        else:
            rs = cursor.fetchall()
            # print(rs)
            return rs[0]         
def select_bonus(chat_id):
    with sqlite3.connect("botuser.db") as conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT `bonus` FROM `user` WHERE `chat_id`=?"
            p = (chat_id,)
            cursor.execute(sql, p)
            
        except sqlite3.ProgrammingError as p:
            print(p.with_traceback())
            return False
        else:
            rs = cursor.fetchall()
            # print(rs)
            return rs[0]    


        
if __name__ == "__main__":
    
    select(1234)
   