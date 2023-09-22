import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    gc = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        gc += 1
    print("MCUSSR Black Guard is in " + str(gc) + " guilds.")
    print("Online!")


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("pong")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = str(message.content)
    msg.lower

    # among detector
    if "among" in msg:
        await message.channel.send('"among"')
        await message.channel.send(
            "https://tenor.com/view/among-us-sus-yhk-among-twerk-among-us-twerk-gif-23335803"
        )

    # among us detector
    if "among us" in msg:
        await message.channel.send('"among us"')
        await message.channel.send(
            "https://tenor.com/view/among-us-sus-yhk-among-twerk-among-us-twerk-gif-23335803"
        )

    # sus detector
    if "sus" in msg:
        await message.channel.send('"sus"')
        await message.channel.send(
            "https://tenor.com/view/among-us-sus-yhk-among-twerk-among-us-twerk-gif-23335803"
        )


bot.run("MTE1NDg5MTY5MjM4NjgyODM5OQ.GbVf7I.7RZHLaF-_5VsQEaf79yBuCgOOGo5WdhPOC0WB8")
