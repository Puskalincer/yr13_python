import requests
import json
import pprint





res = requests.get('https://api-steampowered-com.translate.goog/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json&_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&_x_tr_pto=wapp')
response = json.loads(res.text)
pprint.pprint(response)