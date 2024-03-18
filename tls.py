import discord
from googletrans import Translator
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

client = discord.Client()
token = os.environ.get('bot')
translator = Translator()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!tls'):
        args = message.content.split(' ')
        if len(args) < 3:
            await message.channel.send('Usage: !translate <language> <text>')
            return

        language = args[1]
        text = ' '.join(args[2:])
        try:
            translation = translator.translate(text, dest=language)
            await message.channel.send(translation.text)
        except Exception as e:
            await message.channel.send(f'Error: {e}')
            
@client.event
async def on_ready():
  print(f"Bot {client.user.name} is ready!")
  await client.change_presence(activity=discord.Streaming(
      name="Black Market !", url='https://www.twitch.tv/example_channel'))            

client.run(token)
