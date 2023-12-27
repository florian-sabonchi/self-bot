import asyncio
import os

from discord.ext import commands

initial_extensions = [
    'cogs.message_listener',
    'cogs.message_stats',
]

bot = commands.Bot(command_prefix='!', self_bot=True)


async def load_extensions():
    for extension in initial_extensions:
        await bot.load_extension(extension)


async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('DISCORD_TOKEN'))


asyncio.run(main())
