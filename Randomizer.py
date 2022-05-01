import random
import discord
from discord.ext import commands

class Randomizer:
    suits = ('♠', '♥', '♦', '♣')
    cards = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    dieValues = ('1', '2', '3', '4', '5', '6')
    coinValues = ('Heads', 'Tails')

    async def coin(self, ctx):
        """
        flips a coin
        """
        await ctx.send("```ini\nYou flipped {}!\n```".format(self.getRandomCoin(ctx)))

    async def coinChoices(self, ctx, choices):
        """
        flips a coin.
        :param args: coin flip choices
        """        
        await ctx.send("```ini\nYou flipped {}!\n```".format(self.getRandomCoinChoices(ctx, choices[0], choices[1])))

    async def die(self, ctx):
        """
        rolls a die
        """
        await ctx.send("```ini\nYou rolled a {}!\n```".format(self.getRandomDie(ctx)))

    async def card(self, ctx):
        """
        draws a card
        """
        await ctx.send("```ini\nYou drew a {}!\n```".format(self.getRandomCard(ctx)))

    async def range(self, ctx, low, high):
        """
        randomizes a number between low and high
        :param low: low number
        :param high: high number
        """
        await ctx.send("```ini\nYou got {}!\n```".format(self.getRandomRange(ctx, low, high)))

    async def list(self, ctx, args):
        """
        randomizes from listed options in args
        :param args: possible randomization outcomes
        """
        await ctx.send("```ini\nYou got {}!\n```".format(self.getRandomList(ctx, args.split())))

    def getRandomCoin(self, ctx):
        return random.choice(self.coinValues)

    def getRandomCoinChoices(self, ctx, arg1, arg2):
        return random.choice([arg1, arg2])

    def getRandomDie(self, ctx):
        return random.choice(self.dieValues)

    def getRandomCard(self, ctx):
        return random.choice(self.cards) + random.choice(self.suits)

    def getRandomRange(self, ctx, arg1, arg2):
        return random.randrange(arg1, arg2)

    def getRandomList(self, ctx, args):
        return random.choice(args)