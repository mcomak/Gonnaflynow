import requests
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

url = "https://www.frankfurt-airport.com/en/_jcr_content.flights.json/filter"

querystring = {"perpage":"10","lang":"en-GB","page":"1","flighttype":"departures"}

payload = ""
headers = {
    "cookie": "gig_bootstrap_3_YkifhkvEfiaW1unZitDqKPsSGus6ecsn6ILfyVQ3pbN2XZhH-2g5dlXiAYyEdejc=accounts_ver4; _SI_VID_1.a9a2bd8790000129361bd46e=d4a1a24ea7dee6361422943b; gig_canary=false; _SI_DID_1.a9a2bd8790000129361bd46e=e4e76f5b-e1e3-32fa-aa19-763610c3b0ce; gig_canary_ver=13826-3-28063530; AL_SESS-S=AapYPn2eNiYp66mlz5S6KfyRaynuHLwYN6HKUBnGvY7ozTNPVedR1w1DFrXhX^!NiV3Ve; _SI_SID_1.a9a2bd8790000129361bd46e=bb4c40831d53085f45457870.1683813911561.789086",
    "authority": "www.frankfurt-airport.com",
    "accept": "*/*",
    "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
    "referer": "https://www.frankfurt-airport.com/en/flights-and-transfer/departures.html",
    "sec-ch-ua": "^\^Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}



r = requests.request("GET", url, data=payload, headers=headers, params=querystring)



data = r.json()
res = []
for p in data['data']:
    res.append(p)

df = pd.json_normalize(res)
print(df.head(10))