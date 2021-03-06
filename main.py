import requests
import json
import time
import hashlib
import random
from sec import *

# Generate table Randomly
alphabet = list('abcdefghijklmnopqrstuvwxyz')
random.shuffle(alphabet)
table = ''.join(alphabet)[:10]



def MD5(s):
    return hashlib.md5(s.encode()).hexdigest()


def encrypt(s):
    result = ''
    for i in s:
        result += table[ord(i) - ord('0')]
    # print(result)
    return result


def Run(IMEI,sckey):


    API_ROOT = 'http://client3.aipao.me/api'  # client3 for Android
    Version = '2.40'

    # Login
    TokenRes = requests.get(
        API_ROOT + '/%7Btoken%7D/QM_Users/Login_AndroidSchool?IMEICode=' + IMEI,headers={"version":"2.40"})
    TokenJson = json.loads(TokenRes.content.decode('utf8', 'ignore'))
    print(TokenJson)

    if not TokenJson['Success']:
        requests.get(f"https://sc.ftqq.com/{sckey}.send?text=IMEI过期")
        exit(0)

    print(TokenJson)

    # headers
    token = TokenJson['Data']['Token']
    userId = str(TokenJson['Data']['UserId'])
    timespan = str(time.time()).replace('.', '')[:13]
    auth = 'B' + MD5(MD5(IMEI)) + ':;' + token
    nonce = str(random.randint(100000, 10000000))
    sign = MD5(token + nonce + timespan + userId).upper()  # sign为大写

    header = {'nonce': nonce, 'timespan': timespan,
              'sign': sign, 'version': Version, 'Accept': None, 'User-Agent': None, 'Accept-Encoding': None,
              'Connection': 'Keep-Alive'}

    # Get User Info

    GSurl = API_ROOT + '/' + token + '/QM_Users/GS'
    GSres = requests.get(GSurl, headers=header, data={})
    GSjson = json.loads(GSres.content.decode('utf8', 'ignore'))

    Lengths = GSjson['Data']['SchoolRun']['Lengths']

    print('User Info:', GSjson['Data']['User']['UserID'], GSjson['Data']['User']['NickName'],
          GSjson['Data']['User']['UserName'], GSjson['Data']['User']['Sex'])
    print('Running Info:', GSjson['Data']['SchoolRun']['Sex'], GSjson['Data']['SchoolRun']['SchoolId'],
          GSjson['Data']['SchoolRun']['SchoolName'], GSjson['Data']['SchoolRun']['MinSpeed'],
          GSjson['Data']['SchoolRun']['MaxSpeed'], GSjson['Data']['SchoolRun']['Lengths'])

    # Start Running
    SRSurl = API_ROOT + '/' + token + \
             '/QM_Runs/SRS?S1=27.116333&S2=115.032906&S3=' + str(Lengths)
    SRSres = requests.get(SRSurl, headers=header, data={})
    SRSjson = json.loads(SRSres.content.decode('utf8', 'ignore'))

    # print(SRSjson)

    # Generate Runnig Data Randomly
    RunTime = str(random.randint(700, 800))  # seconds
    RunDist = str(Lengths + random.randint(0, 3))  # meters
    RunStep = str(random.randint(1300, 1600))  # steps

    # print(RunTime,RunStep,RunDist)

    # Running Sleep
    # StartT = time.time()
    # for i in range(int(RunTime)):
    #     time.sleep(1)
    #     # print("test")
    #     print(f"Current Minutes: {i/60:.2f} Running Progress {i*100.0/int(RunTime):.2f}")
    # print("")
    # print("Running Seconds:", time.time() - StartT)

    # print(SRSurl)
    # print(SRSjson)

    RunId = SRSjson['Data']['RunId']

    # End Running
    EndUrl = API_ROOT + '/' + token + '/QM_Runs/ES?S1=' + RunId + '&S4=' + \
             encrypt(RunTime) + '&S5=' + encrypt(RunDist) + \
             '&S6=&S7=1&S8=' + table + '&S9=' + encrypt(RunStep)

    EndRes = requests.get(EndUrl, headers=header)
    EndJson = json.loads(EndRes.content.decode('utf8', 'ignore'))

    print("-----------------------")
    print("Time:", RunTime)
    print("Distance:", RunDist)
    print("Steps:", RunStep)
    print("-----------------------")

    print(EndJson)

    if (EndJson['Success']):
        print("[+]OK:", EndJson['Data'])
    else:
        print("[!]Fail:", EndJson['Data'])





if __name__ == '__main__':
    Run(IMEI,sckey)
