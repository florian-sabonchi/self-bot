import os

from discord.ext import commands

from mongo_db import MongoDB


class MessageListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = MongoDB()

    @commands.Cog.listener()
    async def on_message(self, message):
        server_id = message.guild.id
        if server_id == int(os.getenv("SERVER_ID")):
            document = {
                "author": message.author.name,
                "author_id": message.author.id,
                "content": message.content,
                "channel": message.channel.name,
                "timestamp": message.created_at
            }
            self.db.insert("messages", document)

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.bot.user.name)


async def setup(bot):
    await bot.add_cog(MessageListener(bot))
