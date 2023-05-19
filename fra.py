import requests
import pandas as pd
import psycopg2

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# url = "https://www.frankfurt-airport.com/en/_jcr_content.flights.json/filter"
#
# querystring = {"perpage":"10","lang":"en-GB","page":"1","flighttype":"departures"}
#
# payload = ""
# headers = {
#     "cookie": "gig_bootstrap_3_YkifhkvEfiaW1unZitDqKPsSGus6ecsn6ILfyVQ3pbN2XZhH-2g5dlXiAYyEdejc=accounts_ver4; _SI_VID_1.a9a2bd8790000129361bd46e=d4a1a24ea7dee6361422943b; gig_canary=false; _SI_DID_1.a9a2bd8790000129361bd46e=e4e76f5b-e1e3-32fa-aa19-763610c3b0ce; gig_canary_ver=13826-3-28063530; AL_SESS-S=AapYPn2eNiYp66mlz5S6KfyRaynuHLwYN6HKUBnGvY7ozTNPVedR1w1DFrXhX^!NiV3Ve; _SI_SID_1.a9a2bd8790000129361bd46e=bb4c40831d53085f45457870.1683813911561.789086",
#     "authority": "www.frankfurt-airport.com",
#     "accept": "*/*",
#     "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
#     "referer": "https://www.frankfurt-airport.com/en/flights-and-transfer/departures.html",
#     "sec-ch-ua": "^\^Google",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "^\^Windows^^",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
# }

url = "https://www.frankfurt-airport.com/en/_jcr_content.flights.json/filter"

querystring = {"perpage":"50","lang":"en-GB","page":"1","flighttype":"departures"}

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



r = requests.request("GET", url, data=payload, headers=headers, params=querystring)


data = r.json()
res = []
for p in data['data']:
    res.append(p)

df = pd.json_normalize(res)


# Connect to the PostgreSQL database
conn = psycopg2.connect(database="sky", user="train", password="Ankara06", host="localhost", port="5432")
cur = conn.cursor()

# Define the schema for the table, with the IF NOT EXISTS clause
# table_schema = "CREATE TABLE IF NOT EXISTS frankfurt (ac TEXT, lu TIMESTAMP WITH TIME ZONE, typ TEXT, al TEXT, fnr TEXT, terminal TEXT, halle TEXT, schalter TEXT, s BOOLEAN, iata TEXT, sched TIMESTAMP WITH TIME ZONE, reg TEXT, apname TEXT, id TEXT, gate TEXT, lang TEXT, alname TEXT, flstatus INTEGER, status TEXT, schedArr TIMESTAMP WITH TIME ZONE, cs TEXT, duration TEXT, stops FLOAT, rouname TEXT, rou TEXT)"

# # Execute the schema definition
# cur.execute(table_schema)

cur.execute("CREATE TABLE IF NOT EXISTS frankfurt_temp (ac TEXT, lu TIMESTAMP WITH TIME ZONE, typ TEXT, al TEXT, fnr TEXT, terminal TEXT, halle TEXT, schalter TEXT, s BOOLEAN, iata TEXT, sched TIMESTAMP WITH TIME ZONE, reg TEXT, apname TEXT, id TEXT, gate TEXT, lang TEXT, alname TEXT, flstatus INTEGER, status TEXT, schedarr TIMESTAMP WITH TIME ZONE, cs TEXT, duration TEXT, stops FLOAT, rouname TEXT, rou TEXT, esti TIMESTAMP WITH TIME ZONE)"
)

# Commit the changes to the database
conn.commit()


# Insert the dataframe into the PostgreSQL database
from sqlalchemy import create_engine

engine = create_engine('postgresql://train:Ankara06@localhost:5432/sky')
df.to_sql('frankfurt_temp', engine, if_exists='replace', index=False)

# Rollback any unfinished transactions
conn.rollback()


insert_query = "CREATE TABLE IF NOT EXISTS frankfurt (LIKE frankfurt_temp INCLUDING ALL);"

insert_query2 = """INSERT INTO frankfurt
SELECT *
FROM frankfurt_temp
WHERE NOT EXISTS (
    SELECT 1 FROM frankfurt
    WHERE 
      frankfurt.id = frankfurt_temp.id
      AND frankfurt.status = frankfurt_temp.status
);"""

# insert_query2 = """INSERT INTO frankfurt
# SELECT * FROM frankfurt_temp
# WHERE NOT EXISTS (
#     SELECT 1 FROM frankfurt
#     WHERE
#       frankfurt.id = frankfurt_temp.id
#       AND frankfurt.status = frankfurt_temp.status
# );"""



# insert_query2 = """INSERT INTO frankfurt
# SELECT * FROM frankfurt_temp
# WHERE NOT EXISTS (
#     SELECT 1 FROM frankfurt
#     WHERE frankfurt.ac = frankfurt_temp.ac
#       AND frankfurt.typ = frankfurt_temp.typ
#       AND frankfurt.al = frankfurt_temp.al
#       AND frankfurt.fnr = frankfurt_temp.fnr
#       AND frankfurt.terminal = frankfurt_temp.terminal
#       AND frankfurt.halle = frankfurt_temp.halle
#       AND frankfurt.schalter = frankfurt_temp.schalter
#       AND frankfurt.s = frankfurt_temp.s
#       AND frankfurt.iata = frankfurt_temp.iata
#       AND frankfurt.sched = frankfurt_temp.sched
#       AND frankfurt.reg = frankfurt_temp.reg
#       AND frankfurt.apname = frankfurt_temp.apname
#       AND frankfurt.id = frankfurt_temp.id
#       AND frankfurt.gate = frankfurt_temp.gate
#       AND frankfurt.lang = frankfurt_temp.lang
#       AND frankfurt.alname = frankfurt_temp.alname
#       AND frankfurt.flstatus = frankfurt_temp.flstatus
#       AND frankfurt.status = frankfurt_temp.status
#       AND frankfurt.cs = frankfurt_temp.cs
#       AND frankfurt.duration = frankfurt_temp.duration
#       AND frankfurt.stops = frankfurt_temp.stops
#       AND frankfurt.rouname = frankfurt_temp.rouname
#       AND frankfurt.rou = frankfurt_temp.rou
# );"""

# AND frankfurt.lu = frankfurt_temp.lu
cur.execute(insert_query)
cur.execute(insert_query2)
# Commit the changes to the database
conn.commit()
