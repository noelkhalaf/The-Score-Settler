import os
import shutil
import time
import random
import discord
from discord.ext import commands

class Randomizer:
    suits = ('♠', '♥', '♦', '♣')
    cards = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    dieValues = ('1', '2', '3', '4', '5', '6')
    coinValues = ('Heads', 'Tails')
    
    async def coin(self, ctx, gifson):
        """
        flips a coin
        """
        result = self.getRandomCoin(ctx)
        if gifson:
            if result == 'Heads':
                await ctx.send(file=discord.File('images/HeadsFlip.gif'))
            else:
                await ctx.send(file=discord.File('images/TailsFlip.gif'))
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
                await ctx.send(file=discord.File('images/HeadsFlip.gif'))
            else:
                await ctx.send(file=discord.File('images/TailsFlip.gif'))
            time.sleep(6)
        await ctx.send("```ini\nYou flipped [{}]!\n```".format(result))

    async def die(self, ctx, gifson):
        """
        rolls a die
        """
        result = self.getRandomDie(ctx)
        if gifson:
            if result == '1':
                await ctx.send(file=discord.File('images/dice-1.gif'))
            elif result == '2':
                await ctx.send(file=discord.File('images/dice-2.gif'))
            elif result == '3':
                await ctx.send(file=discord.File('images/dice-3.gif'))
            elif result == '4':
                await ctx.send(file=discord.File('images/dice-4.gif'))
            elif result == '5':
                await ctx.send(file=discord.File('images/dice-5.gif'))
            elif result == '6':
                await ctx.send(file=discord.File('images/dice-6.gif'))
            time.sleep(8)
        await ctx.send("```ini\nYou rolled a [{}]!\n```".format(result))

    async def card(self, ctx):
        """
        draws a card
        """
        await ctx.send("```ini\nYou drew a [{}]!\n```".format(self.getRandomCard(ctx)))

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

    async def entries(self, ctx, num):
        """
        randomizes from entries in entries.txt
        """
        with open("textfiles/entries.txt", "r") as f:
            entries = f.readlines()
        entries = [entry for entry in entries if entry != "\n"]
        if await self.isFileEmpty(ctx, entries): return
        entries_names = [entry[:-1] if entry[-1:] == "\n" else entry for entry in entries]
        for i in range(num):
            await ctx.send("```ini\nYou got [{}]!\n```".format(self.getRandomChoice(ctx, entries_names)))

    async def resetfile(self, ctx):
        """
        replaces the entries.txt file contents with contents of entries_original.txt
        """ 
        shutil.copy2("./textfiles/entries_original.txt","./textfiles/entries.txt")
        await ctx.send("```ini\nEntries reset successfully!\n```")

    async def getfile(self, ctx):
        """
        returns the entries.txt file to view entries
        """ 
        await ctx.send("```ini\nHere is the text file with the entries:\n```")
        await ctx.send(file=discord.File('textfiles/entries.txt'))

    async def setfile(self, ctx, file):
        """
        replaces entries in entries.txt file with new file
        """
        await file.save("textfiles/entries.txt")
        await ctx.send("```ini\nEntries updated successfully!\n```")

    async def sortfile(self, ctx):
        """
        sorts the entries in the entries.txt file alphabetically
        """
        with open("textfiles/entries.txt", "r+") as f:
            entries = f.readlines()
        newentries = [entry+"\n" if entry[-1] !="\n" else entry for entry in entries if entry != "\n"]
        if await self.isFileEmpty(ctx, newentries): return
        newentries.sort(key=str.lower)
        self.replaceEntries(ctx, newentries)
        await ctx.send("```ini\nEntries sorted successfully!\n```")

    async def cleanfile(self, ctx):
        """
        filters out duplicate entries from the entries.txt file
        """
        with open("textfiles/entries.txt", "r+") as f:
            entries = f.readlines()
        entries = [entry+"\n" if entry[-1] !="\n" else entry for entry in entries if entry != "\n"]
        if await self.isFileEmpty(ctx, entries): return
        newentries = list(dict.fromkeys(entries))
        self.replaceEntries(ctx, newentries)
        numdups = len(entries) - len(newentries)
        if numdups == 0:
            await ctx.send("```ini\nNo duplicates in Entries to remove.\n```")
        else:
            await ctx.send("```ini\n[{}] duplicates in Entries removed successfully!\n```".format(numdups))

    async def addentries(self, ctx, args):
        """
        appends specified entries to the entries.txt file
        :param args: list of entries
        """
        with open("textfiles/entries.txt", "r+") as f:
            entries = f.readlines()
            entries = [entry.lower() for entry in entries]
            if entries[-1][-1:] != "\n":
                f.write("\n")
            for arg in args:
                if arg.lower() in entries:
                    await ctx.send("```ini\nEntry [{}] is already in the list of Entries\n```".format(arg))
                else:
                    f.write(arg+"\n")
                    await ctx.send("```ini\n[{}] successfully added to Entries!\n```".format(arg))

    async def removeentries(self, ctx, args):
        """
        removes specified entries from the entries.txt file
        :param args: list of entries
        """
        with open("textfiles/entries.txt", "r+") as f:
            entries = f.readlines()
            if await self.isFileEmpty(ctx, entries): return
            newentries = entries
            entries = [entry[:-1].lower() for entry in entries]
            for arg in args:
                if arg.lower() not in entries:
                    await ctx.send("```ini\nEntry [{}] is not in the list of Entries\n```".format(arg))
                    continue
                count = 0
                for i, entry in enumerate(entries):
                    if entry == arg.lower():
                        newentries[i] = ""
                        count += 1
                    if i == len(entries)-1:
                        await ctx.send("```ini\nSuccessfully removed {} instance(s) of [{}] from Entries!\n```".format(count,arg))
        self.replaceEntries(ctx, newentries)

    def getRandomCoin(self, ctx):
        return random.choice(self.coinValues)

    def getRandomChoice(self, ctx, choices):
        return random.choice(choices)

    def getRandomDie(self, ctx):
        return random.choice(self.dieValues)

    def getRandomCard(self, ctx):
        return random.choice(self.cards) + random.choice(self.suits)

    def getRandomRange(self, ctx, arg1, arg2):
        return random.randrange(arg1, arg2)

    async def isFileEmpty(self, ctx, entries):
        if not entries:
            await ctx.send("```ini\nThere are no entries to choose from. Use '.addentry <entry1>/<entry2>/...' or '.setfile <file.txt>' to add entries!\n```")
            return True
        return False

    def replaceEntries(self, ctx, newentries):
        with open("textfiles/entries.txt", "r+") as f:
            f.seek(0)
            for entry in newentries:
                if entry[-1:] != "\n":
                    f.write(entry+"\n")
                else:
                    f.write(entry)
            f.truncate()
    