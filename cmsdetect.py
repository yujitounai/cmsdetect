import sys
import urllib.request
import json
import glob
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def detection(url,v):
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
        # レスポンスコードは条件通りか
        # エラーコード（5xx,4xx）の時はこっちに例外が飛ぶ
        if e.code == v['response']:
            print (v['CMS']+ v.get('version','*')+' is detected!')
            exit()
    except urllib.error.URLError as e:
        print(e.reason)

# 引数取ってURLを設定する
args = sys.argv
url = args[1] #ここ
signiture=""
if args[2:]:
    signiture = args[2]
# modeとかあれば
mode=""

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
            for v in json_load.values():
                detection(url,v)
else:
    with open('signiture/'+signiture, 'r') as f:
        json_load = json.load(f)
        print ('***** '+signiture+' *****')
        for v in json_load.values():
            detection(url,v)   
