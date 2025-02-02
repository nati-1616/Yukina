import requests
import yt_dlp as ytdl
import random
from discord.ext import commands
import time
import requests
import psutil
import platform
import os
import yt_dlp
import shutil
import asyncio
import json
import subprocess
import discord
import git

# Configuración
BOT_TOKEN = 'MTI0NTU0NzcwOTg3NjkyODU0Mw.Gi1z35.dEi70uWfQs0427uCyXtPHy4isOB-Zpq4py4iFU'  # Reemplaza con tu token
PREFIX = '#'  # Prefijo de comandos

# Inicializar el cliente de Discord
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=PREFIX, intents=intents)

# Función para verificar progreso de descarga
def check_progress(id):
    while True:
        response = requests.get(f'https://p.oceansaver.in/ajax/progress.php?id={id}')
        data = response.json()
        if data['success'] and data['progress'] == 1000:
            return data['download_url']
        time.sleep(5)

# Evento cuando el bot está listo
@client.event
async def on_ready():
    print(f'Bot conectado como🌹{client.user}')

# Configuración de opciones de yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'downloads/%(title)s.%(ext)s',  # Carpeta donde se guardará el archivo
    'ffmpeg_location': '/usr/bin/ffmpeg'  # Ruta de ffmpeg en Replit
}

def descargar_audio(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        

# Comando para descargar música
@client.command()
async def play(ctx, *, query: str):
    if not query:
        await ctx.send("🎵 Escribe el nombre o link del video.")
        return

    # Usar yt-dlp para obtener los resultados de búsqueda
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with ytdl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if not info.get('entries'):
            await ctx.send("⚠️ No se encontraron resultados.")
            return

        video = info['entries'][0]
        video_url = video['url']

    try:
        # Obtener enlace de descarga de audio en MP3
        response = requests.get(f'https://p.oceansaver.in/ajax/download.php?format=mp3&url={video_url}&api=dfcb6d76f2f6a9894gjkege8a4ab232222')
        data = response.json()

        if not data['success']:
            raise Exception('No se pudo descargar.')

        download_url = check_progress(data['id'])
        await ctx.send(f"🎵 *{video['title']}*\n🔗 [Descargar Audio]({download_url})")
    except Exception as e:
        await ctx.send(f"❌ Error al descargar: {str(e)}")

# Comando para descargar video
@client.command()
async def video(ctx, *, query: str):
    if not query:
        await ctx.send("🎬 Escribe el nombre o link del video.")
        return

    # Usar yt-dlp para obtener los resultados de búsqueda
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with ytdl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if not info.get('entries'):
            await ctx.send("⚠️ No se encontraron resultados.")
            return

        video = info['entries'][0]
        video_url = video['url']

    try:
        # Obtener enlace de descarga de video en 720p
        response = requests.get(f'https://p.oceansaver.in/ajax/download.php?format=720&url={video_url}&api=dfcb6d76f2f6a9894gjkege8a4ab232222')
        data = response.json()

        if not data['success']:
            raise Exception('No se pudo descargar.')

        download_url = check_progress(data['id'])
        await ctx.send(f"🎬 *{video['title']}*\n🔗 [Descargar Video]({download_url})")
    except Exception as e:
        await ctx.send(f"❌ Error al descargar: {str(e)}")

# Comandos de moderación
@client.command()
async def ban(ctx, user: discord.User):
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ No tienes permisos.")
        return
    await ctx.guild.ban(user)
    await ctx.send(f"🔨 Usuario baneado: {user}")

@client.command()
async def kick(ctx, user: discord.User):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ No tienes permisos.")
        return
    await ctx.guild.kick(user)
    await ctx.send(f"👢 Usuario expulsado: {user}")

# Comando de juegos
@client.command()
async def dado(ctx):
    resultado = random.randint(1, 6)
    await ctx.send(f"🎲 Has sacado un **{resultado}**")

@client.command()
async def ball(ctx):
    respuestas = ["Sí", "No", "Tal vez", "Pregunta otra vez", "No lo sé"]
    respuesta = random.choice(respuestas)
    await ctx.send(f"🎱 Respuesta: {respuesta}")

# Comando de memes
@client.command()
async def meme(ctx):
    response = requests.get('https://meme-api.com/gimme')
    if response.status_code == 200:
        meme_url = response.json()['url']
        await ctx.send(meme_url)
    else:
        await ctx.send('❌ Error al obtener un meme.')

# Comando de información
@client.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! Latencia: {client.latency * 1000:.2f}ms')

# Comando para obtener el avatar de un usuario
@client.command()
async def avatar(ctx, user: discord.User = None):
    user = user or ctx.author
    await ctx.send(user.avatar_url)

# Comando para cambiar prefijo (opcional)
@client.command()
async def setprefix(ctx, new_prefix: str):
    global PREFIX
    PREFIX = new_prefix
    await ctx.send(f"✅ Prefijo cambiado a: {new_prefix}")

# comando para generar waifus
@client.command()
async def waifu(ctx):
    """Comando para generar una waifu aleatoria"""
    try:
        # Hacer la solicitud a la API de waifu.pics para obtener una waifu
        response = requests.get('https://api.waifu.pics/sfw/waifu')

        if response.status_code == 200:
            data = response.json()
            waifu_image_url = data['url']  # Obtén la URL de la imagen

            # Enviar la imagen de la waifu al canal
            await ctx.send(waifu_image_url)
        else:
            await ctx.send("❌ No se pudo obtener la imagen de waifu.")
    except Exception as e:
        await ctx.send(f"❌ Error al generar la waifu: {str(e)}")

#comando de descargar música 
@client.command()
async def download(ctx, url: str, media_type: str = 'audio'):
    """Comando para descargar audio o video de YouTube.
    
    Argumentos:
    url -- Enlace de YouTube.
    media_type -- 'audio' para descargar solo el audio, 'video' para descargar el video.
    """
    await ctx.send(f"🔽 Iniciando descarga de {media_type}...")

    # Definir opciones de yt-dlp dependiendo del tipo de medio
    if media_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif media_type == 'video':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'quiet': True,
        }
    else:
        await ctx.send("❌ Tipo de medio no válido. Usa 'audio' o 'video'.")
        return

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Descargar el archivo de YouTube
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)

            # Enviar el archivo descargado
            if media_type == 'audio':
                await ctx.send(f"🎵 Aquí tienes el audio de *{info_dict['title']}*:", file=discord.File(filename))
            elif media_type == 'video':
                await ctx.send(f"🎬 Aquí tienes el video de *{info_dict['title']}*:", file=discord.File(filename))
            
            # Borrar el archivo después de enviarlo
            os.remove(filename)

    except Exception as e:
        await ctx.send(f"❌ Error al descargar el archivo: {str(e)}")

