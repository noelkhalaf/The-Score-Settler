import asyncio
import os
import discord
from discord.ext import commands
from Randomizer import Randomizer
from UserEntries import UserEntries
import re
import traceback
from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from threading import Thread

""""
app=Flask("")

@app.route("/")
def index():
    return "<h1>Bot is running</h1>"

Thread(target=app.run,args=("0.0.0.0",8080)).start()
"""

randomizer = Randomizer()
userEntries = UserEntries()
gifs = True
aliases_dict = {
    'commands' : ['command', 'help', 'info', 'lost'],
    'coin' : ['flip','toss','flick','bern','bernoulli'],
    'die' : ['dice','roll'],
    'card' : ['deck','draw'],
    'range' : ['num','number','from'],
    'list' : ['options'],
    'new' : ['newfile', 'create', 'createfile', 'account'],
    'entries' : ['entry','prompt'],
    'resetfile' : ['reset', 'takemeback', 'goodoldays'],
    'getfile' : ['get', 'getentries', 'file', 'fetch', 'gimme', 'handitover'],
    'setfile' : ['set', 'setentries', 'changefile'],
    'sortfile' : ['alpha', 'alphabetical', 'sort', 'arrange', 'orderfile', 'order'],
    'cleanfile' : ['clean', 'filterfile', 'filter', 'duplicates', 'dup', 'dups', 'removeduplicates'],
    'clearfile' : ['clear', 'blank', 'canvas'],
    'addentries' : ['add', 'addentry', 'newentries'],
    'removeentries' : ['remove', 'removeentry'],
    'gifs' : ['togglegifs', 'gif'],
    'aliases' : ['alias'],
}

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("```bash\n'.{}' could not be recognized. Use '.help' to view the list of available commands.\n```".format(ctx.invoked_with))

@client.command(aliases=aliases_dict['commands'])
async def commands(ctx):
  await ctx.send('```bash\n\
                                            The Score Settler commands\n\
Basics:\n\
    \'.coin\' = Flips a two-sided coin.\n\
    \'.coin \"<this>\" \"<that>\"\' = Flips with what is at stake.\n\
    \'.die\' = Rolls a six-sided die.\n\
    \'.card\' = Draws a card from a 52-card deck.\n\
    \'.range <low> <high>\' = Randomizes a number between numbers low and high.\n\
    \'.list \"<thing1>\" \"<thing2>\" ...\' = Chooses at random from a list of options.\n\
Custom Entries:\n\
    \'.new\' = Creates a new personal Entries file.\n\
    \'.entries\' = Returns a random entry from the list of Entries.\n\
    \'.entries <number>\' = Returns a specific number of random Entries from the list of Entries.\n\
    \'.addentries \"<thing1>\" \"<thing2>\" ...\' = Adds Entries to the list of Entries.\n\
    \'.removeentries \"<thing1>\" \"<thing2>\" ...\' = Removes Entries from the list of Entries.\n\
    \'.getfile\' = Returns the list of Entries as a text file attachment.\n\
    \'.setfile <file.txt>\' = Sets the new list of Entries from the text file attachment.\n\
    \'.clearfile\' = Removes all Entries from the list of Entries.\n\
    \'.resetfile\' = Resets the list of Entries to its original contents.\n\
    \'.sortfile\' = Sorts the list of Entries alphabetically.\n\
    \'.cleanfile\' = Removes duplicates and empty lines from the list of Entries.\n\
Misc:\n\
    \'.gifs\' = Toggles gifs.\n\
    \'.aliases <command>\' = Shows the different aliases relating to specific commands.\
```')

"""
Basic Commands
"""

