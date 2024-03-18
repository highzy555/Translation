import discord
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
import asyncio
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

# Set up the Discord bot
bot = commands.Bot(
    command_prefix='!',
    help_command=None,
    intents=discord.Intents.all(),
    strip_after_prefix=True,
    case_insensitive=True, 
)

# Set up the webhook URL
webhook_url = os.environ.get('hook')
token = os.environ.get('bot')

# Create a cooldown dictionary to prevent spam
cooldowns = {3}

# Define the !translate command
@bot.command()
async def tls(ctx, text, language):
    """Translates text to a specified language."""

    # Check if the user is on cooldown
    if ctx.author.id in cooldowns:
        if cooldowns[ctx.author.id] > time.time():
            await ctx.send("You are on cooldown. Please wait {3} seconds.".format(round(cooldowns[ctx.author.id] - time.time())))
            return

    # Reset the cooldown for the user
    cooldowns[ctx.author.id] = time.time() + 60

    # Translate the text using Google Translate
    from googletrans import Translator
    translator = Translator()
    translation = translator.translate(text, dest=language)

    # Create an embed to display the translation
    embed = discord.Embed(title="Translation", description=translation.text, color=0x00ff00)
    embed.add_field(name="Original Language", value=text.split(" ")[0], inline=True)
    embed.add_field(name="Translated Language", value=language, inline=True)
    embed.set_footer(text="Powered by Blackmarket Translate")

    # Send the embed to the channel
    await ctx.send(embed=embed)

    # Send a notification to the webhook
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title="Translation Request", description="A user has requested a translation.", color=0x00ff00)
    embed.add_field(name="User", value=ctx.author.name, inline=True)
    embed.add_field(name="Text", value=text, inline=True)
    embed.add_field(name="Language", value=language, inline=True)
    webhook.add_embed(embed)
    webhook.execute()
    
@bot.event
async def on_ready():
  print(f"Bot {bot.user.name} is ready!")
  await bot.change_presence(activity=discord.Streaming(
      name='Black Market!', url='https://www.twitch.tv/example_channel'))    

# Run the bot
bot.run(token)
