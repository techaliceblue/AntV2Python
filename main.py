import websocket
import _thread
import time
import rel
from modules import *

client_key = 'DEMOPN'
api_key='2IpA4Tn6SSV1Jja4nmKvP8aYDMIGsAQHhck5CPg108WJP292kGuJ9rZRYhgVyevL8f6kjfhGBEHpkQ4iblcTk5qifFfskmtEhoRuQW0Iui9QMkbPfLI709GzzuVfWWTA'



session_request=get_session(client_key,api_key)
if 'loginType' in session_request and session_request['loginType'] == None:
    print(session_request['emsg'])
else:
    session_id=session_request['sessionID']
    invalid_session=invalid_sess(client_key, session_id)
    if invalid_session['stat'] == 'Ok':
        print("Invalid Session request :",invalid_session['stat'])
        create_session=createSession(client_key, session_id)

        if create_session['stat'] == 'Ok':
            print("Create Session request  :",create_session['stat'])
            sha256_encryption1 = hashlib.sha256(session_id.encode('utf-8')).hexdigest()
            sha256_encryption2 = hashlib.sha256(sha256_encryption1.encode('utf-8')).hexdigest()

            def on_message(ws, message):
                print(message)
                data=json.loads(message)
                if 's' in data and data['s'] == 'OK':
                    channel = 'BSE|1#NSE|26017#NSE|26040#NSE|26009#NSE|26000#MCX|232615#MCX|235517#MCX|233042#MCX|234633#MCX|240085#NSE|5435#NSE|20182#NSE|212#NSE|11439#NSE|2328#NSE|772#NSE|14838#NSE|14428#NSE|1327#NSE|7229#NSE|1363#NSE|14366#NSE|1660#NSE|11763#NSE|10576#NSE|14977#NSE|15032#NSE|2885#NSE|3045#NSE|5948#NSE|2107#NSE|3426#NSE|11536#NSE|11915#NSE|5097';
                    data = {
                        "k": channel,
                        "t": 't',
                        "m":"compact_marketdata"
                    }
                    ws.send(json.dumps(data))

            def on_error(ws, error):
                print(error)

            def on_close(ws, close_status_code, close_msg):
                print("### closed ###")

            def on_open(ws):
                print("Opened connection")
                initCon = {
                    "susertoken": sha256_encryption2,
                    "t": "c",
                    "actid": client_key + "_API",
                    "uid": client_key + "_API",
                    "source": "API"
                }
                ws.send(json.dumps(initCon))


            if __name__ == "__main__":
                websocket.enableTrace(False)
                ws = websocket.WebSocketApp("wss://ws1.aliceblueonline.com/NorenWS/",
                                          on_open=on_open,
                                          on_message=on_message,
                                          on_error=on_error,
                                          on_close=on_close)

                ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
                rel.signal(2, rel.abort)  # Keyboard Interrupt
                rel.dispatch()