@client.command(aliases=aliases_dict['coin'])
async def coin(ctx, *, args):
    choices = re.findall(r"[\"\“]([\)\(\}\{\=\-\'\w\s]+)[\"\”]|([\)\(\}\{\=\-\'\w]+)", args)
    if len(choices) == 2:
        await randomizer.coinChoices(ctx, choices, gifs)
        return
    choices = args.split()
    if len(choices) == 2:
        await randomizer.coinChoices(ctx, choices, gifs)
    else:
        await ctx.send("```bash\nYou can either use '.flip' or '.flip \"<this>\" \"<that>\"'.\n```")
@coin.error
async def coin_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await randomizer.coin(ctx, gifs)

@client.command(aliases=aliases_dict['die'])
async def die(ctx):
    await randomizer.die(ctx, gifs)

@client.command(aliases=aliases_dict['card'])
async def card(ctx):
    await randomizer.card(ctx, gifs)

@client.command(aliases=aliases_dict['range'])
async def range(ctx, *args):
    if len(args) != 2:
        await ctx.send("```bash\nType two integers to define the range of integers (inclusive) to randomize a number from '.range <low> <high>'.\n```")
        return
    try:
        range = [int(float(i)) for i in args]
    except ValueError:
        await ctx.send("```bash\nType the range using only integers (inclusive) to randomize a number from '.range <low> <high>'.\n```")
        return
    if range[0] == range[1]:
        await ctx.send("```ini\nYou got [{}]!\n```".format(range[0]))
    elif range[0] > range[1]:
        await randomizer.range(ctx, range[1], range[0])
    else:
        await randomizer.range(ctx, range[0], range[1])
@range.error
async def range_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await ctx.send("```bash\nType the range of integers (inclusive) to randomize a number from '.range <low> <high>'.\n```")

@client.command(aliases=aliases_dict['list'])
async def list(ctx, *, args):
    choices = [a if b == '' else b for (a,b) in re.findall("\"([=-'*\w\s]+)\"|(\w+)", args)]
    await randomizer.list(ctx, choices)
@list.error
async def list_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await ctx.send("```bash\nType a list of possible randomization options to choose from '.list \"<thing1>\" \"<thing2>\" ...'.\n```")

"""
Custom Entries Commands
"""

@client.command(aliases=aliases_dict['new'])
async def new(ctx):
    await userEntries.createNewUser(ctx)

@client.command(aliases=aliases_dict['entries'])
async def entries(ctx, arg):
    try:
        num = int(float(arg))
    except ValueError:
        await ctx.send("```bash\nType the number of entries to randomize using only integers '.entries <number>'.\n```")
        return
    if num>10 or num<1:
        await ctx.send("```bash\nEnter a number of entries to randomize between 1 and 10 '.entries <number>'.\n```")
        return
    await userEntries.entries(ctx, num)
@entries.error
async def entries_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await userEntries.entries(ctx, 1)

@client.command(aliases=aliases_dict['addentries'])
async def addentries(ctx, *, args):
    choices = [a if b == '' else b for (a,b) in re.findall(r"[\"\“]([\)\(\}\{\=\-\'\w\s]+)[\"\”]|([\)\(\}\{\=\-\'\w]+)", args)]
    await userEntries.addEntries(ctx, choices)
@addentries.error
async def addentry_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await ctx.send("```bash\nType the entries you would like to add to the list of Entries '.addentries \"<entry1>\" \"<entry2>\" ...'.\n```")

@client.command(aliases=aliases_dict['removeentries'])
async def removeentries(ctx, *, args):
    choices = [a if b == '' else b for (a,b) in re.findall(r"[\"\“]([\)\(\}\{\=\-\'\w\s]+)[\"\”]|([\)\(\}\{\=\-\'\w]+)", args)]
    await userEntries.removeEntries(ctx, choices)
@removeentries.error
async def removeentry_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await ctx.send("```bash\nType the entries you would like to remove from the list of Entries'.removeentries \"<entry1>\" \"<entry2>\" ...'.\n```")


@client.command(aliases=aliases_dict['getfile'])
async def getfile(ctx):
    await userEntries.getFile(ctx)