#comando de info del bot
@client.command()
async def info(ctx):
    """Comando para obtener información del bot, como el uso de RAM, servidores y más."""
    
    # Obtener uso de RAM (memoria en MB)
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # En MB

    # Obtener información sobre el sistema
    system_info = platform.uname()

    # Obtener el número de servidores y canales
    guild_count = len(client.guilds)
    channel_count = sum(len(guild.text_channels) + len(guild.voice_channels) for guild in client.guilds)

    embed = discord.Embed(
        title="Información del Bot",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="Sistema", value=f"{system_info.system} {system_info.release} ({system_info.machine})", inline=False)
    embed.add_field(name="Versión de Python", value=f"{platform.python_version()}", inline=False)
    embed.add_field(name="Uso de RAM", value=f"{memory_usage:.2f} MB", inline=False)
    embed.add_field(name="Servidores", value=f"{guild_count} servidores", inline=False)
    embed.add_field(name="Canales", value=f"{channel_count} canales", inline=False)
    embed.add_field(name="Hosting", value="Replit", inline=False)  # O el nombre del hosting si es otro

    await ctx.send(embed=embed)

# Configuración del bot
OWNER_ID = 1252023555487567932  # Reemplaza con tu ID de Discord

# Función para verificar si el usuario es el dueño
def is_owner(ctx):
    return ctx.author.id == OWNER_ID

# Comando para reiniciar el bot
@client.command()
async def restart(ctx):
    """Reinicia el bot (Solo el owner)."""
    if not is_owner(ctx):
        await ctx.send("❌ No tienes permisos para ejecutar este comando.")
        return
    
    await ctx.send("🔄 Reiniciando el bot...")
    await client.close()  # Cierra el bot para que se reinicie en Replit automáticamente

