import db_transactions
import definitions
import discord
import validators

class functionContext:
	def __init__(self, message, client):
		self.message = message
		self.client = client

async def bradbot(context):
	msg = db_transactions.getRandomQuote()
	line = msg["quote"].values[0]
	author = context.message.author.name
	server = context.message.guild.name
	print("%-25s %-35s Brad said:'%s'" %(server, author, line), flush=True)
	sent = await context.message.channel.send(msg["quote"].values[0])
	db_transactions.addMessage(sent.id, sent.guild.id, sent.guild.name, msg["quote"].values[0], msg["quote_id"].values[0], context.message.author.id, context.message.author.name)

async def addimage(context):
	try:
		url = context.message.content.split(" ")[1]
	except:
		url = ""
		error =  definitions.missing_url
		return False, url, error
	result = False
	error = None
	if db_transactions.checkPermission(context.message.author.id, definitions.add_image_perms):
		if validators.url(url):
			result = db_transactions.addImage(url)
			if result:
				print(f"Image URL {url} added by user {context.message.author.name}", flush=True)
			else:
				error = definitions.database_duplicate_entry
		else:
			error = definitions.invalid_url
	else:
		error = definitions.insufficient_permissions
	
	if result:
		embed=discord.Embed(title=f"Image added", url=url, color=0xff0000)
		embed.set_thumbnail(url=url)
		await context.message.reply(embed=embed)
	else:
		await context.message.reply(f"`ERROR (add image) : {error}`")

async def bradface(context):
	print("%-25s %-35s Bradface:'%s'" %(context.message.guild.name, context.message.author, ":)"), flush=True)
	url = db_transactions.getRandomImage()
	await context.message.channel.send(url)

async def bradhelp(context):
	print("%-25s %-35s Requested help" %(context.message.guild.name, context.message.author), flush=True)
	embed=discord.Embed(title="Brad Bot Help", url="https://github.com/Mofferator/bradbot", color=0xff0000)
	embed.set_thumbnail(url="https://i.postimg.cc/25Z4ckXg/unknown4.png")
	embed.add_field(name="Brad Bot", value="Type `$bradbot` to make Brad Bot say one of his all chat lines at random", inline=False)
	embed.add_field(name="Brad Bot React", value="React to any of Brad Bot's all chat lines to get a link to the match", inline=False)
	embed.add_field(name="Brad Face", value="Type `$bradface` to see a random picture of Bradley Dragon", inline=False)
	await context.message.reply(embed=embed)

async def listservers(context):
	print("{} is in {} servers:".format(context.client.user, len(context.client.guilds)), flush=True)
	for guild in context.client.guilds:
		print("\t{}".format(guild.name), flush=True)
