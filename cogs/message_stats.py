import io
from datetime import datetime, timedelta

import discord
from discord.ext import commands

import matplotlib.pyplot as plt

from mongo_db import MongoDB


class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = MongoDB()

    @commands.command("stats")
    async def get_stats(self, ctx, member: discord.Member):
        past_24_hours = datetime.utcnow() - timedelta(hours=24)
        current_time = datetime.utcnow()

        results = self.db.find('messages', {
            "author_id": member.id,
            "timestamp_field": {
                "$gte": past_24_hours,
                "$lte": current_time
            }
        })

        for result in results:
            pass

        hours = list(range(1, 25))
        steps_walked = [5, 7, 9, 6, 8, 5, 4, 7, 9, 10, 12, 14, 15, 13, 11, 10, 9, 7, 6, 5, 4, 3, 2, 1]
        plt.plot(hours, steps_walked, color='blue')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        byte_array = buffer.getvalue()

        buffer.close()

        await ctx.send(file=discord.File(io.BytesIO(byte_array), 'image.png'))


async def setup(bot):
    await bot.add_cog(StatsCog(bot))
