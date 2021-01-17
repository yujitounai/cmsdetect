import sys
import sqlite3

dbname = 'cms.db'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 引数取ってURLを設定する
args = sys.argv
if args[1:]:
	pref_id = args[1]
	for a in cur.execute("SELECT * FROM PREFECRURE WHERE PREF_ID=?",(pref_id,)):
		print(a)
else:
	for a in cur.execute("SELECT * FROM PREFECRURE"):
		print(a)








conn.close()
exit()
