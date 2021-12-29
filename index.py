from module.data_base import DataBase
from datetime import datetime

db = DataBase()

# db.insert_exppression('cos(tan(0))','1','0000-00-00 00:00:00')
# db.delete_exppression('cos(tan(0))','1','0000-00-00 00:00:00')
# rows = db.get_all_exppression()
# print(rows[0])

# for i in rows:
#     print(i) 

dt_now = datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")
dt_now2 = datetime.today().strftime(f"%Y-%m-%d %H:%M:%S")
print(type(dt_now))
print(dt_now2)
