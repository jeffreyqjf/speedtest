import sqlite3
data = sqlite3.connect('data.db')
cursor = data.cursor()
cursor.execute('''select * from speedtest''')
result = cursor.fetchall()
for i in result:
    print(i)