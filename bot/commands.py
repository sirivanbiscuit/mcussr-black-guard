import discord
import string
from table2ascii import table2ascii as t2a
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command()
    async def msgplot(self, ctx, arg1:str, arg2:str, arg3:str):
        # Check arg1
        bar = arg1=='bar'
        line = arg1=='line'
        if not bar and not line: 
            await ctx.send("Invalid argument pass: `arg1`\n"
                           +"- arg must specify valid graph type")
            return
        
        # Check arg2
        null_avg = arg2=='/null'
        if not null_avg:
            await ctx.send("Invalid argument pass: `arg2`\n"
                           +"- arg must specify valid moving average")
            return 
        
        # Check arg3
        targ = arg3.lower()
        null_targ = arg3=='/null'

        import numpy as np
        import matplotlib.pyplot as plt
        import io

        # Get dict of all valid msgs
        await ctx.channel.send(
            "Collecting the entirety of this channels's message history..."
            )
        daily = {}
        date, prev_date = None, None
        view, view_milestone = 0, 10
        msgs = [m async for m in ctx.channel.history(limit=None)]
        for i in range(len(msgs)-1, -1, -1):
            msg = msgs[i]
            prev_date = msg.created_at.strftime("%d/%m/%Y")
            valid_str = null_targ or targ.lower() in str(msg.content).lower()
            if valid_str:
                if date != prev_date: 
                    date = prev_date+""
                    daily[date] = 1
                else:
                    daily[date] += 1
            view += 1
            if view == view_milestone:
                view_milestone *= 5 if str(view_milestone)[0]=='1' else 2
                await ctx.channel.send(f"Scanned {view} messages...")

        # Get graph from dict
        plt.figure()
        plt.style.use('default')
        keys = list(daily.keys())
        vals = list(daily.values())
        if bar:
            plt.bar(keys, vals)
        elif line:
            plt.plot(keys, vals)
        plt.xticks([])
        plt.grid()
        plt.savefig('graph.png')
        plt.close()

        with open('graph.png', 'rb') as f:
            file = io.BytesIO(f.read())
        
        # Send graph
        embed = discord.Embed(title=f"Messages in {ctx.channel.name}:", colour=0xff0000)
        image = discord.File(file, filename='graph.png')
        embed.set_image(url=f'attachment://graph.png')
        await ctx.send("**Here is a graph of this channel's entire message history:**"
                       +"\n(It's the best I can do)")
        await ctx.send(file=image, embed=embed)


    @msgplot.error
    async def msgplot_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("The command `msgplot` requires three arguments:"
                           +"\n- `arg1`: graph type"
                           +"\n- `arg2`: moving average (`/null` for none)"  
                           +"\n- `arg3`: target string (`/null` for none)")
    


    def hello(self) -> dict:
        return {}

    @commands.command()
    async def msgdata(self, ctx, data: int, check_for: str):
        await ctx.channel.send(
            "Collecting the entirety of this channels's message history..."
            )
        
        daily = {}
        date = None
        check = None
        view = 0
        view_milestone = 10
        n = check_for=='/null'
        async for msg in ctx.channel.history(limit=None):
            check = msg.created_at.strftime("%d/%m/%Y")
            if date != check: 
                if (n) or (targ.lower() in str(msg.content).lower()):
                    date = check+""
                    daily[date] = 1
            else: 
                if (n) or (targ.lower() in str(msg.content).lower()):
                    daily[date] += 1
            view += 1
            if view == view_milestone:
                view_milestone *= 5 if str(view_milestone)[0]=='1' else 2
                await ctx.channel.send(f"Scanned {view} messages...")
        
        output = t2a(
            header=[ "Date", 'Messages' ],
            body=[[i, daily[i]] for i in daily]
        )

        await ctx.send(f"```\n{output}\n```")
    