import mysql.connector
from pull_quotes import *
import pandas as pd
import discord
import db_transactions
import warnings
import validators
import definitions

warnings.filterwarnings('ignore')

token = open('/secrets/discord_token.txt').readline()
print(token)

client = discord.Client(intents=discord.Intents.all())

def bradbot(message):
	msg = db_transactions.getRandomQuote()
	line = msg["quote"].values[0]
	author = message.author.name
	server = message.guild.name
	print("%-25s %-35s Brad said:'%s'" %(server, author, line), flush=True)
	return msg

def addImage(message):
	try:
		url = message.content.split(" ")[1]
	except:
		url = ""
		error =  definitions.missing_url
		return False, url, error
	result = False
	error = None
	if db_transactions.checkPermission(message.author.id, definitions.add_image_perms):
		if validators.url(url):
			result = db_transactions.addImage(url)
			if result:
				print(f"Image URL {url} added by user {message.author.name}", flush=True)
			else:
				error = definitions.database_duplicate_entry
		else:
			error = definitions.invalid_url
	else:
		error = definitions.insufficient_permissions
	return result, url, error

def bradface(message):
	print("%-25s %-35s Bradface:'%s'" %(message.guild.name, message.author, ":)"), flush=True)
	return db_transactions.getRandomImage()

def bradhelp(message):
	print("%-25s %-35s Requested help" %(message.guild.name, message.author), flush=True)
	embed=discord.Embed(title="Brad Bot Help", url="https://github.com/Mofferator/bradbot", color=0xff0000)
	embed.set_thumbnail(url="https://i.postimg.cc/25Z4ckXg/unknown4.png")
	embed.add_field(name="Brad Bot", value="Type `$bradbot` to make Brad Bot say one of his all chat lines at random", inline=False)
	embed.add_field(name="Brad Bot React", value="React to any of Brad Bot's all chat lines to get a link to the match", inline=False)
	embed.add_field(name="Brad Face", value="Type `$bradface` to see a random picture of Bradley Dragon", inline=False)
	return embed

def listServers():
	print("{} is in {} servers:".format(client.user, len(client.guilds)), flush=True)
	for guild in client.guilds:
		print("\t{}".format(guild.name), flush=True)

@client.event
async def on_ready():
	print("Logged in as {0.user}".format(client), flush=True)

@client.event
async def on_message(message):
	
	db_transactions.addUser(message.author.id, message.author.name)

	if message.author == client.user:
		return

	if message.content.startswith("$bradbot"):
		msg = bradbot(message)
		sent = await message.channel.send(msg["quote"].values[0])
		db_transactions.addMessage(sent.id, sent.guild.id, sent.guild.name, msg["quote"].values[0], msg["quote_id"].values[0], message.author.id, message.author.name)

	if message.content.startswith("$bradface"):
		await message.channel.send(bradface(message))

	if message.content.startswith("$bradhelp"):
		await message.reply(embed=bradhelp(message))
		
	if message.content.startswith("$listservers"):
		listServers()

	if message.content.startswith("$addimage"):
		result, url, error = addImage(message)
		if result:
			embed=discord.Embed(title=f"Image added", url=url, color=0xff0000)
			embed.set_thumbnail(url=url)
			await message.reply(embed=embed)
		else:
			await message.reply(f"`ERROR (add image) : {error}`")

@client.event
async def on_guild_join(guild):
	print("BradBot joined server: '{}'".format(guild.name), flush=True)

@client.event
async def on_reaction_add(reaction, user):
	if reaction.message.author == client.user:
		if(reaction.message.channel.guild.me.guild_permissions.embed_links):
			message_id = reaction.message.id
			msg_info = db_transactions.getMessageMatchID(message_id)
			if msg_info is not None and len(reaction.message.reactions) == 1 and reaction.message.reactions[0].count == 1:
				embed=discord.Embed(title=f"Match {msg_info}", url=f"https://opendota.com/matches/{msg_info}/chat", color=0xff0000)
				image = db_transactions.getRandomImage()
				embed.set_thumbnail(url=image)
				print("%-25s %-35s Match ID fetched:'%s'" %(reaction.message.guild.name, "N/A", msg_info), flush=True)
				await reaction.message.reply(embed=embed)
		else:
			await reaction.message.reply(msg_info)

if __name__ == "__main__":
	
	client.run(token)
