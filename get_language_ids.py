from init_db import db
cursor  = db.cursor()

cursor.execute('select id from judge_language')

ids = list(map(lambda item: item[0], cursor.fetchall()))
ids.sort()
print(ids)