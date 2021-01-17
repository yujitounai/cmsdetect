import sys
import requests
import json
import glob
import ssl
import sqlite3
import datetime


# create cms.db
# If the database already exists, access it.
dbname = 'cms.db'
conn = sqlite3.connect(dbname)

# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# 存在しない場合はテーブル作成
cur.execute('CREATE TABLE IF NOT EXISTS PREFECRURE(ID INTEGER PRIMARY KEY,PREF_ID INTEGER,CITY TEXT,URL TEXT,CMS TEXT,SIGNITURE TEXT,DETECTED INTEGER,CREATED TEXT)')
conn.commit()

ssl._create_default_https_context = ssl._create_unverified_context

def detection(url,v):
	print(url+v['file']) 
#	req = urllib.request.Request(url+v['file'])
	try:
		with requests.get(url+v['file'],allow_redirects=False,timeout=(3.0, 7.5)) as response:
			print (response.status_code)#urllib.request.urlopenは301を無視する
			# レスポンスコードは条件通りか
			if response.status_code == v['response']:
				# レスポンスのバイト数 Content-Lengthヘッダ
				if 'length' in v:
					if response.headers:
						if response.headers.get('Content-Length')==v['length']:
							print(response.headers.get('Content-Length'))
							## 何で検出したか
							print('length = '+ str(v['length']))
							return 1
				# matchワードがあれば
				if 'match' in v:
					response.encoding = 'UTF-8' # 文字化け対策
					if v['match'] in response.text:
						## 何で検出したか
						print ('match ' + v['match'])
						return 1
					response.encoding = 'EUC-JP' # 文字化け対策
					if v['match'] in response.text:
						## 何で検出したか
						print ('match ' + v['match'])
						return 1
				else:
					if mode=='verbose':
						print(response.text)
					return 1
	# HTTPError は URLError のサブクラスであるため、両方を except したい場合は HTTPError を先に書く必要がある。
	except requests.HTTPError as e:
		print(e.code)
		# レスポンスコードは条件通りか
		# エラーコード（5xx,4xx）の時はこっちに例外が飛ぶ
		if e.code == v['response']:
		# matchワードがあれば
			if 'match' in v:
				body = e.read()
				body = body.decode('utf-8', errors="backslashreplace")
				if v['match'] in body:
				## 何で検出したか
					print ('match ' + v['match'])
					return 1
			else:
				return 1
	except requests.exceptions.ConnectTimeout as e:
		print(e)
	except requests.exceptions.RequestException as e:
		print(e)
	except requests.ConnectionError as e:
		print(e)

# 引数取ってURLを設定する
args = sys.argv
url = args[3] #ここ
signiture=""
# 都道府県
pref = args[1]
# 市町村
city = args[2]

if args[4:]:
	signiture = args[4]

#各CMSのjsonを読み込んでファイルからURLを作る
# CMS名、検出ファイル名、検出条件（中身正規表現 or バイト数）

# シグニチャの検出
signitures = glob.glob('signiture/*.json')
print(signitures)

if signiture =="":
	# シグニチャ全部読む
	for signiture in signitures:
		with open(signiture, 'r') as f:
			json_load = json.load(f)
			print ('***** '+signiture+' *****')
			for k,v in json_load.items():
				if detection(url,v)==1:
					print(signiture[10:])
					print(k)
					print (v['CMS']+ v.get('version','*')+' is detected!')
					cur.execute("INSERT INTO PREFECRURE (PREF_ID, CITY, URL, CMS, SIGNITURE, DETECTED, CREATED) VALUES (?, ?, ?, ?, ?, ?, ?)",
					(pref,city,url,signiture[10:],k,1,datetime.datetime.now()))
					conn.commit()
					# close the DB
					conn.close()
					exit()
	cur.execute("INSERT INTO PREFECRURE (PREF_ID, CITY, URL, DETECTED, CREATED) VALUES (?, ?, ?, ?, ?)",
	(pref,city,url,0,datetime.datetime.now()))
	conn.commit()
	conn.close()
else: # 個別シグニチャ呼び出し
	with open('signiture/'+signiture, 'r') as f:
		json_load = json.load(f)
		print ('***** '+signiture+' *****')
		for v in json_load.values():
			if detection(url,v)==1:
				exit()
