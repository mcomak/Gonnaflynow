import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime, timezone

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")

url = "https://www.frankfurt-airport.com/en/_jcr_content.flights.json/filter"

querystring = {"perpage":"50","lang":"en-GB","page":"1","flighttype":"departures","time":f"{current_time}"}

payload = ""
headers = {
    "cookie": "gig_bootstrap_3_YkifhkvEfiaW1unZitDqKPsSGus6ecsn6ILfyVQ3pbN2XZhH-2g5dlXiAYyEdejc=accounts_ver4; _SI_VID_1.a9a2bd8790000129361bd46e=4d5e22c80c57b5304ea1a4eb; gig_canary=false; gig_canary_ver=13826-3-28075320; AL_SESS-S=AQjFAoKjhoDN3DLz1zi1l9bKWPJXfOuMjqsH4tUTf9xqjG9TI^!YrprBdtYcHSaPTfHjJ; _SI_DID_1.a9a2bd8790000129361bd46e=fd1fc64a-e1fc-3a8e-9075-f92cc329b7ea; _SI_SID_1.a9a2bd8790000129361bd46e=2664e3751087b65f10cf974e.1684521751537.75311",
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

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)


r = requests.get(url, headers=headers, params=querystring)
data = r.json()
res = data['data']
df = pd.json_normalize(res)


conn = psycopg2.connect(database="sky", user="train", password="Ankara06", host="localhost", port="5432")
cur = conn.cursor()


create_table_query = """
    CREATE TABLE IF NOT EXISTS frankfurt_temp (
        ac TEXT,
        lu TIMESTAMP WITH TIME ZONE,
        typ TEXT,
        al TEXT,
        fnr TEXT,
        terminal TEXT,
        halle TEXT,
        schalter TEXT,
        s BOOLEAN,
        iata TEXT,
        sched TIMESTAMP WITH TIME ZONE,
        reg TEXT,
        apname TEXT,
        id TEXT,
        gate TEXT,
        lang TEXT,
        alname TEXT,
        flstatus INTEGER,
        status TEXT,
        schedarr TIMESTAMP WITH TIME ZONE,
        cs TEXT,
        duration TEXT,
        stops FLOAT,
        rouname TEXT,
        rou TEXT,
        esti TIMESTAMP WITH TIME ZONE
    )
"""
cur.execute(create_table_query)
conn.commit()


engine = create_engine('postgresql://train:Ankara06@localhost:5432/sky')
df.to_sql('frankfurt_temp', engine, if_exists='replace', index=False)


create_table_query = "CREATE TABLE IF NOT EXISTS frankfurt (LIKE frankfurt_temp INCLUDING ALL);"
cur.execute(create_table_query)
conn.commit()


insert_query = """
    INSERT INTO frankfurt (ac, lu, typ, al, fnr, terminal, halle, schalter, s, iata, sched, reg, apname, id, gate, lang, alname, flstatus, status, "schedArr", cs, duration, stops, rouname, rou, esti)
    SELECT ac, lu, typ, al, fnr, terminal, halle, schalter, s, iata, sched, reg, apname, id, gate, lang, alname, flstatus, status, "schedArr", cs, duration, stops, rouname, rou, CAST('2023-05-19 10:30:00' AS timestamp with time zone) as esti
    FROM frankfurt_temp
    WHERE NOT EXISTS (
        SELECT 1 FROM frankfurt
        WHERE frankfurt.id = frankfurt_temp.id AND frankfurt.status = frankfurt_temp.status
    )
"""


cur.execute(insert_query)
conn.commit()


cur.close()
conn.close()
