#curlで辞書攻撃する

import sys
import urllib.request
import json
import glob
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 引数取ってURLを設定する
args = sys.argv
url = args[1] #ここ

# modeとかあれば
mode=""


#各CMSのjsonを読み込んでファイルからURLを作る
# CMS名、検出ファイル名、検出条件（中身正規表現 or バイト数）

# シグニチャの検出
signitures = glob.glob('signiture/*.json')
print(signitures)

# シグニチャ全部読む
for signiture in signitures:
    with open(signiture, 'r') as f:
        json_load = json.load(f)
        print ('***** '+signiture+' *****')
        for v in json_load.values():
            print(url+v['file']) 
            req = urllib.request.Request(url+v['file'])
            try:
                with urllib.request.urlopen(req) as res:
                    print (res.code)
                    # レスポンスコードは条件通りか
                    if res.code == v['response']:
                        # レスポンスのバイト数 Content-Lengthヘッダ
                        if 'length' in v:
                            headers = res.info()
                            if 'Content-Type' in headers:
                                if int(headers['Content-Length'])==v['length']:
                                    ## 何で検出したか
                                    print('length = '+ str(v['length']))
                                    print (v['CMS']+ v.get('version','*')+' is detected!')
                                    exit()                          
                        # matchワードがあれば
                        if 'match' in v:
                            body = res.read()
                            body = body.decode('utf-8')
                            if v['match'] in body:
                                ## 何で検出したか
                                print ('match ' + v['match'])
                                print (v['CMS']+ v.get('version','*')+' is detected!')
                                exit()
                        else:
                            print (v['CMS']+ v.get('version','*')+' is detected!')
                            if mode=='verbose':
                                print(str(res.read()))
                            exit()
            # HTTPError は URLError のサブクラスであるため、両方を except したい場合は HTTPError を先に書く必要がある。
            except urllib.error.HTTPError as e:
                print(e.code)
                # print(e.read())
            except urllib.error.URLError as e:
                print(e.reason)


'''
with open("./wordpress.json") as f:
	lines = f.read().splitlines()
	for line in lines:
		curlrequest[9]='Host: '+line+'.hackycorp.com'
		print(curlrequest)
		cp = subprocess.run(curlrequest, encoding='UTF-8')


'''

# 結果表示

'''
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as res:
	body = res.read()
'''

'''
フォルダ内のファイルを全部読む
from glob import glob

for file in glob(dir_name + '/*.txt'):
    print(file)
'''