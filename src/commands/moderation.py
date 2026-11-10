import discord
from discord import app_commands
from typing import Optional


def register_commands(tree, guild_id):

    guild = discord.Object(id=guild_id)

    @tree.command(name="clear", description="clears the chat.", guild=guild)
    @app_commands.describe(
        value="how many messages to delete",
        user="which user to delete messages"
    )
    async def clear(
        interaction: discord.Interaction,
        value: Optional[int] = 10,
        user: Optional[discord.Member] = None
    ):
        await interaction.response.defer()

        interaction_message = await interaction.original_response()

        def check(msg):
            if msg.id == interaction_message.id:
                return False

            if user is None:
                return True

            return msg.author == user

        deleted = await interaction.channel.purge(
            limit=value,
            check=check
        )

        await interaction.followup.send(
            f"{len(deleted)} deleted messages.",
            ephemeral=True
        )