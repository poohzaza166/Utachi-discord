import sqlite3
from sqlite3 import OperationalError

class Dbcon:
    def __init__(self,db_path):
        self.db_path = db_path
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()

    def Check_collum(self,table,collum,row):
        self.cur.execute(f"""SELECT EXISTS(SELECT * FROM "{table}" WHERE "{collum}"="{row}")""")
        res = self.cur.fetchall()
        return bool(res[0][0])

    def create_table(self,serverid):
        try:
            self.cur.execute(f"""CREATE TABLE {serverid}(userid,level,xp,doping)""")
            self.con.commit()
        except OperationalError as b:
            print(b)

    def add_table(self,serverid,userid,level,xp,doping):
        if self.Check_collum(serverid,'userid','userid') == False:
            self.cur.execute(f"""INSERT INTO {serverid} (userid,level,xp,doping) VALUES ('{userid}','{level}','{xp}','{doping}')""")
            self.con.commit()
        else:
            print('it existed')

    def mod_table(self,serverid,userid,modkey,modval):
        self.cur.execute(f'''UPDATE {serverid} SET {modkey} = {modval} where userid = "{userid}"''')
        self.con.commit()

    def read_table(self,serverid):
        self.cur.execute(f"""SELECT * FROM {serverid}""")
        rows = self.cur.fetchall()
        return rows

    def ls_tb(self,):
        self.cur.execute(f"""SELECT name from sqlite_master where type= "table" """)
        return self.cur.fetchall()