# Comando para eliminar archivos innecesarios y mostrar cuántos eliminó
@client.command()
async def delai(ctx):
    """Elimina archivos almacenados que no sirven (Solo el owner)."""
    if not is_owner(ctx):
        await ctx.send("❌ No tienes permisos para ejecutar este comando.")
        return
    
    try:
        dirs_to_clean = ["temp", "logs", "cache"]  # Carpetas a limpiar
        total_deleted_files = 0
        total_deleted_folders = 0

        for directory in dirs_to_clean:
            if os.path.exists(directory):
                file_count = sum([len(files) for _, _, files in os.walk(directory)])  # Cuenta archivos en la carpeta
                shutil.rmtree(directory)
                total_deleted_files += file_count
                total_deleted_folders += 1
        
        await ctx.send(f"✅ Se eliminaron {total_deleted_folders} carpetas y {total_deleted_files} archivos innecesarios.")
    
    except Exception as e:
        await ctx.send(f"❌ Error al eliminar archivos: {str(e)}")

# Comando para eliminar sesiones activas innecesarias y mostrar cuántas eliminó
@client.command()
async def ds(ctx):
    """Elimina sesiones que no sirven (Solo el owner)."""
    if not is_owner(ctx):
        await ctx.send("❌ No tienes permisos para ejecutar este comando.")
        return
    
    try:
        session_files = ["session.data", "session.lock", "session.json"]
        deleted_files = []
        
        for file in session_files:
            if os.path.exists(file):
                os.remove(file)
                deleted_files.append(file)
        
        if deleted_files:
            await ctx.send(f"✅ Se eliminaron {len(deleted_files)} sesiones: {', '.join(deleted_files)}")
        else:
            await ctx.send("⚠️ No había sesiones activas para eliminar.")
    
    except Exception as e:
        await ctx.send(f"❌ Error al eliminar sesiones: {str(e)}")

# Diccionario de imágenes para los comandos
imagenes_comandos = {
    "info": "https://ibb.co/RTzbyCN2",
    "ping": "https://ibb.co/7tkRQdHQ",
    "ban": "https://ibb.co/sd9DFgrh",
    "kick": "https://ibb.co/LhC3xWx1",
    "mute": "https://ibb.co/nqYts6D5",
}

