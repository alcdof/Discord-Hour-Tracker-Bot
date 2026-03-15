import discord
import datetime
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
from typing import Optional
import google.generativeai as genai


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-flash-latest")

intents = discord.Intents.all()

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)
GUILD_ID = int(os.getenv("GUILD_ID"))

@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Bot successfully initialized.")

cont = 0
times = {}

# hello
@tree.command(
        name="hello",
        description="the bot greets you.",
        guild=discord.Object(id=GUILD_ID)
)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!  👋")

# ping
@tree.command(
        name="ping",
        description="the bot tells you what is the latency of the server.",
        guild=discord.Object(id=GUILD_ID)
)
async def ping(interaction: discord.Interaction):
    ping = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong!\t🏓\t{ping} ms")

#contador simples: aumenta e diminui
@tree.command(
        name="counter",
        description="a simple counter. for all users.",
        guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(
    action="increment (inc), decrement (dec) or reset (reset) the counter",
    value="how many times to increment/decrement"
)
async def counter(
    interaction: discord.Interaction, 
    action: Optional[str]=None, 
    value: Optional[int]=None
):
    global cont
    
    if action == "inc":
        if value is None:
            cont += 1
        else:
            cont += value
    elif action == "dec":
        if value is None:
            cont -= 1
        else:
            cont -= value
    elif action == "reset":
        cont = 0
    
    await interaction.response.send_message(f"Counter: {cont}")

# limpa o chat
@tree.command(
        name="clear",
        description="clears the chat.",
        guild=discord.Object(id=GUILD_ID)
)
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
    
    deleted = await interaction.channel.purge(limit=value, check=check)

    await interaction.followup.send(
        f"{len(deleted)} deleted messages.",
        ephemeral=True
        )

# entra no canal em que o usuário está
@tree.command(
        name="join",
        description="the bot joins the voice channel.",
        guild=discord.Object(id=GUILD_ID)
)
async def join(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("You need to be on a voice chat.")
        return
    
    channel = interaction.user.voice.channel
    await channel.connect()
    await interaction.response.send_message(f"I successfully joined the **{channel}** channel!")

# sai do canal em que o usuário está
@tree.command(
        name="leave",
        description="the bot leaves the voice channel.",
        guild=discord.Object(id=GUILD_ID)
)
async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client is None:
        await interaction.response.send_message(f"I'm not on a voice channel.")
        return

    channel = interaction.user.voice.channel

    await interaction.guild.voice_client.disconnect()
    await interaction.response.send_message(f"I successfully left the **{channel}** channel!")

# contador de tempo
@bot.event
async def on_voice_state_update(member, before, after):
    # entrou no canal -> inicia contador
    if before.channel is None and after.channel is not None:
        times[member.id] = datetime.datetime.now()

    # saiu do canal -> pausa contador
    if before.channel is not None and after.channel is None:
        times.pop(member.id, None)

# pede o tempo de permanência em um canal
# TODO: implementar sistema de tempo em cada canal
@tree.command(
        name="time",
        description="the bot shows you the time spent in a determined voice channel.",
        guild=discord.Object(id=GUILD_ID)
)
async def time(interaction: discord.Interaction):
    if interaction.author.id not in times:
        await interaction.response.send_message("You've not entered any voice chat recently.")
        return
    
    now = datetime.datetime.now()
    entryTime = times[interaction.author.id]

    time = now - entryTime
    total_seconds = int(time.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60  

    if hours > 0:
        if minutes > 0:
            if seconds > 0:
                await interaction.response.send_message(f"You have been in the channel for {hours}h, {minutes}min and {seconds}s.")
            else:
                await interaction.response.send_message(f"You have been in the channel for {hours}h and {minutes}min.")
        else:
            if seconds > 0:
                await interaction.response.send_message(f"You have been in the channel for {hours}h and {seconds}s.")
            else:
                await interaction.response.send_message(f"You have been in the channel for {hours}h.")
    else:
        if minutes > 0:
            if seconds > 0:
                await interaction.response.send_message(f"You have been in the channel for {minutes}min and {seconds}s.")
            else:
                await interaction.response.send_message(f"You have been in the channel for {minutes}min.")
        else:
            if seconds > 0:
                await interaction.response.send_message(f"You have been in the channel for {seconds}s.")
            else:
                await interaction.response.send_message("You have just entered the channel.")

@tree.command(
    name="ai",
    description="ask Gemini.",
    guild=discord.Object(id=GUILD_ID)
)
async def ai(interaction: discord.Interaction, question: str):
    
    await interaction.response.defer()

    response = model.generate_content(question)

    await interaction.followup.send(response.text)

bot.run(TOKEN)