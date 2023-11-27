import sqlite3
db = sqlite3.connect('data.db')
cursor = db.cursor()
try:
    cursor.execute('''create table speedtest(
                id integer primary key  AUTOINCREMENT,
                upload double,
                download double,
                time_ymd varchar(100),
                time_hms varchar(100),
                weeks varchar(100)
                )''')  # int(20) 和integer区别
    db.commit()
    print("成功创建数据库")
except:
    print('数据库已创建')


cursor.close()
db.close()