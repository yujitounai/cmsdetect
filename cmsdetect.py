import sys
import requests
import json
import glob
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def detection(url,v):
    print(url+v['file']) 
#    req = urllib.request.Request(url+v['file'])
    try:
        with requests.get(url+v['file'],allow_redirects=False) as response:
            print (response.status_code)#urllib.request.urlopenは301を無視する
            # レスポンスコードは条件通りか
            if response.status_code == v['response']:
                # レスポンスのバイト数 Content-Lengthヘッダ
                if 'length' in v:
                    response.headers['Content-Type']
                    if int(response.headers['Content-Length'])==v['length']:
                        ## 何で検出したか
                        print('length = '+ str(v['length']))
                        print (v['CMS']+ v.get('version','*')+' is detected!')
                        exit()
                # matchワードがあれば
                if 'match' in v:
                    if v['match'] in response.text:
                        ## 何で検出したか
                        print ('match ' + v['match'])
                        print (v['CMS']+ v.get('version','*')+' is detected!')
                        exit()
                else:
                    print (v['CMS']+ v.get('version','*')+' is detected!')
                    if mode=='verbose':
                        print(response.text)
                    exit()
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
                    print (v['CMS']+ v.get('version','*')+' is detected!')
                    exit()
            else:
                print (v['CMS']+ v.get('version','*')+' is detected!')
                exit()
    except requests.ConnectionError as e:
        print(e.reason)
        exit()
    except requests.exceptions.ConnectTimeout:
        print(e.reason)
        exit()


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
