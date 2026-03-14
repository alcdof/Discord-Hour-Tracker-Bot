import discord
import datetime
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents)
cont = 0
times = {}

@bot.event
async def on_ready():
    print("Bot inicializado com sucesso.")

# ping
@bot.command()
async def ping(ctx):
    ping = round(bot.latency * 1000)
    await ctx.reply(f"Pong!    🏓    {ping} ms")

# salve (teste)
@bot.command()
async def salve(ctx):
    await ctx.reply("Salve!")

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
        cont == 0

    await ctx.reply(f"Contador: {cont}")

# limpa o chat
@bot.command()
async def clear(ctx, value: int=10, user: discord.Member=None):
    def check(msg):
        return msg.author == user
    
    if user is None:
        deletadas = await ctx.channel.purge(limit=value)
    else: 
        deletadas = await ctx.channel.purge(limit=value, check=check)

    await ctx.send(f"{len(deletadas)} mensagens apagadas.")


# entra no canal em que o usuário está
@bot.command()
async def connect(ctx):
    if ctx.author.voice is None:
        await ctx.reply(f"Você precisa estar em um canal de voz.")
        return
    
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.reply(f"Entrei com sucesso no canal **{channel}**!")

# sai do canal em que o usuário está
@bot.command()
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.reply(f"Eu não estou em um canal de voz.")
        return

    channel = ctx.author.voice.channel

    await ctx.voice_client.disconnect()
    await ctx.reply(f"Saí do canal **{channel}** com sucesso!")


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
        await ctx.reply("Você não entrou em um canal recentemente.")
        return
    
    now = datetime.datetime.now()
    entryTime = times[ctx.author.id]

    time = now - entryTime
    total_seconds = int(time.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60    

    if hours > 0:
        if minutes > 0:
            if seconds > 0:
                await ctx.reply(f"Você está no canal há {hours}h, {minutes}min e {seconds}s.")
            else:
                await ctx.reply(f"Você está no canal há {hours}h e {minutes}min.")
        else:
            if seconds > 0:
                await ctx.reply(f"Você está no canal há {hours}h e {seconds}s.")
            else:
                await ctx.reply(f"Você está no canal há {hours}h.")
    else:
        if minutes > 0:
            if seconds > 0:
                await ctx.reply(f"Você está no canal há {minutes}min e {seconds}s.")
            else:
                await ctx.reply(f"Você está no canal há {minutes}min.")
        else:
            if seconds > 0:
                await ctx.reply(f"Você está no canal há {seconds}s.")
            else:
                return


bot.run("Seu_Token")