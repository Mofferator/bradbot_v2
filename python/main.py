import mysql.connector
from pull_quotes import *
import pandas as pd
import discord
import db_transactions
import warnings
import on_message_functions

warnings.filterwarnings('ignore')

token = open('/secrets/discord_token.txt').readline()
print(token)

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
	print("Logged in as {0.user}".format(client), flush=True)

@client.event
async def on_message(message):
	
	db_transactions.addUser(message.author.id, message.author.name)

	if message.author == client.user:
		return

	context = on_message_functions.functionContext(message, client)

	if message.content.startswith("$"):
		try:
			funcname = message.content.split(" ")[0].replace('$', '')
			func = getattr(on_message_functions, funcname)
			await func(context)
		except:
			pass

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
