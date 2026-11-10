import discord
from src.services.time_tracker import get_elapsed_time


def register_commands(tree, guild_id):

    guild = discord.Object(id=guild_id)

    @tree.command(name="join", description="the bot joins the voice channel.", guild=guild)
    async def join(interaction: discord.Interaction):

        if interaction.user.voice is None:
            await interaction.response.send_message(
                "You need to be on a voice chat."
            )
            return

        channel = interaction.user.voice.channel

        await channel.connect()

        await interaction.response.send_message(
            f"I successfully joined the **{channel}** channel!"
        )

    @tree.command(name="leave", description="the bot leaves the voice channel.", guild=guild)
    async def leave(interaction: discord.Interaction):

        if interaction.guild.voice_client is None:
            await interaction.response.send_message(
                "I'm not on a voice channel."
            )
            return

        channel = interaction.guild.voice_client.channel

        await interaction.guild.voice_client.disconnect()

        await interaction.response.send_message(
            f"I successfully left the **{channel}** channel!"
        )

    @tree.command(name="time", description="shows time spent in a voice channel.", guild=guild)
    async def time(interaction: discord.Interaction):

        elapsed = get_elapsed_time(interaction.user.id)

        if elapsed is None:
            await interaction.response.send_message(
                "You've not entered any voice chat recently."
            )
            return

        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []

        if hours:
            parts.append(f"{hours}h")

        if minutes:
            parts.append(f"{minutes}min")

        if seconds:
            parts.append(f"{seconds}s")

        if not parts:
            parts.append("0s")

        await interaction.response.send_message(
            f"You have been in the channel for {' '.join(parts)}."
        )