import discord
import datetime
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents)
cont = 0


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

times = {}

@bot.event
async def on_ready():
    print("Bot successfully initialized.")

# ping
@bot.command()
async def ping(ctx):
    ping = round(bot.latency * 1000)
    await ctx.reply(f"Pong!\t🏓\t{ping} ms")

#contador simples: aumenta e diminui
@bot.command()
async def contador(ctx, action=None, value: int=None):
    global cont

    if action == "inc":
        if value is None:
            cont += 1
        else:
            cont += value

    elif action == "sub":
        if value is None:
            cont -= 1
        else:
            cont -= value

    elif action == "reset":
        cont = 0

    await ctx.reply(f"Counter: {cont}")

# limpa o chat
@bot.command()
async def clear(ctx, value: int=10, user: discord.Member=None):
    def check(msg):
        return msg.author == user
    
    if user is None:
        deleted = await ctx.channel.purge(limit=value)
    else: 
        deleted = await ctx.channel.purge(limit=value, check=check)

    await ctx.send(f"{len(deleted)} deleted messages.")


# entra no canal em que o usuário está
@bot.command()
async def connect(ctx):
    if ctx.author.voice is None:
        await ctx.reply(f"You need to be on a voice chat.")
        return
    
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.reply(f"I successfully joined the **{channel}** channel!")

# sai do canal em que o usuário está
@bot.command()
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.reply(f"I'm not on a voice channel.")
        return

    channel = ctx.author.voice.channel

    await ctx.voice_client.disconnect()
    await ctx.reply(f"I successfully left the **{channel}** channel!")

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
@bot.command()
async def time(ctx):
    if ctx.author.id not in times:
        await ctx.reply("You've not entered any voice chat recently.")
        return
    
    now = datetime.datetime.now()
    entryTime = times[ctx.author.id]

    time = now - entryTime
    total_seconds = int(time.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60    

    # TODO: traduzir isso dps, que preguiça
    if hours > 0:
        if minutes > 0:
            if seconds > 0:
                await ctx.reply(f"You have been in the channel for {hours}h, {minutes}min and {seconds}s.")
            else:
                await ctx.reply(f"You have been in the channel for {hours}h and {minutes}min.")
        else:
            if seconds > 0:
                await ctx.reply(f"You have been in the channel for {hours}h and {seconds}s.")
            else:
                await ctx.reply(f"You have been in the channel for {hours}h.")
    else:
        if minutes > 0:
            if seconds > 0:
                await ctx.reply(f"You have been in the channel for {minutes}min and {seconds}s.")
            else:
                await ctx.reply(f"You have been in the channel for {minutes}min.")
        else:
            if seconds > 0:
                await ctx.reply(f"You have been in the channel for {seconds}s.")
            else:
                await ctx.reply("You have just entered the channel.")


bot.run(TOKEN)