import sqlite3 

class DataBase:
    def __init__(self):
        self.connect_db()

    def connect_db(self):
        self.__path = r'db\history_db.db'
        self.__conn = sqlite3.connect(self.__path)
        self.__cursor = self.__conn.cursor()

    def insert_exppression(self,exp, result, dateAndTime): 
        self.__cursor.execute(f"INSERT INTO history('expression','result','date_and_time') VALUES('{exp}','{result}','{dateAndTime}')")
        self.__conn.commit()

    def delete_exppression(self,exp, result, dateAndTime): 
        self.__cursor.execute(f"DELETE FROM history WHERE expression='{exp}' and result='{result}' and date_and_time='{dateAndTime}'")       
        self.__conn.commit()

    def get_all_exppression(self): 
        data_rows = self.__cursor.execute("SELECT expression,result,date_and_time from history").fetchall() 
        return data_rows

    def close_connection(self):
        self.__conn.close()
