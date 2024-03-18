import discord
from discord.ext import commands
from googletrans import Translator
from langdetect import detect_langs
import os
#import logging

PREFIX = '!'
translator = Translator()
token = os.environ.get('bot')
intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True 
intents.messages = True 

client = commands.Bot(command_prefix="!", intents=intents)
#logging.basicConfig(filename='translation.log', level=logging.INFO)

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not message.content.startswith(f"{PREFIX}tls"):
        return

    args = message.content.split(' ')
    if len(args) < 4:
        await message.channel.send(f'Usage: {PREFIX}tls <source language> <target language> <text>')
        return

    source_lang = args[1]
    target_lang = args[2]
    text = ' '.join(args[3:])

    if source_lang == target_lang:
        await message.channel.send('Source and target languages cannot be the same.')
        return

    try:
        # ตรวจสอบโทเค็นบอท
        if not isinstance(client.user.id, int):
            await message.channel.send('Invalid bot token.')
            return

        # ตรวจสอบภาษาต้นทาง
        langs = detect_langs(text)
        if source_lang not in [lang.lang for lang in langs]:
            source_lang = max(langs, key=lambda lang: lang.prob).lang
            await message.channel.send(f'Detected source language: {source_lang}')

        # แปลข้อความ
        translation = translator.translate(text, src=source_lang, dest=target_lang)
        await message.channel.send(translation.text)

        # บันทึกไปที่ไฟล์บันทึก
        #logging.info(f'{message.author.name}: {text} -> {translation.text}')

    except ValueError as e:
        await message.channel.send(f'Invalid language code: {e}')
    except discord.HTTPException as e:
        await message.channel.send(f'Discord API error: {e}')
    except Exception as e:
        await message.channel.send(f'Error: {e}')
        
@client.event
async def on_ready():
  print(f"Bot {client.user.name} is ready!")
  await client.change_presence(activity=discord.Streaming(
      name='Black Market!', url='https://www.twitch.tv/example_channel'))        

client.run(token)
