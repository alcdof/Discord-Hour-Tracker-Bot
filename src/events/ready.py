import discord

def register_ready_event(bot, tree, guild_id):

    @bot.event
    async def on_ready():
        await tree.sync(guild=discord.Object(id=guild_id))
        print("Bot successfully initialized.")