#informacion del owner
@client.command()
async def owner(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Solo el creador del bot puede usar este comando.")
        return

    embed = discord.Embed(
        title="👑 Creadora del Bot",
        description="Información de la persona que hizo posible este bot.",
        color=discord.Color.gold()
    )
    embed.set_thumbnail(url="https://ibb.co/RTzbyCN2")  # Cambia la imagen si quieres
    embed.add_field(name="👩‍💻 Nombre", value="Natalia Zuleta", inline=False)
    embed.add_field(name="📞 Contacto", value="+5592996077349", inline=False)
    embed.add_field(name="📌 Descripción", value="Soy la creadora de este bot y diseñadora quien edito el bot 💋❤️.", inline=False)
    
    await ctx.send(embed=embed)

# Lista de templates de memes disponibles
templates = [
    "drake/not_this/YES.png",
    "expanding_brain/Expandiendo/el/cerebro.png",
    "one_does_not/simply/NO.png",
    "why_though/por_que/NO.png",
    "condescending_wonka/Este/es/el/mejor/YES.png",
    "success_kid/Exito/YES.png"
]

# Función para generar meme aleatorio sin repetirse
used_templates = set()  # Guarda los templates ya usados

def generar_meme(texto_arriba, texto_abajo):
    # Asegurarse de que no se repita el mismo template
    available_templates = [t for t in templates if t not in used_templates]
    
    if not available_templates:
        used_templates.clear()  # Reinicia la lista si todos los templates han sido usados
    
    meme_template = random.choice(available_templates)
    meme_url = f"https://api.memegen.link/images/{meme_template.replace('YES', texto_arriba).replace('NO', texto_abajo)}"
    
    # Marcar este template como usado
    used_templates.add(meme_template)
    
    return meme_url

@client.command()
async def mme(ctx, *, texto: str):
    """
    Genera un meme aleatorio con un texto proporcionado.
    El comando debe ser usado como #mme texto_arriba|texto_abajo
    """
    # Verificar si el texto tiene dos partes separadas por "|"
    if "|" not in texto:
        await ctx.send("Por favor, usa el formato correcto: #mme texto_arriba|texto_abajo")
        return

    texto_arriba, texto_abajo = texto.split("|", 1)

    # Generar meme con los textos proporcionados
    meme_url = generar_meme(texto_arriba, texto_abajo)

    # Enviar el meme generado
    await ctx.send(meme_url)
    
# ✅ Activar todos los permisos necesarios
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# 📂 Archivo donde se guardarán los usuarios
USERS_FILE = "users.json"

# 📌 Imágenes para los embeds
IMAGEN_REGISTRO = "https://i.ibb.co/rtXByCN/registro.jpg"
IMAGEN_PERFIL = "https://i.ibb.co/7tkRQdHQ/perfil.jpg"
IMAGEN_NIVEL_UP = "https://i.ibb.co/sd9DFgr/nivel-up.jpg"
IMAGEN_ADVERTENCIA = "https://i.ibb.co/LhC3xWx/advertencia.jpg"

# 📜 Cargar o crear el archivo de usuarios
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

def cargar_usuarios():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def guardar_usuarios(usuarios):
    with open(USERS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)

# 🔹 Comando de REGISTRO
@client.command()
async def reg(ctx, *, info):
    usuarios = cargar_usuarios()
    user_id = str(ctx.author.id)

    if user_id in usuarios:
        await ctx.send("⚠️ Ya estás registrado en el sistema.")
        return

    try:
        nombre, edad = info.split(".")
        usuarios[user_id] = {
            "nombre": nombre,
            "edad": edad,
            "nivel": 1,
            "xp": 0,
            "advertencias": 0
        }
        guardar_usuarios(usuarios)

        embed = discord.Embed(title="✅ Registro Completado", color=discord.Color.green())
        embed.set_thumbnail(url=IMAGEN_REGISTRO)
        embed.add_field(name="📛 Nombre", value=nombre, inline=True)
        embed.add_field(name="🎂 Edad", value=edad, inline=True)
        embed.set_footer(text="Bienvenido al sistema")
        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Formato incorrecto. Usa el comando así: `#reg nombre.edad`\nEjemplo: `#reg NATI.16`")

# 🔹 Comando para VER PERFIL
@client.command()
async def profile(ctx):
    usuarios = cargar_usuarios()
    user_id = str(ctx.author.id)

    if user_id not in usuarios:
        await ctx.send("⚠️ No estás registrado. Usa `#reg nombre.edad` para registrarte.")
        return

    datos = usuarios[user_id]
    embed = discord.Embed(title=f"Perfil de {ctx.author.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=IMAGEN_PERFIL)
    embed.add_field(name="📛 Nombre", value=datos["nombre"], inline=True)
    embed.add_field(name="🎂 Edad", value=datos["edad"], inline=True)
    embed.add_field(name="⭐ Nivel", value=datos["nivel"], inline=True)
    embed.add_field(name="🎮 Experiencia", value=datos["xp"], inline=True)
    embed.add_field(name="🚨 Advertencias", value=datos["advertencias"], inline=True)
    embed.set_footer(text="Tu información en el sistema")
    await ctx.send(embed=embed)

# 🔹 Comando para ADVERTIR USUARIOS
@client.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member, *, reason="No especificado"):
    usuarios = cargar_usuarios()
    user_id = str(member.id)

    if user_id not in usuarios:
        await ctx.send("⚠️ El usuario no está registrado en el sistema.")
        return

    usuarios[user_id]["advertencias"] += 1
    guardar_usuarios(usuarios)

    embed = discord.Embed(title="⚠️ Advertencia", color=discord.Color.red())
    embed.set_thumbnail(url=IMAGEN_ADVERTENCIA)
    embed.add_field(name="👤 Usuario", value=member.mention, inline=True)
    embed.add_field(name="📜 Razón", value=reason, inline=True)
    embed.add_field(name="🚨 Total Advertencias", value=usuarios[user_id]["advertencias"], inline=True)
    embed.set_footer(text="Sistema de advertencias")
    await ctx.send(embed=embed)

    if usuarios[user_id]["advertencias"] >= 3:
        await ctx.guild.ban(member, reason="Acumuló 3 advertencias")
        await ctx.send(f"🚨 {member.mention} ha sido **baneado** por acumular 3 advertencias.")

# 🔹 Comando de SUBIR DE NIVEL
@client.command()
async def adventure(ctx):
    usuarios = cargar_usuarios()
    user_id = str(ctx.author.id)

    if user_id not in usuarios:
        await ctx.send("⚠️ No estás registrado. Usa `#reg nombre.edad` para registrarte.")
        return

    xp_ganado = random.randint(5, 15)
    usuarios[user_id]["xp"] += xp_ganado

    # Si el XP es mayor a 50, sube de nivel
    if usuarios[user_id]["xp"] >= 50:
        usuarios[user_id]["xp"] = 0
        usuarios[user_id]["nivel"] += 1
        nivel_up = True
    else:
        nivel_up = False

    guardar_usuarios(usuarios)

    embed = discord.Embed(title="🎮 Aventura", color=discord.Color.purple())
    embed.set_thumbnail(url=IMAGEN_NIVEL_UP if nivel_up else IMAGEN_PERFIL)
    embed.add_field(name="👤 Usuario", value=ctx.author.mention, inline=True)
    embed.add_field(name="🆙 XP Ganado", value=xp_ganado, inline=True)
    embed.add_field(name="⭐ Nivel", value=usuarios[user_id]["nivel"], inline=True)
    embed.set_footer(text="Sigue jugando para subir de nivel")
    await ctx.send(embed=embed)

    if nivel_up:
        await ctx.send(f"🎉 ¡Felicidades {ctx.author.mention}! **Has subido al nivel {usuarios[user_id]['nivel']}** 🎉")

# 📂 Archivo donde están los subbots
SUBBOTS_FILE = "subbots.json"

# 📌 Función para cargar subbots
def cargar_subbots():
    with open(SUBBOTS_FILE, "r") as f:
        return json.load(f)

# 📌 Lista de subbots en ejecución
subbots_activos = []

async def iniciar_subbot(token, nombre):

    @client.event
    async def on_ready():
        print(f"✅ Subbot {nombre} conectado como {client.user}")

    @client.command()
    async def hola(ctx):
        await ctx.send(f"👋 ¡Hola! Soy un subbot de {nombre}")

    # Puedes agregar más comandos aquí...

    await client.start(token)

async def iniciar_todos_subbots():
    subbots = cargar_subbots()
    tareas = []

    for user_id, data in subbots.items():
        token = data["token"]
        nombre = data["nombre"]
        tarea = asyncio.create_task(iniciar_subbot(token, nombre))
        subbots_activos.append(tarea)

    await asyncio.gather(*subbots_activos)

# Cambia esto con tu token del bot
OWNER_ID = 1252023555487567932  # Reemplázalo con tu ID de Discord
GITHUB_REPO = "https://github.com/nati-1616/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"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="#", intents=intents)

# Comando para subir los cambios a GitHub
@client.command()
async def subirgit(ctx):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ No tienes permisos para usar este comando.")

    try:
        repo = git.Repo(os.getcwd())  # Obtiene el repositorio
        repo.git.add(".")  # Agrega todos los cambios
        repo.index.commit("Actualización desde Replit")  # Confirma los cambios
        repo.remote().push()  # Sube los cambios
        await ctx.send("✅ Bot actualizado en GitHub.")
    except Exception as e:
        await ctx.send(f"❌ Error al subir: `{e}`")

# Comando para actualizar el bot desde GitHub
@client.command()
async def actualizar(ctx):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ No tienes permisos para usar este comando.")

    try:
        repo = git.Repo(os.getcwd())
        origin = repo.remote()
        origin.pull()  # Descarga la última versión del repositorio
        await ctx.send("✅ Bot actualizado. Reiniciando...")
        os.system("kill 1")  # Reinicia el bot en Replit
    except Exception as e:
        await ctx.send(f"❌ Error al actualizar: `{e}`")

# Ejecutar el bot
client.run(BOT_TOKEN)