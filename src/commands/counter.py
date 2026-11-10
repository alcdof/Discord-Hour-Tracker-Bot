import discord
from discord import app_commands
from typing import Optional


def register_commands(tree, guild_id):

    guild = discord.Object(id=guild_id)
    counter_value = 0

    @tree.command(name="counter", description="a simple counter for all users.", guild=guild)
    @app_commands.describe(
        action="increment (inc), decrement (dec) or reset (reset)",
        value="how many times to increment/decrement"
    )
    async def counter(
        interaction: discord.Interaction,
        action: Optional[str] = None,
        value: Optional[int] = None
    ):
        nonlocal counter_value

        if action == "inc":
            counter_value += value if value is not None else 1

        elif action == "dec":
            counter_value -= value if value is not None else 1

        elif action == "reset":
            counter_value = 0

        await interaction.response.send_message(f"Counter: {counter_value}")