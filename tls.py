import discord
from discord.ext import commands
import googletrans
import os
from flask import Flask, render_template
from threading import Thread
app = Flask('')
@app.route('/')
def home():
  return "bot python is online!"
def index():
  return render_template("index.html")
def run():
  app.run(host='0.0.0.0', port=8080)
def highzy():
  t = Thread(target=run)
  t.start()
  
highzy()  
token = os.environ.get('bot')
intents=discord.Intents.all()
case_insensitive=True


class TranslationBot():
    async def on_message(self, message):
        #ตอบกลับข้อความด้วยคำแปล
        if message.author == self.user:
            return
        if message.content.startswith(f'!แปล'):
            content = message.content.split(' ')
            if len(content) < 3:
                await message.channel.send("คำสั่งใช้: !แปล <ภาษาต้นทาง> <ภาษาปลายทาง> <ข้อความ>")
                return
            source_lang = content[1]
            target_lang = content[2]
            text = ' '.join(content[3:])

            # แปลข้อความ
            translator = googletrans.Translator()
            result = translator.translate(text, dest=target_lang, src=source_lang)

            # ส่งข้อความที่แปลแล้ว
            await message.channel.send(f"** # คำแปล: __{result.text}__ **")
            
            


client = TranslationBot()
client.run(token)
