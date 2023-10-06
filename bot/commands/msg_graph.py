import discord
from discord.ext import commands

from table2ascii import table2ascii as t2a
import matplotlib.pyplot as plt
import io

# If this doesn't exist you should probably make the folder here
GRAPH_CACHE_PATH = "mcussr-black-guard/bot/_graphcache/"
GRAPH = "graph.png"

# Contains all message graph commands
class MsgGraphCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    """
    An advanced command to generate graphs based on the entire server's message history. Can target specific words and phrases and calculate their occurence over the server's history.
    """
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

        # Collect message history
        await ctx.channel.send(
            "Collecting the entirety of this channels's message history..."
            )
        daily = {}
        msgs = []
        date, prev_date = None, None
        view, view_milestone = 0, 10
        async for m in ctx.channel.history(limit=None): 
            msgs.append(m)
            view += 1
            if view == view_milestone:
                view_milestone *= 5 if str(view_milestone)[0]=='1' else 2
                await ctx.channel.send(f"Scanned {view} messages...")
        
        # Get dict of all valid msgs
        await ctx.channel.send("Message history retrieved, building graph data...")
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
        plt.savefig(GRAPH_CACHE_PATH+GRAPH)
        plt.close()

        # EMBED ARGS
        colour = 0xff0000
        title = f"Messages in {ctx.channel.name}:"
        embed = discord.Embed(title=title, colour=colour)
        with open(GRAPH_CACHE_PATH+GRAPH, 'rb') as f:
            image = discord.File(io.BytesIO(f.read()), filename=GRAPH)
        
        # Send graph
        await ctx.send(
            "**Here is a graph of this channel's entire message history:**"
            +"\n(It's the best I can do)")
        await ctx.send(
            file=image, 
            embed=embed.set_image(url='attachment://'+GRAPH))


    """
    Error catcher for incorrect number of args for $msgplot.
    """
    @msgplot.error
    async def msgplot_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("The command `msgplot` requires three arguments:"
                           +"\n- `arg1`: graph type"
                           +"\n- `arg2`: moving average (`/null` for none)"  
                           +"\n- `arg3`: target string (`/null` for none)")
    