@client.command(aliases=aliases_dict['setfile'])
async def setfile(ctx):
    try:
        file = ctx.message.attachments[0]
    except:
        await ctx.send("```bash\nNo file attached. Attach the file of Entries using '.setfile <file.txt>'.\n```")
        return
    if file.filename[-4:] != ".txt":
        await ctx.send("```bash\nAttach a text file of Entries using '.setfile <file.txt>'.\n```")
        return

    first_line = "Are you sure you would like to replace the current list of Entries with '{}'?\n".format(file.filename)
    confirming = True
    while confirming:
        await ctx.send("```ini\n{}Enter either [yes] or [no]\n```".format(first_line))
        first_line = ""
        try:
            reply = await client.wait_for('message', timeout=30.0)
            msg = reply.content.lower()
        except asyncio.TimeoutError:
            await ctx.send("```bash\nTimed out. Use '.setfile <file.txt>' to try again.\n```")
            return
        if msg == 'y' or msg == 'yes' or msg == 'yep' or msg == 'yeah' or msg == 'ye':
            confirming = False
            await userEntries.setFile(ctx, file)
        elif msg == 'n' or msg == 'no' or msg == 'nope' or msg == 'nah' or msg == 'negatory':
            confirming = False
            await ctx.send("```bash\nList of entries not modified.\n```")
            return
        else:
            first_line = "'{}' is not an accepted response.\n".format(msg)

@client.command(aliases=aliases_dict['clearfile'])
async def clearfile(ctx):
        first_line = "Are you sure you would like to remove all Entries from the list of Entries?\n"
        confirming = True
        while confirming:
            await ctx.send("```ini\n{}Enter either [yes] or [no]\n```".format(first_line))
            try:
                reply = await client.wait_for('message', timeout=30.0)
                msg = reply.content.lower()
            except asyncio.TimeoutError:
                await ctx.send("```bash\nTimed out. Use '.clearfile' to try again.\n```")
                return
            if msg == 'y' or msg == 'yes' or msg == 'yep' or msg == 'yeah' or msg == 'ye':
                confirming = False
                await userEntries.clearFile(ctx)
            elif msg == 'n' or msg == 'no' or msg == 'nope' or msg == 'nah' or msg == 'negatory':
                confirming = False
                await ctx.send("```bash\nList of entries not modified.\n```")
                return
            else:
                first_line = "'{}' is not an accepted response.\n".format(msg)

@client.command(aliases=aliases_dict['resetfile'])
async def resetfile(ctx):
    await userEntries.resetFile(ctx)

@client.command(aliases=aliases_dict['sortfile'])
async def sortfile(ctx):
    await userEntries.sortFile(ctx)

@client.command(aliases=aliases_dict['cleanfile'])
async def cleanfile(ctx):
    await userEntries.cleanFile(ctx)

"""
Misc Commands
"""

@client.command(aliases=aliases_dict['gifs'])
async def gifs(ctx):
    global gifs
    gifs = not gifs
    if gifs:
        await ctx.send("```bash\nGifs enabled successfully!\n```")
    else:
        await ctx.send("```bash\nGifs disabled successfully!\n```")

@client.command(aliases=aliases_dict['aliases'])
async def aliases(ctx, command):
    """
    shows all the aliases of a given command
    """
    if command in aliases_dict:
        await ctx.send("```ini\nAliases for '{}' : {}.\n```".format(command, aliases_dict[command]))
        return

    for key, value in aliases_dict.items():
        if command in value:
            aliases = [alias if alias != command else key for alias in value]
            await ctx.send("```ini\nAliases for '{}' : {}.\n```".format(command, aliases))
            return
    await ctx.send("```bash\n'{}' is not on of the avaiable commands.\nYou can use \'.command\' to view all the commands.```".format(command))
    #await commands(ctx)
@aliases.error
async def aliases_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await ctx.send("```bash\nEnter one of the possible commands to view its aliases '.aliases <command>'.\n```")


client.run(os.environ['TOKEN'])
