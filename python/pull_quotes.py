import mysql.connector
import pandas as pd
import requests
import asyncio

account_id = 80597991
def getApiKey():
    password=open('/secrets/opendota_key.txt').readline()
    return password

def getDB():
    db = mysql.connector.connect(
        host="mysql",
        user="root",
        password=open('/secrets/db_root_password.txt').readline(),
        database='BradBotDB')
    return db


def getPulledMatchIDs():
    db = getDB()
    sql = "SELECT match_id FROM Matches"
    df = pd.read_sql(sql, db)
    print(f"Matches in DB: {len(df)}")
    return df["match_id"].to_list()

def getListOfAllMatchIDs(account_id):
    key = getApiKey()
    url = f"https://api.opendota.com/api/players/{account_id}/matches?api_key={key}"

    payload = {}
    headers = {}

    responseJson = requests.request("GET", url, headers=headers, data=payload).json()

    matchIDs = [match["match_id"] for match in responseJson]
    return matchIDs

def getMatch(match_id):
    key = getApiKey()
    url = f"https://api.opendota.com/api/matches/{match_id}?api_key={key}"

    payload = {}
    headers = {}

    responseJson = requests.request("GET", url, headers=headers, data=payload).json()

    return responseJson

def ingestMatchJson(matchJson, account_id):
    match_id = matchJson["match_id"]
    playerSlot = -1
    kills = -1
    assists = -1
    deaths = -1
    messages = []
    for p in matchJson["players"]:
        if p["account_id"] == account_id:
            playerSlot = p["player_slot"]
            kills = p["kills"]
            assists = p["assists"]
            deaths = p["deaths"]
    if matchJson["chat"] is not None:
        for msg in matchJson["chat"]:
            if msg["player_slot"] == playerSlot:
                messages.append(msg["key"])


    db = getDB()
    print(f"MatchID : {match_id}\nkills : {kills}\nassists : {assists}\ndeaths : {deaths}")
    match_insert_stmt = """
    INSERT INTO Matches (match_id, kills, assists, deaths)
    VALUES (%s, %s, %s, %s)
    """

    quotes_insert_stmt = """
    INSERT INTO Quotes (match_id, quote)
    VALUES (%s, %s)
    """

    quoteData = [(match_id, msg) for msg in messages]

    cursor = db.cursor()
    cursor.execute(match_insert_stmt, (match_id, kills, assists, deaths))
    cursor.executemany(quotes_insert_stmt, quoteData)
    db.commit()
    print(f"Match {match_id} added to database", flush=True)


def getNewMatchIDs(account_id):
    pulledIDs = getPulledMatchIDs() 
    allIDs = getListOfAllMatchIDs(account_id)
    newIDs = [id for id in allIDs if id not in pulledIDs]
    return newIDs

def pullNewMatches(account_id):
    newIDs = getNewMatchIDs(account_id)

    for id in newIDs:
        matchJson = getMatch(id)
        ingestMatchJson(matchJson, account_id)
