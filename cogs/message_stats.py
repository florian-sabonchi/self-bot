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
    async def get_stats(self, ctx, author_id: int):
        past_24_hours = datetime.utcnow() - timedelta(hours=24)

        query = {
            "author_id": author_id,
            "timestamp": {"$gte": past_24_hours}
        }

        pipeline = [
            {"$match": query},
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$timestamp"},
                        "month": {"$month": "$timestamp"},
                        "day": {"$dayOfMonth": "$timestamp"},
                        "hour": {"$hour": "$timestamp"}
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1, "_id.hour": 1}
            }
        ]

        result = list(self.db.aggregate('messages', pipeline))

        hours = []
        message_count = []

        for message in result:
            hours.append(str(message['_id']['hour']))
            message_count.append(message['count'])

        plt.bar(hours, message_count, color='blue')

        plt.xlabel('Time')
        plt.ylabel('messages')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        byte_array = buffer.getvalue()
        buffer.close()

        await ctx.send(file=discord.File(io.BytesIO(byte_array), 'image.png'))


async def setup(bot):
    await bot.add_cog(StatsCog(bot))
