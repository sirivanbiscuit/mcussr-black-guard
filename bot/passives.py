import discord
from discord.ext import commands


class Passives(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Automatic message responses
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        msg = str(message.content)
        msg.lower

        # 'among' detector
        if "among" in msg:
            await message.channel.send('"among us"' if "among us" in msg else '"among"')
            await message.channel.send(
                "https://tenor.com/view/among-us-sus-yhk-among-twerk-among-us-twerk-gif-23335803"
            )

        # 'sus' detector
        elif "sus" in msg:
            await message.channel.send('"sus"')
            await message.channel.send(
                "https://tenor.com/view/among-us-sus-yhk-among-twerk-among-us-twerk-gif-23335803"
            )
