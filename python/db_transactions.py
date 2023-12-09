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

def addMessage(messageID, guildID, guildName, messageText, quoteID, requesterID, requesterName):
	
	user_sql = """
	INSERT INTO Users (user_id, user_name, uses)
	VALUES (%s, %s, 1)
	ON DUPLICATE KEY UPDATE uses = uses + 1;
	"""

	message_sql = """
	INSERT INTO MessageID (message_id, guild_id, guild_name, message_txt, quote_id, req_id)
	VALUES (%s, %s, %s, %s, %s, %s)
	"""

	cursor = db.cursor()
	cursor.execute(user_sql, (requesterID, requesterName))
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
	


def addURLs():

	urls = ["https://i.imgur.com/MpsvpWw.png",
	"https://i.imgur.com/O3dkmGx.png",
	"https://cdn.discordapp.com/attachments/940421411024011275/986373541601640518/unknown.png",
	"https://cdn.discordapp.com/attachments/875389011932377108/981115714654048257/unknown.png",
	"https://cdn.discordapp.com/attachments/875389011932377108/978386659253055498/uikkiuhikuiuk.jpg",
	"https://cdn.discordapp.com/attachments/875389011932377108/963948493075009536/unknown.png",
	"https://cdn.discordapp.com/attachments/875389011932377108/961012326063018044/unknown.png",
	"https://cdn.discordapp.com/attachments/875389011932377108/957335961103110204/unknown.png",
	"https://cdn.discordapp.com/attachments/875389011932377108/953437806150184970/bradsharkevil.png",
	"https://cdn.discordapp.com/attachments/875389011932377108/935740154373615635/unknown.png",
	"https://cdn.discordapp.com/attachments/875389011932377108/933896025217830973/34534535.png",
	"https://cdn.discordapp.com/attachments/875389011932377108/930119318203695224/brad.png",
	"https://cdn.discordapp.com/attachments/875389011932377108/918633363840049222/unknown.png",
	"https://cdn.discordapp.com/attachments/875389011932377108/903039503881633802/unknown.png",
	"https://i.postimg.cc/Qd5W9Rzk/11.png",
	"https://i.postimg.cc/Yq069Dkb/2.png",
	"https://i.postimg.cc/d31yhDML/3432434.jpg",
	"https://i.postimg.cc/V6zMcDD9/756u65u6u.jpg",
	"https://i.postimg.cc/63zZ6nmk/768u6uy.jpg",
	"https://i.postimg.cc/d0Pr5qCx/78yiuytiuy.jpg",
	"https://i.postimg.cc/rFHStGwc/7m8iu7iu.jpg",
	"https://i.postimg.cc/XvfFhTc7/7ui7yuiuy.jpg",
	"https://i.postimg.cc/t4VFd1s6/7yui7yi7uyi.jpg",
	"https://i.postimg.cc/kM1SkN88/bdt-rdreynrynrt.jpg",
	"https://i.postimg.cc/wMGsLHHF/bjkhoyn.jpg",
	"https://i.postimg.cc/3JzvwKtx/dfgdfgfd.jpg",
	"https://i.postimg.cc/TYKbGyqs/erwretstrd.jpg",
	"https://i.postimg.cc/jjbnzM0V/etrwtrfgg.jpg",
	"https://i.postimg.cc/7LnGXSw5/ewr3ewrew.jpg",
	"https://i.postimg.cc/nzVsWMh0/fdgfdgff.jpg",
	"https://i.postimg.cc/Px6LnhLh/fgdgfhfg.jpg",
	"https://i.postimg.cc/PJPCtcZD/fgfgfgfg.jpg",
	"https://i.postimg.cc/QCwHVbky/fghrteghrtgh.jpg",
	"https://i.postimg.cc/2jKqHkR7/ftuyjyghjgyhjgy.jpg",
	"https://i.postimg.cc/GhT4VWbw/ftyhtfhghg.jpg",
	"https://i.postimg.cc/3Nv3fHmt/fyhrtytryt.jpg",
	"https://i.postimg.cc/cLqvSFJK/gffgfg.jpg",
	"https://i.postimg.cc/pdCrKxJ8/ghghghh.jpg",
	"https://i.postimg.cc/4xzmNpKW/ghuuhji.jpg",
	"https://i.postimg.cc/6QtT7Tnt/ghyhjughuj.jpg",
	"https://i.postimg.cc/B6v6gymz/grgrdfgrf.jpg",
	"https://i.postimg.cc/4dF3F5Mx/gyfhcgyfh.jpg",
	"https://i.postimg.cc/KjkYXTSr/hjhjhj.jpg",
	"https://i.postimg.cc/NF3jQ0Qh/hjyyhj.jpg",
	"https://i.postimg.cc/wxZvXwLW/huguhjuhj.jpg",
	"https://i.postimg.cc/L6PsNjVm/hyr56y5y.jpg",
	"https://i.postimg.cc/6pNpSTHn/i7yi7yiu.jpg",
	"https://i.postimg.cc/CxHxVYtt/iklojkjkjo.jpg",
	"https://i.postimg.cc/25k8kMN5/ikuhkk.jpg",
	"https://i.postimg.cc/GpX3HKbx/iouoiuoiol.jpg",
	"https://i.postimg.cc/qRgJnKRV/iouyiouio.jpg",
	"https://i.postimg.cc/W3K274FD/iuyiuiui.jpg",
	"https://i.postimg.cc/8kJWgJb0/jikhjikjik.jpg",
	"https://i.postimg.cc/141sLYKs/jkhjkjkj.jpg",
	"https://i.postimg.cc/9X69mm8F/jkkjkj.jpg",
	"https://i.postimg.cc/15Dq4k20/jklijljk.jpg",
	"https://i.postimg.cc/GmrsDMnW/jughhjjhlkkljklk.jpg",
	"https://i.postimg.cc/6p04fd9y/juhghjuhjug.jpg",
	"https://i.postimg.cc/3wx4SdR9/jy8yuy.jpg",
	"https://i.postimg.cc/7LtCpwJ4/jyutru6uy.jpg",
	"https://i.postimg.cc/bJKZwgRF/kiuhkuikui.jpg",
	"https://i.postimg.cc/0Q66vF7w/kjhjkhjkh.jpg",
	"https://i.postimg.cc/qqyzhKbB/kklijk.jpg",
	"https://i.postimg.cc/qB3t5fJf/pknoilj.jpg",
	"https://i.postimg.cc/X76ZM2qr/poipopo.jpg",
	"https://i.postimg.cc/TYjKTr5C/rdb-trebtrtr.jpg",
	"https://i.postimg.cc/RZMNhNc9/reg5h65er6t5r.jpg",
	"https://i.postimg.cc/0NjjGFWB/retgrhth5rtt.jpg",
	"https://i.postimg.cc/R0YFgd2V/rtyhtryhtyrhty.jpg",
	"https://i.postimg.cc/fRBk9DKd/rtytrytrytr.jpg",
	"https://i.postimg.cc/ydSNt9zh/Screenshot-1.jpg",
	"https://i.postimg.cc/3N5wTRKs/tryhrtytryht.jpg",
	"https://i.postimg.cc/WzG1bvzh/trytyhthth.jpg",
	"https://i.postimg.cc/v8fBvWhb/tuyjghfjghf.jpg",
	"https://i.postimg.cc/X7Wv1p1F/tuytyruytuy.jpg",
	"https://i.postimg.cc/RVTZk42Y/tyhfytjyjut.jpg",
	"https://i.postimg.cc/pdmV58yN/tytruytut.jpg",
	"https://i.postimg.cc/9Q8Ff1mt/u8ytiuy8i8y8yiu.jpg",
	"https://i.postimg.cc/rwFwc7kw/ugjyjhghjgkjh.jpg",
	"https://i.postimg.cc/j2bR1FcK/uhikikuikuiku.jpg",
	"https://i.postimg.cc/7LjH36T5/uikkiuhikuiuk.jpg",
	"https://i.postimg.cc/k48nfmxf/uikuykk.jpg",
	"https://i.postimg.cc/90YcHYg9/uiuyukuku.jpg",
	"https://i.postimg.cc/fTMwj1kf/uiyiuyi7uyiuyi.jpg",
	"https://i.postimg.cc/dQ2sCJQ0/uiyiuyiuyiuy.jpg",
	"https://i.postimg.cc/NfbQNbHq/ujhjj.jpg",
	"https://i.postimg.cc/t4Tp8P31/ujygijuhijuuijuij.jpg",
	"https://i.postimg.cc/7ZWw469K/ujygjyghjy.jpg",
	"https://i.postimg.cc/bvS8whFp/utyhjgfjhg.jpg",
	"https://i.postimg.cc/ZRkm9M13/uygjuyguyg.jpg",
	"https://i.postimg.cc/264DnxDt/uytuyyuuy.jpg",
	"https://i.postimg.cc/4ysTPh4x/uyuy.jpg",
	"https://i.postimg.cc/nVGxzTTj/y7tugyuyg.jpg",
	"https://i.postimg.cc/3N1QcJWC/ygfcghv.jpg",
	"https://i.postimg.cc/7YPkT7QB/ygu-kyiyiy.jpg",
	"https://i.postimg.cc/qMmdcRPp/yhthfghtfhf.jpg",
	"https://i.postimg.cc/Dw83xhhL/yjygjy.jpg",
	"https://i.postimg.cc/FRQtFJLV/yrtfytrutuht.jpg",
	"https://i.postimg.cc/XYmShPNh/ytrytrtrutru.jpg",
	"https://i.postimg.cc/pdjbtBpd/ytrytrytrytr.jpg",
	"https://i.postimg.cc/5ynDm7ks/yuhujghugjhgj.jpg",
	"https://i.postimg.cc/d3qzrPn7/yuhuyjtyu.jpg",
	"https://i.postimg.cc/Y9N5vqNK/yuiuj.jpg",
	"https://i.postimg.cc/Vsgy1vLX/yuiuyiuyiuy.jpg",
	"https://i.postimg.cc/gk2C0pnQ/yutuyuyyu.jpg",
	"https://cdn.discordapp.com/attachments/872924113725956106/1009881158831587399/bradthunk.gif",
	"https://i.postimg.cc/CKQQDxnt/20221210-103549.png",
	"https://i.postimg.cc/Znr71Pst/fefef.png",
	"https://i.postimg.cc/25VHzN9x/image.png",
	"https://i.postimg.cc/jd43cXJy/image1.png",
	"https://i.postimg.cc/rFMQDrYs/image10.png",
	"https://i.postimg.cc/T2qcvPY6/image12.png",
	"https://i.postimg.cc/tJ5d3BmT/image13.png",
	"https://i.postimg.cc/qq0X6PwS/image14.png",
	"https://i.postimg.cc/1tFJqcQn/image2.png",
	"https://i.postimg.cc/ZY3MBZb7/image3.png",
	"https://i.postimg.cc/g2MSF2sJ/image4.png",
	"https://i.postimg.cc/MHk3P3Dm/image5.png",
	"https://i.postimg.cc/c4S5fj6s/image6.png",
	"https://i.postimg.cc/s2qTxHtC/image7.png",
	"https://i.postimg.cc/Xq0xcGj2/image8.png",
	"https://i.postimg.cc/gjqsMzrG/image9.png",
	"https://i.postimg.cc/tgKzpZxX/Screenshot-20220614-1143062.png",
	"https://i.postimg.cc/GhXJ9Syg/unknown.png",
	"https://i.postimg.cc/y8WhRXh1/unknown2.png",
	"https://i.postimg.cc/13TGrnMp/unknown3.png",
	"https://i.postimg.cc/25Z4ckXg/unknown4.png",
	"https://media.discordapp.net/attachments/872928101057822750/1064641974256275606/image.png",
	"https://media.discordapp.net/attachments/872924113725956106/1064658511377748088/jhijgh.jpg"
	]

	urls = [(url,) for url in urls]
	cursor = db.cursor()
	cursor.executemany("INSERT INTO Images (image_url) VALUES (%s)", urls)
	db.commit()