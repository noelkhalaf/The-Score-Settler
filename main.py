from ast import alias
import discord
from discord.ext import commands
from Randomizer import Randomizer

aliases_dict = {
    'coin' : ['flip','toss','flick'],
    'die' : ['dice','roll'],
    'card' : ['deck','draw'],
    'range' : ['num','number','from'],
    'list' : ['options'],
}

client = commands.Bot(command_prefix = '.')
client.remove_command('help')
randomizer = Randomizer()

@client.event
async def on_ready():
  print('Bot is ready.')

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.CommandNotFound):
    await commands(ctx)

@client.command()
async def commands(ctx):
  await ctx.send('```bash\n\
The Score Settler commands:\n\
".coin" = Flips a two-sided coin.\n\
".coin <this> <that>" = Flips with what is at stake.\n\
".die" = Rolls a six-sided die.\n\
".card" = Draws a card from a 52-card deck.\n\
".range <low> <high>" = Randomizes an integer between numbers low and high.\n\
".list <thing1> <thing2> <thing3> ..." = Chooses at random from a list of options.\n\
".aliases <command>" = Shows the different aliases relating to specific commands.\
                ```')

@client.command(aliases=aliases_dict['coin'])
async def coin(ctx, *, args):
    choices = args.split()
    if len(choices) == 2:
        await randomizer.coinChoices(ctx, choices)
    else:
        await ctx.send("```ini\nYou can either do '.flip' or '.flip <this> <that>'.\n```")
@coin.error
async def coin_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await randomizer.coin(ctx)

@client.command(aliases=aliases_dict['die'])
async def die(ctx):
    await randomizer.die(ctx)

@client.command(aliases=aliases_dict['card'])
async def card(ctx):
    await randomizer.card(ctx)

@client.command(aliases=aliases_dict['range'])
async def range(ctx, *, args):
    range = [int(i) for i in args.split()]
    if len(range) == 2:
        if range[0] == range[1]:
            await ctx.send("```ini\nYou got {}!\n```".format(range[0]))       
        elif range[0] > range[1]:
            await randomizer.range(ctx, range[1], range[0])
        else:
            await randomizer.range(ctx, range[0], range[1])
    else:
        await ctx.send("```ini\nType the range of integers (inclusive) to randomize a number from '.range <low> <high>'.\n```")
@range.error
async def range_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await ctx.send("```ini\nType the range of integers (inclusive) to randomize a number from '.range <low> <high>'.\n```")

@client.command(aliases=aliases_dict['list'])
async def list(ctx, *, args):
    await randomizer.list(ctx, args)
@list.error
async def list_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await ctx.send("```ini\nType a list of possible randomization options to choose from '.list <thing1> <thing2> <thing3> ...'.\n```")


@client.command()
async def aliases(ctx, command):
    """
    shows all the aliases of a given command
    """
    if command in aliases_dict:
        await ctx.send("```ini\nAliases for {} : {}.\n```".format(command, aliases_dict[command]))
    else:
        await ctx.send("```ini\n{} is not a command.\n```".format(command))
        await commands(ctx)
@aliases.error
async def aliases_error(ctx, error):
	if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
		await ctx.send("```ini\nSpecify a command to view its aliases '.aliases <command>'.\n```")


client.run('OTY5NzI2MzA1MzQ2MTM4MTYy.Ymxl_w.V90kDA_3hntiIrPcyjRkjezPz4k')


"""
.flip                                   *
.flip <player1> <player2>               *
.roll                                   *
.roll <p1> <p2> <p3> <p4> <p5> <p6>
.roll <p1=4,5,6> <p2=1:3>
.range <high>
.range <low> <high>                     *
.range <low> <high> <exclusions>
.randomize <string1> <string2> ....     *
"""
