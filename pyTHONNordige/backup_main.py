import requests
import json
import pandas as pd
import nordigen

token = '653a453ddd99a254c52157c04bbfcaa120700b6c628f04d130294a208e45632f3dcf9ead94708df360ce40f1d307a7210bf7a6e296f5a909fa805f895c6e022a'
data = {'secret_id': '00d2f1c8-41bc-49e3-848a-c1a44341ce08',
        'secret_key': token
        }

API_ENDPOINT_TOKEN_NEW = 'https://ob.nordigen.com/api/v2/token/new/'
API_ENDPOINT_TOKEN_REFRESH = 'https://ob.nordigen.com/api/v2/token/refresh/'
r = requests.post(url=API_ENDPOINT_TOKEN_NEW, data=data)
print(r.status_code)
if r.status_code == 200:
        # extracting response text
        pastebin_url = r.text
        print("The pastebin URL is:%s" % pastebin_url)

        data1 = {'accept': 'application/json',
                'X-CSRFToken': token
                }
        INSTITUTIONS_ENDPOINT = "https://ob.nordigen.com/api/v2/institutions/?country=IT"
        r = requests.get(INSTITUTIONS_ENDPOINT, data1)
        if r.status_code == 200:
                df = pd.DataFrame.from_dict(pd.json_normalize(r.json(), max_level=10))
                print(df)
        elif r.status_code == 401:
                data2 = {'accept': 'application/json',
                         'Content-Type': 'application/json',
                         'X-CSRFToken': token
                         }
                r = requests.post(url=API_ENDPOINT_TOKEN_REFRESH, data=data2)
                print("refresh status code= ", r.status_code)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/