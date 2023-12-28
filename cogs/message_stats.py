import io
from datetime import datetime, timedelta

import discord
import pytz

from discord.ext import commands

import matplotlib.pyplot as plt

from mongo_db import MongoDB


def get_hours_from_current():
    current_hour = datetime.now().hour
    return [(current_hour + i) % 24 for i in range(24)]


class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = MongoDB()

    @commands.command("message_stats")
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
                        "hour": {"$hour": "$timestamp"},
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1, "_id.hour": 1}
            }
        ]

        result = list(self.db.aggregate('messages', pipeline))

        timezone = pytz.timezone('Europe/Berlin')
        past_hours = get_hours_from_current()
        message_count = [0] * 24

        for message in result:
            date = datetime(message['_id']['year'],
                            message['_id']['month'],
                            message['_id']['day'],
                            message['_id']['hour'])

            result_hour = date.replace(tzinfo=pytz.utc).astimezone(timezone).hour
            index = past_hours.index(result_hour)
            message_count[index] = message['count']

        plt.figure(figsize=(10, 5))
        plt.bar([str(hour) for hour in past_hours], message_count, color='blue')

        plt.xlabel('Time')
        plt.ylabel('Messages')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        byte_array = buffer.getvalue()
        buffer.close()

        await ctx.send(file=discord.File(io.BytesIO(byte_array), 'image.png'))


async def setup(bot):
    await bot.add_cog(StatsCog(bot))
