#!/bin/python
from os import system
try: from requests import post, get
except ModuleNotFoundError : system("pip install requests"); from requests import post, get
try: import datetime
except ModuleNotFoundError : system('pip install datetime'); import datetime
from re import findall; from pathlib import Path; from random import randint, choice; from json import loads, dumps, JSONDecodeError; import base64, urllib3; from Crypto.Cipher import AES; from Crypto.Util.Padding import pad, unpad; from time import sleep; urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class encryption :
    def __init__(self, auth: str) -> None :
        self.key = bytearray(self.secret(auth), "UTF-8"); self.iv = bytearray.fromhex('00000000000000000000000000000000')
    def replaceCharAt(self, e, t, i) : return e[0:t] + i + e[t + len(i):]
    def secret(self, e) :
        t, i, s = e[0:8], e[8:16], 0; n = e[16:24] + t + e[24:32] + i
        while s < len(n) :
            e = n[s]
            if e >= '0' and e <= '9' :
                t = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
                n = self.replaceCharAt(n, s, t)
            else :
                t = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
                n = self.replaceCharAt(n, s, t)
            s += 1
        return n
    def encrypt(self, text: str) -> str :
        raw, aes = pad(text.encode('UTF-8'), AES.block_size), AES.new(self.key, AES.MODE_CBC, self.iv); enc = aes.encrypt(raw); result = base64.b64encode(enc).decode('UTF-8'); return result
    def decrypt(self, text: str) -> str :
        aes = AES.new(self.key, AES.MODE_CBC, self.iv); dec = aes.decrypt(base64.urlsafe_b64decode(text.encode('UTF-8'))); result = unpad(dec, AES.block_size).decode('UTF-8'); return result
class accesses :
    class admin : pin, newAdmin, editInfo, banMember, changeLink, editMemberAccess, deleteMessages = "PinMessages", "setAdmin", "ChangeInfo", "BanMember", "SetJoinLink", "SetMemberAccess", "DeleteGlobalAllMessages"
    class user : viewMembers, viewAdmins, sendMessage, addMember= "ViewMembers", "ViewAdmins", "SendMessages", "AddMember"
class clients :
    web, android = {
        "app_name":"Main",
        "app_version":"4.1.4",
        "platform":"Web",
        "package":"web.rubika.ir",
        "lang_code":"fa"
    }, {
        "app_name":"Main",
        "app_version":"2.8.1",
        "platform":"Android",
        "package":"ir.resaneh1.iptv",
        "lang_code":"fa"
    }
