import discord
import json
from discord.ext import commands

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} está conectado a Discord!')

def cargar_puntuaciones():
    try:
        with open("puntuaciones.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_puntuaciones(puntuaciones):
    with open("puntuaciones.json", "w") as f:
        json.dump(puntuaciones, f)

puntuaciones = cargar_puntuaciones()

@bot.command(name="registrar")
async def registrar(ctx, user: discord.Member):
    if user.id in puntuaciones:
        puntuaciones[user.id] += 0
    else:
        puntuaciones[user.id] = 0

    guardar_puntuaciones(0)  
    await ctx.send(f"{user.name} ahora tiene {puntuaciones[user.id]} puntos.")

@bot.command(name="puntuaciones")
async def ver_puntuaciones(ctx):
    if puntuaciones:
        ranking = ""
        sorted_puntuaciones = sorted(puntuaciones.items(), key=lambda x: x[1], reverse=True)
        for user_id, puntos in sorted_puntuaciones:
            user = bot.get_user(int(user_id))
            if user:
                ranking += f"{user.mention}: {puntos}\n"
            else:
                ranking += f"Usuario ID {user_id}: {puntos}\n"
        await ctx.send(f"**Tabla de Puntuaciones:**\n{ranking}")
    else:
        await ctx.send("No hay puntuaciones registradas aún.")

@bot.command(name="resetear")
@commands.has_permissions(administrator=True)
async def resetear_puntuacion(ctx, user: discord.Member):
    user_id = str(user.id)
    puntuaciones[user_id] = 0
    guardar_puntuaciones(puntuaciones)
    await ctx.send(f"Se ha reseteado la puntuación de {user.name}.")
    
@bot.event
async def on_message(message):
    puntos_correctos = 0
    filas_erroneas = 1
    if message.author == bot.user:
        return

    if message.channel.id == 1270550504744947794:
        if message.content.startswith("Connections"):
            lines = message.content.strip().split('\n')
            if len(lines) < 3:
                await message.channel.send(f"{message.author.mention}, el formato del puzzle es incorrecto.")
                return
            filas = lines[2:]

            for fila in filas:
                fila = fila.strip()
                if len(fila) != 4:
                    filas_erroneas += 1
                    continue
                if all(emoji == fila[0] for emoji in fila):
                    puntos_correctos += 10 
                else:
                    filas_erroneas += 1
                    
            puntaje_total = round(puntos_correctos / filas_erroneas, 2)
            if str(message.author.id) in puntuaciones:
                puntuaciones[str(message.author.id)] += puntaje_total
            else:
                puntuaciones[str(message.author.id)] = puntaje_total

            guardar_puntuaciones(puntuaciones)

            await message.channel.send(f"{message.author.mention} ha obtenido **{puntaje_total}** punto(s)")

    await bot.process_commands(message)

# Iniciar el bot
bot.run('MTI5MTAyNjQ2MDYwOTM0NzYzNg.GwpOLu.MKp0ExRkPjL3lJxXfb4mxv9GSgU66Csk5nHpZs')