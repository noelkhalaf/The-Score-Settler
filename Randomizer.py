import os
import shutil
import time
import random
import discord
from discord.ext import commands

class Randomizer:
    cardSuits = {
        "♠" : "spade",
        "♥" : "heart",
        "♦" : "diamond",
        "♣" : "club",
    }
    cardValues = {
        "1" : "A",
        "11" : "J",
        "12" : "Q",
        "13" : "K",
    }
    coinValues = ('Heads', 'Tails')

    async def coin(self, ctx, gifson):
        """
        flips a coin
        """
        result = self.getRandomCoin(ctx)
        if gifson:
            await ctx.send(file=discord.File('images/coin-animation-gifs/{}Flip.gif'.format(result)))
            time.sleep(6)
        await ctx.send("```ini\nYou flipped [{}]!\n```".format(result))

    async def coinChoices(self, ctx, choices, gifson):
        """
        flips a coin with choices
        :param args: coin flip choices
        """
        result = self.getRandomChoice(ctx, choices)
        if gifson:
            if result == choices[0]:
                await ctx.send(file=discord.File('images/coin-animation-gifs/HeadsFlip.gif'))
            else:
                await ctx.send(file=discord.File('images/coin-animation-gifs/TailsFlip.gif'))
            time.sleep(6)
        await ctx.send("```ini\nYou flipped [{}]!\n```".format(result))

    async def die(self, ctx, gifson):
        """
        rolls a die
        """
        result = self.getRandomDie(ctx)
        if gifson:
            await ctx.send(file=discord.File('images/dice-animation-gifs/dice-{}.gif'.format(result)))
            time.sleep(8)
        await ctx.send("```ini\nYou rolled a [{}]!\n```".format(result))

    async def card(self, ctx, gifson):
        """
        draws a card
        """
        value, suit = self.getRandomCard(ctx)
        value_royals = self.cardValues.get(value, value)
        suit_name = self.cardSuits[suit]
        if gifson:
            await ctx.send(file=discord.File('images/card-animation-gifs/{}/{}-{}.gif'.format(suit_name,value,suit_name)))
            time.sleep(6)
        await ctx.send("```ini\nYou drew a [{}{}]!\n```".format(value_royals, suit))

    async def range(self, ctx, low, high):
        """
        randomizes a number between low and high
        :param low: low number
        :param high: high number
        """
        await ctx.send("```ini\nYou got [{}]!\n```".format(self.getRandomRange(ctx, low, high)))

    async def list(self, ctx, args):
        """
        randomizes from listed options in args
        :param args: possible randomization outcomes
        """
        await ctx.send("```ini\nYou got [{}]!\n```".format(self.getRandomChoice(ctx, args)))

    def getRandomCoin(self, ctx):
        return random.choice(self.coinValues)

    def getRandomChoice(self, ctx, choices):
        return random.choice(choices)

    def getRandomDie(self, ctx):
        return str(random.randrange(1,6))

    def getRandomCard(self, ctx):
        return str(random.randrange(1,13)), random.choice(list(self.cardSuits))

    def getRandomRange(self, ctx, arg1, arg2):
        return random.randrange(arg1, arg2)