defaultDevice: dict = {
    "app_version":"MA_2.9.8",
    "device_hash":"CEF34215E3E610825DC1C4BF9864D47A",
    "device_model":"rubx-lib",
    "is_multi_account": False,
    "lang_code":"fa",
    "system_version":"SDK 22",
    "token":"cgpzI3mbTPKddhgKQV9lwS:APA91bE3ZrCdFosZAm5qUaG29xJhCjzw37wE4CdzAwZTawnHZM_hwZYbPPmBedllAHlm60v5N2ms-0OIqJuFd5dWRAqac2Ov-gBzyjMx5FEBJ_7nbBv5z6hl4_XiJ3wRMcVtxCVM9TA-",
    "token_type":"Firebase"
}
citys, proxys, auth_, sent = [], [], [], (lambda data: ['error' if data['status'].lower() != 'ok' else 'yeah'])
class Robot :
    def __init__(self, app='rubx', phone_number=None, auth=None, device=defaultDevice, proxy={'http':'http://127.0.0.1:9050'}, your_name='rubx', city='tehran', logo=True) -> None :
        self.app = app; citys.append(city); self.proxy = proxy; proxys.append(proxy)
        if logo != False : [(print(s, flush=True, end=''), sleep(0.01)) for s in f'\n\033[0m< \033[31mrubx \033[0m> \033[36m | \033[31mstarted in \033[0m{str(datetime.datetime.now())}\n']
        if your_name != None :
            self.your_name = your_name
            try :
                with open('library-info.txt', 'w+') as f: f.write('name fan: '+your_name+'\ntime started: '+str(datetime.datetime.now())+'\nyour ip: '+str(get('https://api.ipify.org').text))
            except : pass
        try:
            if auth == None:
                with open(f"{app}.json", "r") as account :
                    account = loads(account.read())
                    self.auth = account["data"]["auth"]; auth_.append(self.auth)
            else: raise FileNotFoundError('file not find')
        except FileNotFoundError :
                if auth != None :
                    self.auth = auth; auth_.append(auth)
                elif phone_number != None :
                    try:
                        code = Robot.sendCode(phone_number, 'Internal')["data"]["phone_code_hash"]; account = Robot.signIn(phone_number, code, input("please enter activation code : "))
                        with open(f"{app}.json", "w") as file : file.write(dumps(account, indent=4, ensure_ascii=False))
                        self.auth = account["data"]["auth"]; auth_.append(self.auth); Robot.registerDevice(self.auth, device=device)
                    except KeyboardInterrupt : exit()
                else :
                    try :
                        phone_number = input("please enter your phone number : "); code = Robot.sendCode(phone_number, 'Internal')["data"]["phone_code_hash"]; account = Robot.signIn(phone_number, code, input("please enter activation code : ")); self.auth = account["data"]["auth"]; auth_.append(self.auth)
                        with open(f"{app}.json", "w") as file :
                            file.write(dumps(account, indent=4, ensure_ascii=False))
                        Robot.registerDevice(self.auth, device=device)
                    except KeyboardInterrupt :
                        exit()
        except JSONDecodeError : raise RuntimeError(f"\033[35mfile is invalid. please login again to your account and then DO NOT modify the {app}.json")
        self.enc = encryption(self.auth)
    def __enter__(self) : return self
    def __exit__(self, *args, **kwargs) -> None : pass
    @staticmethod
    def _getURL() -> str :
        servers: dict = {"API": {
            "174": "https://messengerg2c74.iranlms.ir",
            "122": "https://messengerg2c22.iranlms.ir", 
            "101": "https://messengerg2c59.iranlms.ir/", 
            "102": "https://messengerg2c2.iranlms.ir",
            "103": "https://messengerg2c3.iranlms.ir",
            "104": "https://messengerg2c4.iranlms.ir", 
            "105": "https://messengerg2c5.iranlms.ir",
            "106": "https://messengerg2c6.iranlms.ir",
            "107": "https://messengerg2c7.iranlms.ir", 
            "108": "https://messengerg2c8.iranlms.ir",
            "109": "https://messengerg2c9.iranlms.ir",
            "110": "https://messengerg2c10.iranlms.ir",
            "111": "https://messengerg2c11.iranlms.ir", 
            "112": "https://messengerg2c12.iranlms.ir",
            "113": "https://messengerg2c13.iranlms.ir", 
            "114": "https://messengerg2c14.iranlms.ir",
            "115": "https://messengerg2c15.iranlms.ir", 
            "116": "https://messengerg2c16.iranlms.ir",
            "117": "https://messengerg2c17.iranlms.ir", 
            "118": "https://messengerg2c18.iranlms.ir",
            "119": "https://messengerg2c19.iranlms.ir", 
            "120": "https://messengerg2c20.iranlms.ir",
            "121": "https://messengerg2c21.iranlms.ir",
            "122": "https://messengerg2c21.iranlms.ir",
            "123": "https://messengerg2c23.iranlms.ir",
            "124": "https://messengerg2c24.iranlms.ir",
            "125": "https://messengerg2c25.iranlms.ir",
            "126": "https://messengerg2c26.iranlms.ir",
            "127": "https://messengerg2c26.iranlms.ir",
            "128": "https://messengerg2c28.iranlms.ir",
            "129": "https://messengerg2c29.iranlms.ir",
            "130": "https://messengerg2c30.iranlms.ir", 
            "131": "https://messengerg2c31.iranlms.ir", 
            "132": "https://messengerg2c32.iranlms.ir", 
            "133": "https://messengerg2c33.iranlms.ir",
            "134": "https://messengerg2c34.iranlms.ir",
            "135": "https://messengerg2c35.iranlms.ir",
            "136": "https://messengerg2c36.iranlms.ir", 
            "137": "https://messengerg2c37.iranlms.ir", 
            "138": "https://messengerg2c38.iranlms.ir", 
            "139": "https://messengerg2c39.iranlms.ir",
            "140": "https://messengerg2c40.iranlms.ir", 
            "141": "https://messengerg2c41.iranlms.ir", 
            "142": "https://messengerg2c42.iranlms.ir", 
            "143": "https://messengerg2c43.iranlms.ir", 
            "144": "https://messengerg2c44.iranlms.ir", 
            "145": "https://messengerg2c45.iranlms.ir", 
            "146": "https://messengerg2c46.iranlms.ir", 
            "147": "https://messengerg2c47.iranlms.ir", 
            "148": "https://messengerg2c48.iranlms.ir", 
            "149": "https://messengerg2c49.iranlms.ir", 
            "150": "https://messengerg2c50.iranlms.ir", 
            "151": "https://messengerg2c51.iranlms.ir", 
            "152": "https://messengerg2c52.iranlms.ir", 
            "153": "https://messengerg2c53.iranlms.ir",
            "154": "https://messengerg2c54.iranlms.ir"
            }
                         }
        if citys[0].lower() == 'mashhad':
            return servers['API']['137']
        elif citys[0].lower() == 'ahvaz':
            return servers['API']['154']
        elif citys[0].lower() == 'esfahan':
            return servers['API']['147']
        elif citys[0].lower() == 'tehran':
            return servers['API']['101']
        else:
            return servers['API'][str(randint(101, 154))]
    @staticmethod
    def getUrl() -> dict :
        for i in range(10) :
            try: return loads(post(url='https://getdcmess.iranlms.ir/', json = {"api_version":"4","method":"getDCs","client":clients.web}, timeout=5)); break
            except: pass
    @staticmethod
    def _tmpGeneration() -> str :
        tmp_session, choices = '', [*"abcdefghijklmnopqrstuvwxyz0123456789"]
        for i in range(32): tmp_session += choice(choices)
        return tmp_session
    @staticmethod
    def sendCode(phone_number: str, send_type='SMS', password=None) -> dict:
        '''send_type <- key/value -> SMS/Internal '''
        tmp = Robot._tmpGeneration(); enc = encryption(tmp); req = {"phone_number":f"98{phone_number[1:]}", "send_type": send_type}
        if password != None : req['pass_key'] = password
        while 1 :
            try :
                return loads(enc.decrypt(post(json={"api_version":"5","tmp_session": tmp,"data_enc": enc.encrypt(dumps({
                    "method":"sendCode",
                    "input":req,
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=proxys[0]).json()["data_enc"]))
            except Exception as e : print(e)
    @staticmethod
    def signIn(phone_number,phone_code_hash,phone_code) -> dict :
        '''
        phone_number : phone number of target's account : 09XXXXXXXXX
        phone_code_hash : hash of code sent to phone
        phone_code : code sent to phone
        '''
        while 1 :
            try :
                tmp = Robot._tmpGeneration()
                enc = encryption(tmp)
                return loads(enc.decrypt(post(json={"api_version":"5","tmp_session": tmp,"data_enc":enc.encrypt(dumps({
                    "method":"signIn",
                    "input":{
                        "phone_number":f"98{phone_number[1:]}",
                        "phone_code_hash":phone_code_hash,
                        "phone_code":phone_code
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=proxys[0]).json().get("data_enc")))
            except Exception as e : print(e)
    @staticmethod
    def registerDevice(auth, device=defaultDevice) -> dict :
        while 1 :
            try :
                enc = encryption(auth); response = loads(enc.decrypt(post(json={
                    "api_version":"4",
                    "auth":auth,
                    "client": clients.android,
                    "data_enc":enc.encrypt(dumps(device)),
                    "method":"registerDevice",
                },url=Robot._getURL(), proxies=proxys[0]).json()["data_enc"]))
                return response
            except JSONDecodeError : break
    @staticmethod
    def _parse (mode: str, text: str) -> list :
        results: list = []
        if mode.upper() == "HTML" :
            realText = text.replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", "").replace("<pre>", "").replace("</pre>", ""); bolds = findall("<b>(.*?)</b>", text); italics = findall("<i>(.*?)</i>", text); monos = findall("<pre>(.*?)</pre>", text); bResult = [realText.index(i) for i in bolds]; iResult = [realText.index(i) for i in italics]; mResult = [realText.index(i) for i in monos]
            for bIndex,bWord in zip(bResult,bolds) : 
                results.append({
                    "from_index": bIndex,
                    "length": len(bWord),
                    "type": "Bold"
                })
            for iIndex,iWord in zip(iResult,italics) :
                results.append({
                    "from_index": iIndex,
                    "length": len(iWord),
                    "type": "Italic"
                })
            for mIndex,mWord in zip(mResult,monos) :
                results.append({
                    "from_index": mIndex,
                    "length": len(mWord),
                    "type": "Mono"
                })
        elif mode.lower() == "markdown" :
            realText = text.replace("**", "").replace("__", "").replace("`", ""); bolds = findall(r"\*\*(.*?)\*\*", text); italics = findall(r"\_\_(.*?)\_\_",text); monos = findall("`(.*?)`",text); bResult = [realText.index(i) for i in bolds]; iResult = [realText.index(i) for i in italics];  mResult = [realText.index(i) for i in monos]
            for bIndex,bWord in zip(bResult,bolds):
                results.append({
                    "from_index": bIndex,
                    "length": len(bWord),
                    "type": "Bold"
                })
            for iIndex,iWord in zip(iResult,italics):
                results.append({
                    "from_index": iIndex,
                    "length": len(iWord),
                    "type": "Italic"
                })
            for mIndex,mWord in zip(mResult,monos):
                results.append({
                    "from_index": mIndex,
                    "length": len(mWord),
                    "type": "Mono"
                })
        return results
    def _requestSendFile(self, file):
        return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
            "method":"requestSendFile",
            "input":{
                "file_name": str(file.split("/")[-1]),
                "mime": file.split(".")[-1],
                "size": Path(file).stat().st_size
            },
            "client": clients.web
        }))},url=Robot._getURL(), proxies=self.proxy).json()["data_enc"]))["data"]
    def _uploadFile(self, file):
        if not "http" in file:
            frequest = Robot._requestSendFile(self, file)
            bytef = open(file,"rb").read()
            hash_send = frequest["access_hash_send"]
            file_id = frequest["id"]
            url = frequest["upload_url"]
            header = {
                'auth':self.auth,
                'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
                'chunk-size':str(Path(file).stat().st_size),
                'file-id':str(file_id),
                'access-hash-send':hash_send,
                "content-type": "application/octet-stream",
                "content-length": str(Path(file).stat().st_size),
                "accept-encoding": "gzip",
                "user-agent": "okhttp/3.12.1"
            }
            if len(bytef) <= 131072 :
                header["part-number"], header["total-part"] = "1", "1"
                while 1 :
                    try :
                        j = post(data=bytef, url=url, headers=header).text; j = loads(j)['data']['access_hash_rec']; break
                    except Exception : continue
                return [frequest, j]
            else :
                t: int = round(len(bytef) / 131072 + 1)
                for i in range(1,t+1) :
                    if i != t :
                        k = i - 1; k = k * 131072
                        while 1 :
                            try :
                                header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t); o = post(data=bytef[k:k + 131072],url=url,headers=header).text; o = loads(o)['data']; break
                            except Exception : continue
                    else :
                        k = i - 1; k = k * 131072
                        while 1 :
                            try : header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t); p = post(data=bytef[k:],url=url,headers=header).text; p = loads(p)['data']['access_hash_rec']; break
                            except Exception : continue
                        return [frequest, p]
        else :
            frequest = loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                "method":"requestSendFile",
                "input":{
                    "file_name": file.split("/")[-1],
                    "mime": file.split(".")[-1],
                    "size": len(get(file).content)
                },
                "client": clients.web
            }))},url=Robot._getURL()).json()["data_enc"]))["data"]
            hash_send = frequest["access_hash_send"]; file_id = frequest["id"]; url = frequest["upload_url"]; bytef = get(file).content
            header = {
                'auth':self.auth,
                'Host':url.replace("https://","").replace("/UploadFile.ashx",""),
                'chunk-size':str(len(get(file).content)),
                'file-id':str(file_id),
                'access-hash-send':hash_send,
                "content-type": "application/octet-stream",
                "content-length": str(len(get(file).content)),
                "accept-encoding": "gzip",
                "user-agent": "okhttp/3.12.1"
            }
            if len(bytef) <= 131072 :
                header["part-number"], header["total-part"] = "1", "1"
                while 1 :
                    try : j = post(data=bytef,url=url,headers=header).text; j = loads(j)['data']['access_hash_rec']; break
                    except Exception : continue
                return [frequest, j]
            else :
                t = round(len(bytef) / 131072 + 1)
                for i in range(1,t+1):
                    if i != t :
                        k = i - 1; k = k * 131072
                        while 1 :
                            try : header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t); o = post(data=bytef[k:k + 131072],url=url,headers=header).text; o = loads(o)['data']; break
                            except : continue
                    else :
                        k = i - 1; k = k * 131072
                        while 1 :
                            try : header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t); p = post(data=bytef[k:],url=url,headers=header).text; p = loads(p)['data']['access_hash_rec']; break
                            except Exception : continue
                        return [frequest, p]
    @staticmethod
    def _getThumbInline(image_bytes: bytes) -> bytes :
        import io, base64, PIL.Image; im = PIL.Image.open(io.BytesIO(image_bytes)); width, height = im.size
        if height > width : new_height = 40; new_width  = round(new_height * width / height)
        else : new_width  = 40; new_height = round(new_width * height / width)
        im = im.resize((new_width, new_height), PIL.Image.ANTIALIAS); changed_image = io.BytesIO(); im.save(changed_image, format='PNG'); changed_image = changed_image.getvalue(); return base64.b64encode(changed_image)
    @staticmethod
    def _getImageSize(image_bytes: bytes) -> list[str, ]:
        import io, PIL.Image; im = PIL.Image.open(io.BytesIO(image_bytes)); width, height = im.size; return [width , height]
    def getChats(self, start_id=None) -> dict :
        for i in range(3) :
            try :
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getChats",
                    "input":{
                        "start_id":start_id
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
                break
            except : pass
    def sendMessage(self, chat_id, text, metadata=[], parse_mode=None, message_id=None) -> dict:
        inData = {
            "method":"sendMessage",
            "input":{
                "object_guid":chat_id,
                "rnd":f"{randint(100000,999999999)}",
                "text":text,
                "reply_to_message_id":message_id
            },
            "client": clients.web
        }
        if metadata != [] : inData["input"]["metadata"] = {"meta_data_parts":metadata}
        if parse_mode != None : inData["input"]["metadata"] = {"meta_data_parts": Robot._parse(parse_mode, text)}; inData["input"]["text"] = text.replace("<b>","").replace("</b>","").replace("<i>","").replace("</i>","").replace("<pre>","").replace("</pre>","") if parse_mode.upper() == "HTML" else text.replace("**","").replace("__","").replace("`","")
        for i in range(4) :
            try: return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps(inData))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def editMessage(self, message_id, chat_id, newText, metadata=[], parse_mode=None) -> dict:
        inData = {
            "method":"editMessage",
            "input":{
                "message_id": message_id,
                "object_guid": chat_id,
                "text": newText
            },
            "client": clients.web}
        if metadata != [] : inData["input"]["metadata"] = {"meta_data_parts":metadata}
        if parse_mode != None : inData["input"]["metadata"] = {"meta_data_parts":Robot._parse(parse_mode, newText)}; inData["input"]["text"] = newText.replace("<b>","").replace("</b>","").replace("<i>","").replace("</i>","").replace("<pre>","").replace("</pre>","") if parse_mode.upper() == "HTML" else newText.replace("**","").replace("__","").replace("`","")
        for i in range(4):
            try: return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({inData}))},url=Robot._getURL(), proxies=self.proxy, timeout=5).json()["data_enc"])); break
            except: pass
    def _setMethods_(data: dict, mode=None) -> dict :
        '''mode for client android and web'''
        enc: encryption = encryption(auth_[0])
        for i in range(4):
            try: return loads(enc.decrypt(post(json={"api_version":"5","auth":auth_[0],"data_enc":enc.encrypt(dumps(data))}, url=Robot._getURL(), timeout=5, proxies=proxys[0]).json()["data_enc"])); break
            except: pass
    getChatsUpdates = (lambda self, state='0' : Robot._setMethods_(data={"method":"getChatsUpdates","input":{"state":state},"client":{"app_name":"Main","app_version":"4.1.4","platform":"Web","package":"web.rubika.ir","lang_code":"fa"}}))
    getMessagesInterval = (lambda self, guid, middle_message_id : Robot._setMethods_({"method":"getMessagesInterval","input":{"object_guid":guid,"middle_message_id":middle_message_id},"client":{"app_name":"Main","app_version":"4.1.4","platform":"Web","package":"web.rubika.ir","lang_code":"fa"}}))
    getFolders = (lambda self : Robot._setMethods_({"method":"getFolders","input":{},"client":{"app_name":"Main","app_version":"4.1.4","platform":"Web","package":"web.rubika.ir","lang_code":"fa"}}))
    def getStickersBySetIDs(self, sticker_set_ids: list) -> dict :
        '''sticker ids :  ['5e0c957a6282726921b7634n', '6e0c957a6282726921b7635l']'''
        # server client: api https://messengerg2c121.iranlms.ir/
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getStickersBySetIDs",
                    "input":{
                        "sticker_set_ids":sticker_set_ids},
                    "client": clients.web
                }))},url='https://messengerg2c121.iranlms.ir/', timeout=5, proxies=self.proxy).json()["data_enc"]))
                break
            except: pass
    def deleteMessages(self, chat_id, message_ids) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"deleteMessages",
                    "input":{
                        "object_guid":chat_id,
                        "message_ids":message_ids,
                        "type":"Global"
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
                break
            except: pass
    def getUserInfo(self, chat_id) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getUserInfo",
                    "input":{
                        "user_guid":chat_id
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def getMessages(self, chat_id,min_id) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getMessagesInterval",
                    "input":{
                        "object_guid":chat_id,
                        "middle_message_id":min_id
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), proxies=self.proxy, timeout=5).json().get("data_enc"))).get("data").get("messages")
            except: pass
    def getInfoByUsername(self, username) -> dict:
        ''' username should be without @ '''
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getObjectByUsername",
                    "input":{
                        "username":username
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json().get("data_enc")))
            except: pass
    def banGroupMember(self, chat_id, user_id) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"banGroupMember",
                    "input":{
                        "group_guid": chat_id,
                        "member_guid": user_id,
                        "action":"Set"
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def unbanGroupMember(self, chat_id, user_id) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "client": clients.android,
                    "input":{
                        "group_guid": chat_id,
                        "member_guid": user_id,
                        "action":"Unset"
                    },
                    "method":"banGroupMember"
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def invite(self, chat_id: str, user_ids: list) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"addGroupMembers",
                    "input":{
                        "group_guid": chat_id,
                        "member_guids": user_ids
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5).json()["data_enc"]))
            except: pass
    def inviteChannel(self, chat_id: str, user_ids: list) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"addChannelMembers",
                    "input":{
                        "channel_guid": chat_id,
                        "member_guids": user_ids
                    },
                    "client": clients.web
                }))},url=Robot._getURL(),timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def getGroupAdmins(self, chat_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "client": clients.android,
                    "input":{
                        "group_guid":chat_id
                    },
                    "method":"getGroupAdminMembers"
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json().get("data_enc")))
            except: pass
    def getMessagesInfo(self, chat_id: str, message_ids: list) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getMessagesByID",
                    "input":{
                        "object_guid": chat_id,
                        "message_ids": message_ids
                    },
                    "client": clients.web
                }))}, url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"])).get("data").get("messages")
            except: pass
    def setMembersAccess(self, chat_id: str, access_list: list) -> dict:
        for i in range(4):
            try:
                return post(json={
                    "api_version": "4",
                    "auth": self.auth,
                    "client": clients.android,
                    "data_enc": self.enc.encrypt(dumps({
                        "access_list": access_list,
                        "group_guid": chat_id
                    })),
                    "method": "setGroupDefaultAccess"
                }, url=Robot._getURL(), timeout=5, proxies=self.proxy)
            except: pass
    def getGroupMembers(self, chat_id: str, start_id=None) -> dict:
        """use:  bot.getGroupMembers('guid', '0')"""
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={
                    "api_version":"5",
                        "auth": self.auth,
                        "data_enc": self.enc.encrypt(dumps({
                            "method":"getGroupAllMembers",
                            "input":{
                                "group_guid": chat_id,
                                "start_id": start_id
                            },
                            "client": clients.web
                    }))
                }, url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def getGroupInfo(self, chat_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(
                    json={
                        "api_version":"5",
                        "auth": self.auth,
                        "data_enc": self.enc.encrypt(dumps({
                            "method":"getGroupInfo",
                            "input":{
                                "group_guid": chat_id,
                            },
                            "client": clients.web
                    }))}, url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def getGroupLink(self, chat_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getGroupLink",
                    "input":{
                        "group_guid":chat_id
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json().get("data_enc"))).get("data").get("join_link")
            except: pass
    def changeGroupLink(self, chat_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={
                    "api_version":"4",
                    "auth":self.auth,
                    "client": clients.android,
                    "data_enc":self.enc.encrypt(dumps({
                        "group_guid": chat_id
                    })),
                    "method":"setGroupLink",
                },url=Robot._getURL(), proxies=self.proxy).json()["data_enc"]))
            except: pass
    def setGroupTimer(self, chat_id: str, time: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={
                    "api_version":"4",
                    "auth":self.auth,
                    "client": clients.android,
                    "data_enc":self.enc.encrypt(dumps({
                        "group_guid": chat_id,
                        "slow_mode": time,
                        "updated_parameters":["slow_mode"]
                    })),
                    "method":"editGroupInfo"
                },url=Robot._getURL(), proxies=self.proxy).json()["data_enc"]))
            except: pass
    def setGroupAdmin(self, chat_id: str, user_id: str, access_list=[]) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"setGroupAdmin",
                    "input":{
                        "group_guid": chat_id,
                        "access_list": access_list,
                        "action": "SetAdmin",
                        "member_guid": user_id
                    },
                    "client": clients.android
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def deleteGroupAdmin(self, chat_id: str, user_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"setGroupAdmin",
                    "input":{
                        "group_guid": chat_id,
                        "action": "UnsetAdmin",
                        "member_guid": user_id
                    },
                    "client": clients.android
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def logout(self) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"logout",
                    "input":{},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def forwardMessages(self, From: str, message_ids: list[str,], to: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"forwardMessages",
                    "input":{
                        "from_object_guid": From,
                        "message_ids": message_ids,
                        "rnd": f"{randint(100000,999999999)}",
                        "to_object_guid": to
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def seenChats(self, seenList: list) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"seenChats",
                    "input":{
                        "seen_list": seenList
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def sendChatAction(self, chat_id: str, action: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"sendChatActivity",
                    "input":{
                        "activity": action,
                        "object_guid": chat_id
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def pin(self, chat_id: str, message_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version": "4", "auth": self.auth, "client": clients.android,
                    "data_enc": self.enc.encrypt(dumps({
                        "action":"Pin",
                        "message_id": message_id,
                        "object_guid": chat_id
                    })),
                    "method": "setPinMessage"
                },url=Robot._getURL(),timeout=5, proxies=self.proxy)))
            except: pass
    def unpin(self, chat_id: str, message_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version": "4", "auth": self.auth, "client": clients.android,
                    "data_enc": self.enc.encrypt(dumps({
                        "action":"Unpin",
                        "message_id": message_id,
                        "object_guid": chat_id
                    })),
                    "method": "setPinMessage"
                },url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def joinGroup(self, link: str) -> dict:
        hashLink = link.split("/")[-1]
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"joinGroup",
                    "input":{
                        "hash_link": hashLink
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def groupPreviewByJoinLink(self, link: str) -> dict:
        hashLink = link.split("/")[-1]
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"groupPreviewByJoinLink",
                    "input":{
                        "hash_link": hashLink
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def leaveGroup(self, chat_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"leaveGroup",
                    "input":{
                        "group_guid": chat_id
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def block(self, chat_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"setBlockUser",
                    "input":{
                        "action": "Block",
                        "user_guid": chat_id
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), proxies=self.proxy).json()["data_enc"]))
            except: pass
    def unblock(self, chat_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"setBlockUser",
                    "input":{
                        "action": "Unblock",
                        "user_guid": chat_id
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def sendPhoto(self, chat_id: str, file, size=[], thumbnail=None, caption=None, message_id=None) -> dict:
        uresponse = Robot._uploadFile(self, file)
        if thumbnail == None: thumbnail = "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"
        elif "." in thumbnail:thumbnail = str(Robot._getThumbInline(open(file,"rb").read() if not "http" in file else get(file).content))
        if size == []: size = Robot._getImageSize(open(file,"rb").read() if not "http" in file else get(file).content)
        file_inline = {
            "dc_id": uresponse[0]["dc_id"],
            "file_id": uresponse[0]["id"],
            "type":"Image",
            "file_name": file.split("/")[-1],
            "size": str(len(get(file).content if "http" in file else open(file,"rb").read())),
            "mime": file.split(".")[-1],
            "access_hash_rec": uresponse[1],
            "width": size[0],
            "height": size[1],
            "thumb_inline": thumbnail
        }
        inData = {
                "method":"sendMessage",
                "input":{
                    "file_inline": file_inline,
                    "object_guid": chat_id,
                    "rnd": f"{randint(100000,999999999)}",
                    "reply_to_message_id": message_id
                },
                "client": clients.web
            }
        if caption != None: inData["input"]["text"] = caption
        data = {"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps(inData))}
        for i in range(4):
            try: return loads(self.enc.decrypt(post(json=data,url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def sendVoice(self, chat_id: str, file, time: str, caption=None, message_id=None) -> dict:
        uresponse = Robot._uploadFile(self, file)
        inData = {
                "method":"sendMessage",
                "input":{
                    "file_inline": {
                        "dc_id": uresponse[0]["dc_id"],
                        "file_id": uresponse[0]["id"],
                        "type":"Voice",
                        "file_name": file.split("/")[-1],
                        "size": str(len(get(file).content if "http" in file else open(file,"rb").read())),
                        "time": time,
                        "mime": file.split(".")[-1],
                        "access_hash_rec": uresponse[1],
                    },
                    "object_guid":chat_id,
                    "rnd":f"{randint(100000,999999999)}",
                    "reply_to_message_id":message_id
                },
                "client": clients.web
            }
        if caption != None: inData["input"]["text"] = caption
        data = {
            "api_version":"5",
            "auth":self.auth,
            "data_enc":self.enc.encrypt(dumps(inData))
        }
        for i in range(4):
            try: return loads(self.enc.decrypt(post(json=data,url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def sendDocument(self, chat_id: str, file, caption=None, message_id=None) -> dict:
        uresponse = Robot._uploadFile(self, file)
        file_id = str(uresponse[0]["id"])
        mime = file.split(".")[-1]
        dc_id = uresponse[0]["dc_id"]
        access_hash_rec = uresponse[1]
        file_name = file.split("/")[-1]
        size = str(len(get(file).content if "http" in file else open(file,"rb").read()))
        inData = {
            "method":"sendMessage",
            "input":{
                "object_guid":chat_id,
                "reply_to_message_id":message_id,
                "rnd":f"{randint(100000,999999999)}",
                "file_inline":{
                    "dc_id":str(dc_id),
                    "file_id":str(file_id),
                    "type":"File",
                    "file_name":file_name,
                    "size":size,
                    "mime":mime,
                    "access_hash_rec":access_hash_rec
                }
            },
            "client": clients.web
        }
        if caption != None: inData["input"]["text"] = caption
        data = {
            "api_version":"5",
            "auth":self.auth,
            "data_enc":self.enc.encrypt(dumps(inData))
        }
        while True:
            try:
                return loads(self.enc.decrypt(loads(post(json=data,url=Robot._getURL(), proxies=self.proxy, timeout=5).text)['data_enc']))
                break
            except: continue
    def sendLocation(self, chat_id: str, location:list, message_id=None) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={
                    "api_version":"4",
                    "auth":self.auth,
                    "client": clients.android,
                    "data_enc":self.enc.encrypt(dumps({
                        "is_mute": False,
                        "object_guid":chat_id,
                        "rnd":f"{randint(100000,999999999)}",
                        "location":{
                            "latitude": location[0],
                            "longitude": location[1]
                        },
                        "reply_to_message_id":message_id
                    })),
                    "method":"sendMessage"
                },url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
                break
            except: pass
    def getChannelMembers(self, channel_guid: str, text=None, start_id=None) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={
                    "api_version":"4",
                    "auth":self.auth,
                    "client": clients.android,
                    "data_enc":self.enc.encrypt(dumps({
                        "channel_guid": channel_guid,
                        "search_text": text,
                        "start_id": start_id
                    })),
                    "method":"getChannelAllMembers"
                },url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except KeyError:
                pass
                if i == 3: return None
    def getChatsUpdate(self) -> dict:
        time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getChatsUpdates",
                    "input":{
                        "state":time_stamp,
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json().get("data_enc"))).get("data").get("chats")
            except: pass
    def getChatUpdate(self, chat_id: str) -> dict:
        time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getMessagesUpdates",
                    "input":{
                        "object_guid":chat_id,
                        "state":time_stamp
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json().get("data_enc"))).get("data").get("updated_messages")
            except: pass
    def myStickerSet(self) -> dict:
        time_stamp = str(round(datetime.datetime.today().timestamp()) - 200)
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getMyStickerSets",
                    "input":{},
                    "client": clients.web
                }))},url=Robot._getURL(),timeout=5, proxies=self.proxy).json().get("data_enc"))).get("data")
            except: pass
    def uploadAvatar(self,myguid,main,thumbnail=None) -> dict:
        mainID = str(Robot._uploadFile(self, main)[0]["id"])
        thumbnailID = str(Robot._uploadFile(self, thumbnail or main)[0]["id"])
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"uploadAvatar",
                    "input":{
                        "object_guid":myguid,
                        "thumbnail_file_id":thumbnailID,
                        "main_file_id":mainID
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def startVoiceChat(self, chat_id: str, on="Group") -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":f"create{on}VoiceChat",
                    "input":{
                        f"{on.lower()}_guid":chat_id,
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))	
            except: pass
    def editVoiceChat(self, chat_id: str,voice_chat_id: str, title: str, on="Group") -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":f"set{on}VoiceChatSetting",
                    "input":{
                        f"{on.lower()}_guid":chat_id,
                        "voice_chat_id" : voice_chat_id,
                        "title" : title ,
                        "updated_parameters": ["title"]
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def finishVoiceChat(self, chat_id: str, voice_chat_id: str, on="Group") -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":f"discard{on}VoiceChat",
                    "input":{
                        f"{on.lower()}_guid":chat_id,
                        "voice_chat_id" : voice_chat_id,
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), proxies=self.proxy, timeout=5).json()["data_enc"]))
            except: pass
    def getAvatars(self,myguid) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getAvatars",
                    "input":{
                        "object_guid":myguid,
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), proxies=self.proxy, timeout=5).json().get("data_enc"))).get("data").get("avatars")
            except: pass
    def deleteAvatar(self,myguid: str, avatar_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"deleteAvatar",
                    "input":{
                        "object_guid":myguid,
                        "avatar_id":avatar_id
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def download(self, dl="message",save=False,**kwargs):
        result = b""
        if dl == "message":
            message = kwargs["message"]
            if type(message) != dict:
                message = Robot(self.app_name, auth=self.auth, displayWelcome=False).getMessagesInfo(kwargs["chat_id"], [str(message)])[0]
            fileID = str(message["file_inline"]["file_id"])
            size = message["file_inline"]["size"]
            dc_id = str(message["file_inline"]["dc_id"])
            accessHashRec = message["file_inline"]["access_hash_rec"]
            filename = message["file_inline"]["file_name"]
        else :
            fileID = str(kwargs.get("fileID"))
            size = kwargs.get("size")
            dc_id = str(kwargs.get("dc_id"))
            accessHashRec = kwargs.get("accessHashRec")
        header = {
            'auth':self.auth,
            'file-id':fileID,
            'access-hash-rec':accessHashRec
        }
        server = "https://messenger"+dc_id+".iranlms.ir/GetFile.ashx"
        if size <= 131072:
            header["start-index"], header["last-index"] = "0",str(size)
            while True:
                try:
                    result += get(url=server,headers=header).content
                    break
                except Exception as e:
                    print (e)
                    continue
        else:
            lastnow = 0
            lastlast = 131072
            while True:
                try:
                    if lastnow <= 131072:
                        header["start-index"], header["last-index"] = "0", str(size)
                        result += get(url=server,headers=header).content
                    else:
                        for i in range(0,size,131072):
                            header["start-index"], header["last-index"] = str(i), str(i+131072 if i+131072 <= size else size)
                            result += get(url=server,headers=header).content
                    break
                except Exception as e:
                    print(e)
        if save:
            with open(kwargs.get("saveAs") or f"{filename}","wb") as file: file.write(result)
        else:
            return result
    def editProfile(self, **kwargs) -> dict:
        if "username" in list(kwargs.keys()):
            for i in range(4):
                try:
                    return loads(self.enc.decrypt(post(json={
                        "api_version":"4",
                        "auth":self.auth,
                        "client": clients.android,
                        "data_enc":self.enc.encrypt(dumps({
                            "username": kwargs.get("username"),
                            "updated_parameters":["username"]
                        })),
                        "method":"updateUsername"
                    },url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
                    kwargs = kwargs.pop("username")
                except: pass
        if len(list(kwargs.keys())) > 0:
            return loads(self.enc.decrypt(post(json={
                "api_version":"4",
                "auth":self.auth,
                "client": clients.android,
                "data_enc":self.enc.encrypt(dumps({
                    "first_name": kwargs.get("first_name"),
                    "last_name": kwargs.get("last_name"),
                    "bio": kwargs.get("bio"),
                    "updated_parameters":list(kwargs.keys())
                })),
                "method":"updateProfile"
            },url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
    def sendGIF(self, chat_id: str, file, width, height, thumbnail="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", caption=None, message_id=None) -> dict:
        uresponse = Robot._uploadFile(self, file)
        file_id = str(uresponse[0]["id"])
        mime = file.split(".")[-1]
        dc_id = uresponse[0]["dc_id"]
        access_hash_rec = uresponse[1]
        file_name = file.split("/")[-1]
        size = str(len(get(file).content if "http" in file else open(file,"rb").read()))
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={
                    "api_version":"4",
                    "auth":self.auth,
                    "client": clients.android,
                    "data_enc":self.enc.encrypt(dumps({
                        "object_guid": chat_id,
                        "is_mute": False,
                        "rnd": randint(100000,999999999),
                        "file_inline": {
                            "access_hash_rec": access_hash_rec,
                            "dc_id": dc_id,
                            "file_id": file_id,
                            "auto_play": False,
                            "file_name": file_name,
                            "width": width,
                            "height": height,
                            "mime": mime,
                            "size": size,
                            "thumb_inline": thumbnail,
                            "type": "Gif"
                        },
                        "text": caption,
                        "reply_to_message_id":message_id
                    })),
                    "method":"sendMessage"
                },url=Robot._getURL(), timeout=5).json()["data_enc"]))
            except: pass
    def sendPoll(self, **kwargs) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={
                    "api_version":"4",
                    "auth":self.auth,
                    "client": clients.android,
                    "data_enc":self.enc.encrypt(dumps(kwargs)),
                    "method": "createPoll"
                }, url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def votePoll(self, poll_id: str, option_index) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={
                    "api_version":"4",
                    "auth":self.auth,
                    "client": clients.android,
                    "data_enc":self.enc.encrypt(dumps({
                        "poll_id": poll_id,
                        "selection_index": option_index
                    })),
                    "method": "votePoll"
                }, url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def deleteChatHistory(self, chat_id: str, lastMessageId) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={
                    "api_version":"4",
                    "auth":self.auth,
                    "client": clients.android,
                    "data_enc":self.enc.encrypt(dumps({
                        "object_guid": chat_id,
                        "last_message_id": lastMessageId
                    })),
                    "method": "deleteChatHistory"
                }, url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def search(self, text: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={
                    "api_version":"4",
                    "auth":self.auth,
                    "client": clients.android,
                    "data_enc":self.enc.encrypt(dumps({
                        "search_text": text
                    })),
                    "method": "searchGlobalObjects"
                }, url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def getPollStatus(self, poll_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getPollStatus",
                    "input":{
                        "poll_id":poll_id,
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))
            except: pass
    def getPollOptionVoters(self, poll_id: str, option_index: str, start_id=None) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getPollOptionVoters",
                    "input":{
                        "poll_id":poll_id,
                        "selection_index": option_index,
                        "start_id": start_id
                    },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def getMe(self):
        return Robot(self.app_name, auth=self.auth, displayWelcome=False).getUserInfo(loads(open(self.app_name+".json","rt").read()).get("data").get("user").get("user_guid"))
    def reportObject(self, user_guid: str,  mode: str, message_id=None) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={
                    "api_version":"4",
                    "auth": self.auth,
                    "client": clients.android,
                    "data_enc":self.enc.encrypt(dumps({
                        "object_guid": user_guid,
                        "report_description": mode, 
                        'report_type_object': 'Object', 
                        'report_type': 100,
                        'meesage_id': message_id
                    })),
                    "method":"reportObject"
                },url=Robot._getURL(), proxies=self.proxy).json()["data_enc"]))
                break
            except: pass
    def auths() -> str:
        auths, choices = "", [*"abcdefghijklmnopqrstuvwxyz"]
        for i in range(32): auths += choice(choices)
        return auths
    def getServiceInfo (self, guid: str) -> dict :
        self.guid = guid
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method": "getServiceInfo",
                    "input": {
                        "service_guid": self.guid
                        },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def getPrivacySetting (self) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                   "method": "getPrivacySetting",
                   "input": {},
                    "client": clients.web
                }))},url=Robot._getURL(), proxies=self.proxy, timeout=5).json()["data_enc"]))["data"]
            except: pass
    def setSetting (self, show_my_last_online=None, show_my_phone_number=None, show_my_profile_photo=None, link_forward_message=None, can_join_chat_by=None) -> dict:
        '''for type setSetting : Nobody, MyContacts, Everybody  (bot.setSetting(show_my_last_online='Nobody'))'''
        # Nobody, MyContacts, Everybody
        for i in range(4):
            if show_my_phone_number != None :
                try:
                    return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method": "setSetting",
                    "input":
                        {"settings": {"show_my_phone_number": show_my_phone_number},
                        "update_parameters": ["show_my_phone_number"]},
                        "client": clients.web
                    }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
                except: pass
            elif show_my_last_online != None:
                try:
                    return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method": "setSetting",
                    "input":
                        {"settings": {"show_my_last_online": show_my_last_online},
                        "update_parameters": ["show_my_last_online"]},
                        "client": clients.web
                    }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
                except: pass
            elif show_my_profile_photo != None:
                try:
                    return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method": "setSetting",
                    "input":
                        {"settings": {"show_my_profile_photo": show_my_profile_photo},
                        "update_parameters": ["show_my_profile_photo"]},
                        "client": clients.web
                    }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
                except: pass
            elif link_forward_message != None:
                try:
                    return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method": "setSetting",
                    "input":
                        {"settings": {"link_forward_message": link_forward_message},
                        "update_parameters": ["link_forward_message"]},
                        "client": clients.web
                    }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
                except: pass
            elif can_join_chat_by != None:
                try:
                    return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method": "setSetting",
                    "input":{
                        "settings": {"can_join_chat_by": can_join_chat_by},
                        "update_parameters": ["can_join_chat_by"]
                        },
                        "client": clients.web
                    }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
                except: pass
    def getMySessions(self) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getMySessions",
                    "input":{},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def getTwoPasscodeStatus(self) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                   "method":"getTwoPasscodeStatus",
                   "input":{},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def checkTwoStepPasscode(self, password: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"checkTwoStepPasscode",
                    "input":{"password":password},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def changePassword(self, password: str, new_password: str, new_hint: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                      "method":"changePassword",
                        "input":{
                           "password":password,
                           "new_password":new_password,
                           "new_hint":new_hint
                           },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def turnOffTwoStep(self, password: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"turnOffTwoStep",
                    "input":{"password":password},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def setupTwoStepVerification(self, password: str, hint: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                   "method":"setupTwoStepVerification",
                    "input":{"password":password,"hint":hint},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def getBlockUsers(self) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                  "method":"getBlockedUsers","input":{},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def requestRecoveryEmail(self, password: str, recovery_email: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                  "method":"requestRecoveryEmail",
                  "input":{
                      "password":password,
                      "recovery_email":recovery_email
                      },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def verifyRecoveryEmail(self, password: str, code: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                  "method":"verifyRecoveryEmail",
                   "input":{
                       "password":password,
                       "code":code
                       },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def setActionChat(self, object_guid: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                  "method":"setActionChat",
                  "input":{
                      "object_guid":object_guid,
                      "action":"Mute"
                      },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def GroupPreviewByJoinLink(self, hash_link: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                 "method":"groupPreviewByJoinLink",
                  "input":{
                      "hash_link":hash_link
                      },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def joinChannelAction(self, guid: str) -> dict:
        for i in range(3):
            try: return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({"method":"joinChannelAction","input":{"channel_guid":guid,"action":"Join"},"client": clients.web}))},url=Robot._getURL(), timeout=5, proxies=self.proxy)))
            except: pass
    def getObjectByUsername(self, username: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                 "method":"getObjectByUsername",
                  "input":{
                      "username":username
                      },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def leaveChannel(self, guid: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                "method":"joinChannelAction",
                 "input":{
                     "channel_guid":guid,
                     "action":"Leave"
                     },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def createChannel(self, title: str, description: str, channel_type: str) -> dict:
        '''channel_type is: Public or Private'''
        # Public , Privte
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"addChannel",
                    "input":{
                        "title":title,
                        "description":description,
                        "channel_type":channel_type},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5).json()["data_enc"]))["data"]
            except: pass
    def editChannnelInfo(self, guid: str, sign_messages=None, title=None, description=None) -> dict:
        for i in range(4):
            if sign_messages != None:
                try:
                    return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"editChannelInfo",
                    "input":{
                        "channel_guid":guid,
                        "sign_messages":sign_messages,
                        "updated_parameters":["sign_messages"]
                        },
                        "client": clients.web
                    }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
                except: pass
            elif title != None:
                try:
                    return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                        "method":"editChannelInfo",
                        "input":{
                            "channel_guid":guid,
                            "title":title,
                            "description":description,
                            "updated_parameters":["title","description"]
                            },
                        "client": clients.web
                    }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
                except: pass
    def setChannelLink(self, guid: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                 "method":"setChannelLink",
                  "input":{
                      "channel_guid":guid
                      },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def checkChannelUsername(self, username: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                 "method":"checkChannelUsername",
                 "input":{
                     "username":username
                     },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def updateChannelUsername(self, guid: str, username: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"updateChannelUsername",
                    "input":{
                        "channel_guid":guid,
                        "username":username
                        },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def joinGroupVoiceChat(self, channel_guid: str, your_guid: str, voice_chat_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"joinGroupVoiceChat",
                    "input":{
                        "chat_guid":channel_guid,
                        "voice_chat_id":voice_chat_id,
                        "sdp_offer_data":"""v=0\r\no=- 7025254686977085379 2 IN IP4 127.0.0.1\r\ns=-\r\nt=0 0\r\na=group:BUNDLE 0\r\na=extmap-allow-mixed\r\na=msid-semantic: WMS LjIerKYwibTOvR0Ewwk1PBsYYxTInaoXObBE\r\nm=audio 9 UDP/TLS/RTP/SAVPF 111 63 103 104 9 0 8 106 105 13 110 112 113 126\r\nc=IN IP4 0.0.0.0\r\na=rtcp:9 IN IP4 0.0.0.0\r\na=ice-ufrag:6Hy7\r\na=ice-pwd:pyrxfUF+roBFRHDy6qgiKSAp\r\na=ice-options:trickle\r\na=fingerprint:sha-256 8C:90:E9:0C:E7:A4:79:7E:BF:78:81:ED:A7:19:82:64:71:F7:21:AB:43:4F:4B:3A:4C:EB:B5:3C:6A:01:CB:13\r\na=setup:actpass\r\na=mid:0\r\na=extmap:1 urn:ietf:params:rtp-hdrext:ssrc-audio-level\r\na=extmap:2 http://www.webrtc.org/experiments/rtp-hdrext/abs-send-time\r\na=extmap:3 http://www.ietf.org/id/draft-holmer-rmcat-transport-wide-cc-extensions-01\r\na=extmap:4 urn:ietf:params:rtp-hdrext:sdes:mid\r\na=sendrecv\r\na=msid:LjIerKYwibTOvR0Ewwk1PBsYYxTInaoXObBE 00f6113c-f01a-447a-a72e-c989684b627a\r\na=rtcp-mux\r\na=rtpmap:111 opus/48000/2\r\na=rtcp-fb:111 
transport-cc\r\na=fmtp:111 minptime=10;useinbandfec=1\r\na=rtpmap:63 red/48000/2\r\na=fmtp:63 111/111\r\na=rtpmap:103 ISAC/16000\r\na=rtpmap:104 ISAC/32000\r\na=rtpmap:9 G722/8000\r\na=rtpmap:0 PCMU/8000\r\na=rtpmap:8 PCMA/8000\r\na=rtpmap:106 CN/32000\r\na=rtpmap:105 CN/16000\r\na=rtpmap:13 CN/8000\r\na=rtpmap:110 telephone-event/48000\r\na=rtpmap:112 telephone-event/32000\r\na=rtpmap:113 telephone-event/16000\r\na=rtpmap:126 telephone-event/8000\r\na=ssrc:1614457217 cname:lYBnCNdQcW/DEUj9\r\na=ssrc:1614457217 msid:LjIerKYwibTOvR0Ewwk1PBsYYxTInaoXObBE 00f6113c-f01a-447a-a72e-c989684b627a\r\n""",
                        "self_object_guid":your_guid},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def getDisplayAsInGroupVoiceChat(self, guid: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                   "method":"getDisplayAsInGroupVoiceChat",
                    "input":{
                        "chat_guid":guid
                        },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def setActionChat(self, guid: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"setActionChat",
                    "input":{
                        "object_guid":guid,
                        "action":"Unmute"
                        },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def leaveGroupVoiceChat(self, chat_guid: str, voice_chat_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"leaveGroupVoiceChat",
                    "input":{
                        "chat_guid":chat_guid,
                        "voice_chat_id":voice_chat_id
                        },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def setGroupVoiceChatSetting(self, chat_guid: str, voice_chat_id: str, title: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"setGroupVoiceChatSetting",
                    "input":{
                        "chat_guid":chat_guid,
                        "voice_chat_id":voice_chat_id,
                        "title":title,
                        "updated_parameters":["title"]
                        },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def discardGroupVoiceChat(self, chat_guid: str, voice_chat_id: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"discardGroupVoiceChat",
                    "input":{
                        "chat_guid":chat_guid,
                        "voice_chat_id":voice_chat_id
                        },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def removeChannel(self, guid: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"removeChannel",
                    "input":{
                        "channel_guid":guid
                        },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def editGroupInfo(self, guid: str, title=None, description=None) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                   "method":"editGroupInfo",
                   "input":{
                       "group_guid":guid,
                       "title":title,
                       "description":description,
                       "updated_parameters":["title","description"]},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def setGroupDefaultAccess(self, guid: str, ViewMembers=None, ViewAdmins=None,SendMessages =None, AddMember=None) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                   "method":"setGroupDefaultAccess",
                   "input":{
                       "group_guid":guid,
                       "group_guid":guid,
                       "access_list":[["ViewMembers" if ViewMembers != None else None], ["ViewAdmins" if ViewAdmins != None else None], ["SendMessages" if SendMessages != None else None], ["AddMember" if AddMember != None else None]]},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def appUrl (self, app_url: str) -> dict:
        '''for open link on rubika and info link'''
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                   "method":"getLinkFromAppUrl",
                   "input":{
                       "app_url": app_url
                       },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def sendChatActivity(self, target_guid: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"sendChatActivity",
                    "input":{
                        "object_guid":target_guid,
                        "activity":"rubx-lib"
                        },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def addAddressBook(self, phone: str, first_name=None, last_name=None) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"addAddressBook",
                    "input":{
                        "phone":phone,
                        "first_name":first_name,
                        "last_name":last_name
                        },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def searchGloblMessages(self, text: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"searchGlobalMessages",
                    "input":{
                        "search_text":text,
                        "type":"Text",
                        "start_id":0},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def getContactsLastOnline(self, user_guids: list) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getContactsLastOnline",
                    "input":{
                        "user_guids":user_guids},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def getAbsObjects(self, user_guids: list) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                    "method":"getAbsObjects",
                    "input":{
                        "objects_guids":user_guids},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def getChannelInfo(self, guid: str) -> dict:
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                  "method":"getChannelInfo",
                  "input":{
                      "channel_guid": guid
                      },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def getMessagesUpdates(self, guid: str, state='0') -> dict:
        '''guid : chat_id for get messages , state : state or time stamp for get messages'''
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                  "method":"getMessagesUpdates",
                  "input":{
                      "object_guid": guid,
                      "state":state
                      },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def getBannedGroupMembers(self, guid: str, state=None) -> dict :
        for i in range(4):
            try: return loads(self.enc.decrypt(post(json={'api_version': '4', 'auth': self.auth, 'client': clients.android, 'method': 'getBannedGroupMembers', 'data_enc': self.enc.encrypt(dumps({'group_guid': guid}))}, url=Robot._getURL(), timeout=5, proxies=self.proxy).json()['data_enc']))
            except: pass
    def getGroupMentionList(self, guid: str) -> dict :
        for i in range(4):
            try:
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                  "method":"getGroupMentionList",
                  "input":{
                      "group_guid": guid,
                      "search_mention":'null'
                      },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def sendMention(self, object_guid: str, text: str, user_guids: list, modes: list, message_id=None) -> dict :
        """ send Mention for tag user:  bot.sendMention('group-GUID', text='hello from send metion rubx library', user_guids=['guid'], modes=['User', 'Channel'], message_id='28333444') """
        for i in range(4):
            try:
                data: list = []
                if len(user_guids) >= 1 :
                    for i in range(len(user_guids)) : data.append({"type":"MentionText", "mention_text_object_guid": user_guids[i], "from_index":0, "length": 12, "mention_text_object_type": modes[i]})
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                  "method":"sendMessage",
                  "input":{
                      "object_guid": object_guid,
                      "rnd": str(randint(100000,999999999)),
                      "text": text,
                      'reply_to_message_id': message_id,
                      "metadata":{
                          "meta_data_parts": data
                          }
                      },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except: pass
    def getContactsUpdates(self, state='0') -> dict :
        for i in range(4):
            try :
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                  "method":"getContactsUpdates",
                  "input":{
                      "state": state
                      },
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except : pass
    def addFolder(self, name: str, include_chat_types: list, exclude_chat_types=None, include_object_guids=None, exclude_object_guids=None) -> dict :
        """ name = name folder, include_chat_types = ['Contacts', ...], ... """
        for i in range(4) :
            try :
                return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
                  "method":"addFolder",
                  "input":{
                      "name": name,
                      "include_chat_types": include_chat_types,
                      "exclude_chat_types": exclude_chat_types,
                      "include_object_guids": include_object_guids,
                      "exclude_object_guids": exclude_object_guids,
                      "is_add_to_top":'true'},
                    "client": clients.web
                }))},url=Robot._getURL(), timeout=5, proxies=self.proxy).json()["data_enc"]))["data"]
            except : pass
class Socket:
    data: dict = {"error":[],"messages":[]}
    def __init__(self, auth) -> None :
        self.auth = auth; self.enc = encryption(auth)
    def on_open(self, ws, api_version='4') -> None :
        def handShake(*args):
            ws.send(dumps({
                "api_version": api_version,
                "auth": self.auth,
                "data_enc": "",
                "method": "handShake"}))
        import _thread; _thread.start_new_thread(handShake, ())
    def on_error(self, error) -> None : Socket.data["error"].append(error)
    def on_message(self, message) -> None :
        try: parsedMessage = loads(message); Socket.data["messages"].append({"type": parsedMessage["type"], "data": loads(self.enc.decrypt(parsedMessage["data_enc"]))})
        except KeyError: pass
    def on_close(self, code, msg) -> None : return {"code": code, "message": msg}
    def handle(self, OnOpen=None, OnError=None, OnMessage=None, OnClose=None, forEver=True) -> None :
        from websocket import WebSocketApp
        ws = WebSocketApp(
            "wss://jsocket3.iranlms.ir:80",
            on_open=OnOpen or Socket(self.auth).on_open,
            on_message=OnMessage or Socket(self.auth).on_message,
            on_error=OnError or Socket(self.auth).on_error,
            on_close=OnClose or Socket(self.auth).on_close)
        if forEver : ws.run_forever()

class Set :
    def __init__(auth: str, mode: str, password=None, newpassword=None, hint=None, newhint=None) -> None :
        '''set password to account: modes:  1, 2, 3  and  1 = changePassword or new password  and  2 = createPassword,  and 3 = off password :)'''
        bot = Robot(auth=auth)
        if mode == '1' : bot.getTwoPasscodeStatus(); bot.checkTwoStepPasscode(str(password)); bot.changePassword(str(password), str(newpassword), str(newhint))
        elif mode == '2' : bot.setupTwoStepVerification(str(password), str(hint))
        else : bot.turnOffTwoStep(str(password))
