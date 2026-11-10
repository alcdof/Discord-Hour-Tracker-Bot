import discord
from discord import app_commands


def register_commands(tree, bot, guild_id):

    guild = discord.Object(id=guild_id)

    @tree.command(name="hello", description="the bot greets you.", guild=guild)
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Hello, {interaction.user.mention}! 👋"
        )

    @tree.command(name="ping", description="the bot tells you the latency.", guild=guild)
    async def ping(interaction: discord.Interaction):
        latency = round(bot.latency * 1000)
        await interaction.response.send_message(f"Pong! 🏓 {latency} ms")