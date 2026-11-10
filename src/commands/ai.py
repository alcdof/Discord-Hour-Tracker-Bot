import discord
from src.services.gemini import generate_response


def register_commands(tree, guild_id):

    guild = discord.Object(id=guild_id)

    @tree.command(name="ai", description="ask Gemini.", guild=guild)
    async def ai(interaction: discord.Interaction, question: str):

        await interaction.response.defer()

        response = generate_response(question)

        await interaction.followup.send(response)