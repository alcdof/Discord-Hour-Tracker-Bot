import discord
from discord import app_commands

from src.config.settings import GUILD_ID

from src.commands.general import register_commands as register_general
from src.commands.counter import register_commands as register_counter
from src.commands.moderation import register_commands as register_moderation
from src.commands.voice import register_commands as register_voice
from src.commands.ai import register_commands as register_ai

from src.events.ready import register_ready_event
from src.events.voice_state import register_voice_event


intents = discord.Intents.all()

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

register_general(tree, bot, GUILD_ID)
register_counter(tree, GUILD_ID)
register_moderation(tree, GUILD_ID)
register_voice(tree, GUILD_ID)
register_ai(tree, GUILD_ID)

register_ready_event(bot, tree, GUILD_ID)
register_voice_event(bot)