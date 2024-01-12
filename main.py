import discord
from discord.ext import commands
from discord import Intents
from fuzzywuzzy import fuzz
from dotenv import load_dotenv
import os
import sys

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

def yukle():
    soru_cevap = {}
    with open("sc.txt", "r") as dosya:
        satirlar = dosya.readlines()
        for satir in satirlar:
            parcalar = satir.strip().split(":")
            if len(parcalar) == 2:
                soru_cevap[parcalar[0].lower()] = parcalar[1]
    return soru_cevap

def en_yakin_soru(soru, soru_cevap):
    en_yakin = max(soru_cevap.keys(), key=lambda k: fuzz.ratio(soru, k))
    return en_yakin

def is_yapimci(ctx):
    return ctx.message.author.id == 880821273289179147 

@bot.event
async def on_ready():
    print(f'{bot.user.name} HAZIRIM EFENDİM')

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        soru = message.content.lower()
        soru_cevap = yukle()

        if soru in soru_cevap:
            await message.channel.send(soru_cevap[soru])
        else:
            en_yakin = en_yakin_soru(soru, soru_cevap)
            en_yakin_cevap = soru_cevap.get(en_yakin)
            await message.channel.send(f"{en_yakin_cevap}")

    await bot.process_commands(message)

@bot.command(name='mami')
async def mami(ctx, *, soru=None):
    if not is_yapimci(ctx):
        await ctx.send("Bu komutu sadece yapımcı kullanabilir.")
        return

    if soru is None:
        await ctx.send('Soru ve cevap belirtilmedi.')
        return

    soru = soru.lower()
    soru_cevap = yukle()

    parcalar = soru.split(":")
    if len(parcalar) == 2:
        soru_cevap[parcalar[0].strip().lower()] = parcalar[1].strip()
        with open("sc.txt", "a") as dosya:
            dosya.write(f"{parcalar[0].strip()}:{parcalar[1].strip()}\n")
        await ctx.send(f"{parcalar[0].strip()} sorusu ve cevabı eklendi.")
    else:
        await ctx.send('Geçerli bir soru:cevap formatı belirtmelisiniz.')

@bot.command(name='flym')
async def flym(ctx, *, soru=None):
    if soru is None:
        await ctx.send('HE! YARRAM')
        return

    soru = soru.lower()
    soru_cevap = yukle()

    if soru in soru_cevap:
        await ctx.send(soru_cevap[soru])
    else:
        en_yakin = en_yakin_soru(soru, soru_cevap)
        en_yakin_cevap = soru_cevap.get(en_yakin)
        await ctx.send(f"{en_yakin_cevap}")

@bot.command(name='kapan')
async def yeniden_basla(ctx):
    if not is_yapimci(ctx):
        await ctx.send("Bu komutu sadece yapımcı kullanabilir.")
        return

    await ctx.send("EMREDERSİNİZ EFENDİM")
    await bot.close()

bot.run(TOKEN)
