import mysql.connector
import pandas as pd

db = mysql.connector.connect(
	host="mysql",
	user="root",
	password=open('/secrets/db_root_password.txt').readline(),
	database='BradBotDB'
)

def getRandomQuote():
	sql_stmnt = """
	SELECT * FROM Quotes
	ORDER BY RAND()
	LIMIT 1
	"""

	df = pd.read_sql(sql_stmnt, db)
	return df

def getRandomImage():
	sql_stmnt = """
	SELECT * FROM Images
	ORDER BY RAND()
	LIMIT 1
	"""

	df = pd.read_sql(sql_stmnt, db)
	return df["image_url"].values[0]

def addUser(user_id, user_name):
	user_sql = """
	INSERT INTO Users (user_id, user_name, uses)
	VALUES (%s, %s, 1)
	ON DUPLICATE KEY UPDATE uses = uses + 1;
	"""

	cursor = db.cursor()
	cursor.execute(user_sql, (user_id, user_name))
	db.commit()


def addMessage(messageID, guildID, guildName, messageText, quoteID, requesterID, requesterName):

	message_sql = """
	INSERT INTO MessageID (message_id, guild_id, guild_name, message_txt, quote_id, req_id)
	VALUES (%s, %s, %s, %s, %s, %s)
	"""

	cursor = db.cursor()
	cursor.execute(message_sql, (messageID, guildID, guildName, messageText, int(quoteID), requesterID))
	db.commit()
	
def getMessageMatchID(message_id):
	sql = """
	SELECT m.match_id
	FROM Matches m
	JOIN Quotes q ON m.match_id = q.match_id
	JOIN MessageID msg ON q.quote_id = msg.quote_id
	WHERE msg.message_id = %s;
	"""
	
	df = pd.read_sql(sql, db, params=(message_id,))
	try:
		return df["match_id"].values[0]
	except IndexError:
		return None
	
def checkPermission(user_id, permission_string):
	sql = """
	SELECT *
	FROM Users
	WHERE user_id = %s;
	"""

	df = pd.read_sql(sql, db, params=(user_id,))

	return df[permission_string].values[0] == 1

def addImage(image_url):
	sql = """
	INSERT INTO Images (image_url)
	VALUES (%s);
	"""

	try:
		cursor = db.cursor()
		cursor.execute(sql, (image_url,))
		db.commit()
		return True
	except:
		return False