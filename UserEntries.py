import os
import sqlite3
from inspect import currentframe
from random import choice
import discord

class UserEntries:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('sql/users.db')
            self.c = self.conn.cursor()
            self.c.execute("""CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY,
                            display_name TEXT NOT NULL,
                            username TEXT NOT NULL,
                            discriminator INTEGER NOT NULL,
                            server TEXT NOT NULL,
                            entries TEXT NOT NULL
                        )""")
            self.conn.commit()
        except Exception as e:
            print('Error ('+currentframe().frameinfo.f_back.f_lineno+'): ', e)

    async def createNewUser(self, ctx, entries=""):
        """
        Creates a new row in the DB for the user if it's not already there
        Uses entries_original.txt as a default list of entries
        """ 
        try:
            self.c.execute("INSERT INTO users (user_id, display_name, username, discriminator, server, entries) VALUES (?,?,?,?,?,?)",
                        (self.getUserId(ctx), self.getDisplayName(ctx), self.getUsername(ctx), self.getDiscriminator(ctx), self.getServerName(ctx), entries))
            self.conn.commit()
            await ctx.send("```ini\nSuccessfully created your personal Entries file {}!\n```".format(self.getDisplayName(ctx)))
        except Exception as e:
            print('Error ('+str(currentframe().frameinfo.f_back.f_lineno)+'): ', e)
            await ctx.send("```ini\nYour personal Entries file has already been made {}.\n```".format(self.getDisplayName(ctx)))

    async def entries(self, ctx, num):
        """
        Randomizes entries from the user's 'entries' attribute in the DB
        Takes from the entries_original.txt if the user_id is not found in the DB
        :param num: number of entries to randomly select
        """
        user_id = self.getUserId(ctx)
        self.c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        try:
            data = self.c.fetchone()[5]
        except Exception as e:
            data = self.getDefaultEntries()

        with open(f"textfiles/{user_id}.txt", "w") as f:
            f.write(data)

        with open(f"textfiles/{user_id}.txt", "r") as f:
            entries = f.readlines()
        os.remove(f"textfiles/{user_id}.txt")

        if await self.isFileEmpty(ctx, entries): return
        entries_names = [entry[:-1].strip() if entry[-1:] == "\n" else entry.strip() for entry in entries if entry.strip() != "\n"]
        for i in range(num):
            await ctx.send("```ini\nYou got [{}]!\n```".format(choice(entries_names)))

    async def addEntries(self, ctx, args):
        """
        Appends specified entries to the user's 'entries' attribute in the DB
        Creates a new row in the DB for the user if user_id is not recognized
        :param args: list of entries
        """
        user_id = self.getUserId(ctx)
        self.c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        try:
            old_data = self.c.fetchone()[5]
        except Exception as e:
            await self.createNewUser(ctx, self.getDefaultEntries())
            old_data = self.getDefaultEntries()
            
        
        with open(f"textfiles/{user_id}.txt", "w") as f:
            f.write(old_data)

        with open(f"textfiles/{user_id}.txt", "r+") as f:
            old_entries = f.readlines()
            old_entries = [entry.lower().strip() for entry in old_entries if entry.strip() != "\n"]
            
            if len(old_entries) > 0:
                if not old_entries[-1].endswith("\n"):
                    f.write("\n")

            for arg in args:
                if arg.lower().strip()+"\n" in old_entries:
                    await ctx.send("```ini\nEntry [{}] is already in the list of Entries\n```".format(arg))
                else:
                    f.write(arg.strip()+"\n")
                    await ctx.send("```ini\n[{}] successfully added to Entries!\n```".format(arg))

        with open(f"textfiles/{user_id}.txt", "r") as f:
            new_entries = f.read()
        os.remove(f"textfiles/{user_id}.txt")
        
        try:
            self.c.execute("UPDATE users SET entries=? WHERE user_id=?", (new_entries, user_id))
        except Exception as e:
            print('Error ('+str(currentframe().frameinfo.f_back.f_lineno)+'): ', e)
        self.conn.commit()

    async def removeEntries(self, ctx, args):
        """
        Appends specified entries to the user's 'entries' attribute in the DB
        Creates a new row in the DB for the user if user_id is not recognized
        :param args: list of entries
        """
        user_id = self.getUserId(ctx)
        self.c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        try:
            old_data = self.c.fetchone()[5]
        except Exception as e:
            old_data = self.getDefaultEntries()
            await self.createNewUser(ctx, old_data)
            
        with open(f"textfiles/{user_id}.txt", "w") as f:
            f.write(old_data)

        with open(f"textfiles/{user_id}.txt", "r") as f:
            old_entries = f.readlines()
            new_entries = old_entries
            if await self.isFileEmpty(ctx, old_entries): return
            old_entries = [entry[:-1].strip() if entry[-1:] == "\n" else entry.strip() for entry in old_entries if entry.strip() != "\n"]
            for arg in args:
                if arg.lower().strip() not in old_entries.lower():
                    await ctx.send("```ini\nEntry [{}] is not in the list of Entries\n```".format(arg))
                    continue
                count = 0
                for entry in old_entries:
                    if entry.lower() == arg.lower().strip():
                        new_entries.remove(entry)
                        count += 1
                if count > 0:
                    await ctx.send("```ini\nSuccessfully removed {} instance(s) of [{}] from Entries!\n```".format(count,arg))
        os.remove(f"textfiles/{user_id}.txt")

        try:
            new_entries_str = "\n".join(new_entries) + "\n"
            self.c.execute("UPDATE users SET entries=? WHERE user_id=?", (new_entries_str, user_id))
        except Exception as e:
            print('Error ('+str(currentframe().frameinfo.f_back.f_lineno)+'): ', e)
        self.conn.commit()

    async def getFile(self, ctx):
        """
        Returns the user's 'entries' attribute as a text file to view
        Returns the entries_original.txt if the user_id is not found in the DB
        """ 
        user_id = self.getUserId(ctx)
        data = self.c.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()

        if not data:
            await ctx.send("```ini\nHere is the original Entries text file:\n```")
            await ctx.send(file=discord.File('textfiles/entries_original.txt'))
            return

        with open(f"textfiles/{user_id}.txt", "w") as f:
            f.write(data[5])
        await ctx.send("```ini\nHere is your personal Entries text file {}:\n```".format(self.getDisplayName(ctx)))
        await ctx.send(file=discord.File(f"textfiles/{user_id}.txt"))
        os.remove(f"textfiles/{user_id}.txt")


    async def setFile(self, ctx, file):
        """
        Replaces the user's 'entries' attribute with the contents of their passed-in text file
        Creates a new row in the DB for the user if user_id is not recognized
        """ 
        user_id = self.getUserId(ctx)
        result = self.c.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()

        if not result:
            await self.createNewUser(ctx, file.read())
            await ctx.send("```ini\nEntries updated successfully!\n```")
            return

        new_data = file.read()
        try:
            self.c.execute("UPDATE users SET entries=? WHERE user_id=?", (new_data, user_id))
        except Exception as e:
            print('Error ('+str(currentframe().frameinfo.f_back.f_lineno)+'): ', e)
        self.conn.commit()
        await ctx.send("```ini\nEntries updated successfully!\n```")

    async def clearFile(self, ctx):
        """
        Removes all entries from the user's 'entries' attribute
        Creates a new row in the DB for the user if user_id is not recognized
        """ 
        user_id = self.getUserId(ctx)
        result = self.c.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()

        if not result:
            await self.createNewUser(ctx)
        else:
            data = ""
            self.c.execute("UPDATE users SET entries=? WHERE user_id=?", (data, user_id))
        await ctx.send("```ini\nEntries successfully cleared!\n```")

    async def resetFile(self, ctx):
        """
        Replaces the user's 'entries' attribute with the contents of entries_original.txt
        """ 
        user_id = self.getUserId(ctx)
        result = self.c.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
        
        if not result:
            await ctx.send("```bash\nCannot reset original Entries file. Create your own Entries file using '.new'.\n```")
        else:
            data = self.getDefaultEntries()
            self.c.execute("UPDATE users SET entries=? WHERE user_id=?", (data, user_id))
            await ctx.send("```ini\nEntries successfully reset!\n```")

    async def sortFile(self, ctx):
        """
        Sorts the user's 'entries' attribute alphabetically
        Creates a new row in the DB for the user if user_id is not recognized
        """ 
        user_id = self.getUserId(ctx)
        result = self.c.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
        
        if not result:
            data = self.getDefaultEntries()
            await self.createNewUser(ctx)
        else:
            data = result[5]

        with open(f"textfiles/{user_id}.txt", "w") as f:
            f.write(data)

        with open(f"textfiles/{user_id}.txt", "r+") as f:
            entries = f.readlines()
        os.remove(f"textfiles/{user_id}.txt")

        if await self.isFileEmpty(ctx, entries): return
        new_entries = [entry.strip()+"\n" if entry[-1].strip() !="\n" else entry.strip() for entry in entries if entry.strip() != "\n"]
        new_entries.sort(key=str.lower)
        new_entries_str = "\n".join(new_entries) + "\n"
        self.c.execute("UPDATE users SET entries=? WHERE user_id=?", (new_entries_str, user_id))
        await ctx.send("```ini\nEntries sorted successfully!\n```")

    async def cleanFile(self, ctx):
        """
        Filters out duplicate entries from the user's 'entries' attribute
        """ 
        user_id = self.getUserId(ctx)
        result = self.c.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
        
        if not result:
            await ctx.send("```bash\nNo duplicates in original Entries file. Create your own Entries file using '.new'.\n```")
        else:
            data = result[5]

        with open(f"textfiles/{user_id}.txt", "w") as f:
            f.write(data)

        with open(f"textfiles/{user_id}.txt", "r+") as f:
            entries = f.readlines()
        os.remove(f"textfiles/{user_id}.txt")

        if await self.isFileEmpty(ctx, entries): return
        entries = [entry.strip()+"\n" if entry[-1].strip() !="\n" else entry.strip() for entry in entries if entry.strip() != "\n"]
        new_entries = list(dict.fromkeys(entries))
        new_entries_str = "\n".join(new_entries) + "\n"
        self.c.execute("UPDATE users SET entries=? WHERE user_id=?", (new_entries_str, user_id))

        numdups = len(entries) - len(new_entries)
        if numdups == 0:
            await ctx.send("```ini\nNo duplicates in personal Entries to remove.\n```")
        else:
            await ctx.send("```ini\n[{}] duplicates in Entries removed successfully {}!\n```".format(numdups, self.getDisplayName(ctx)))

    def getUserId(self, ctx):
        return ctx.author.id

    def getDisplayName(self, ctx):
        return ctx.author.display_name

    def getUsername(self, ctx):
        return ctx.author.name

    def getDiscriminator(self, ctx):
        return ctx.author.discriminator

    def getServerName(self, ctx):
        return ctx.guild.name

    def getDefaultEntries(self):
        with open('textfiles/entries_original.txt', 'r') as f:
            return f.read()

    async def isFileEmpty(self, ctx, entries):
        clean_entries = [entry for entry in entries if entry.strip() != "\n"]
        if not clean_entries:
            await ctx.send("```ini\nThere are no entries to choose from. Use '.addentry <entry1>/<entry2>/...' or '.setfile <file.txt>' to add entries!\n```")
            return True
        return False