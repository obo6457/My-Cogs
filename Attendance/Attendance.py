from __future__ import print_function
from redbot.core import Config
from redbot.core import commands
import discord
import gspread
import time
import typing
from oauth2client.service_account import ServiceAccountCredentials


class Attendance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_role("Officer")
    async def LogEvent(self, ctx, channel: typing.Optional[discord.VoiceChannel], *guests: discord.Member):
        """Increments members in the event channel's event score, minus guests"""
        if not channel:
            channel = ctx.guild.get_channel(360785714339643392)
        vch = channel
        Guest_Arr = []
        error = False
        for member in guests:
            if member:
                Guest_Arr.append(str(member))
            else:
                await ctx.send(str(member) + " is not a member")
                error = True
                break

        if not error:
            Member_Array = []
            mem = vch.members
            for x in mem:
                Member_Array.append(str(x))
            print(Member_Array)
            print(Guest_Arr)
            for Guest in Guest_Arr:
                if Guest in Member_Array:
                    Member_Array.remove(Guest)

            print(Member_Array)
            if len(Member_Array) == 0:
                await ctx.send("Only Guests/Empty Channel")
            else:
                scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
                Creds = ServiceAccountCredentials.from_json_keyfile_name("GCreds.json", scope)
                gc = gspread.authorize(Creds)
                wks = gc.open("GoA Guild Roster").sheet1
                for member in Member_Array:
                    await ctx.send(member)
                    try:
                        cell = wks.find(member)
                    except gspread.exceptions.CellNotFound:
                        await ctx.send(str(member) + " could not be found on the roster")
                        continue
                    if cell != "" and cell.col == 4:
                        col = cell.col
                        row = cell.row
                        AC = wks.cell(row, 10)
                        if AC.value == "":
                            ACV = 0
                        else:
                            ACV = float(AC.value)
                        #print(ACV)
                        ACV = ACV+1
                        #print(ACV)
                        wks.update_cell(AC.row, AC.col, ACV)
                        d1 = time.strftime("%d/%m/%Y")
                        #print(wks.cell(row, 11))
                        wks.update_cell(AC.row, 11, d1)
                    else:
                        await ctx.send(str(member) + " could not be found on the roster")
