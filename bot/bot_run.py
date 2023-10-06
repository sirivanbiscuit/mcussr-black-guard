import discord
from discord.ext import commands
from passives import Passives
from commands import Commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)

## CHANGE IF NEW TOKEN PATH
token = "mcussr-black-guard/token/token.mcussr"


# Initializations
@bot.event
async def on_ready():
    # Terminal Messages
    print("The Black Guard is active in the following guilds:")
    gc = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        gc += 1
    print("Online!")

    # Status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="your wretched soul"
        )
    )

    await bot.add_cog(Passives(bot))
    await bot.add_cog(Commands(bot))


# Fetch token and run:
if __name__ == "__main__":
    bot.run(open(token).read())
