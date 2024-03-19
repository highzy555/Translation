import discord
import json
import TranslatorApi
import supported_languages
import os
import discord
from discord.ext import commands
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

bot_token = os.environ.get("bot")

intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True 
intents.messages = True 

client = commands.Bot(command_prefix="!", intents=intents)

requesting_user = "highzixdev_69" #การร้องขอ_ผู้ใช้

# United States Flag = english
# Indian Flag = Hindi
# Spanish Flag = Spanish
# German Flag = German
# French Flag = French

help_message = "To translate a message simply react to it with a flag emoji." \
               "List of supported languages and their flags: \n"\
               ":flag_us: English | US\n"\
               ":flag_in: Hindi | IN\n"\
               ":flag_es: Spanish | ES\n"\
               ":flag_de: German | DE\n"\
               ":flag_mf: French | MF\n"\
               ":flag_pt: Portuguese | PT\n"\
               ":flag_ru: Russia | RU\n"\
               ":flag_jp: Japanese | JP\n"\
               ":flag_jp: Thailand | TH\n"\
               "More languages will be supported in future releases."

def get_country(flag):
    with open("required_data.json", "r") as datafile:
        jsondata = json.loads(datafile.read())

    for every in jsondata:
        if every["flag"] == flag:
            return every


@client.event
async def on_reaction_add(reaction, user):
    print("You added a reaction"+reaction.emoji)

    received_emoji = reaction.emoji
    country_name = get_country(received_emoji)
    print(country_name)
    if country_name is not None:
        languages = supported_languages.SupportedLanguages
        if country_name["name"]["common"] == "France":
            language = languages.French
        elif country_name["name"]["common"] == "Germany":
            language = languages.German
        elif country_name["name"]["common"] == "India":
            language = languages.Hindi
        elif country_name["name"]["common"] == "United States":
            language = languages.English
        elif country_name["name"]["common"] == "Spain":
            language = languages.Spanish
        elif country_name["name"]["common"] == "Russia":
            language = languages.Russian
        elif country_name["name"]["common"] == "Portugal":
            language = languages.Portuguese
        elif country_name["name"]["common"] == "Japan":
            language = languages.Japanese
        elif country_name["name"]["common"] == "Thai":
            language = languages.Thailand
        else:
            language = None

        if language is not None:
            api = TranslatorApi.TranslatorApi()
            text = [{"text": reaction.message.content}]
            translation = api.translate(text, language)
            response = translation.text
            response = json.loads(response)
            if response[0]["detectedLanguage"] is not None:
                if response[0]["translations"] is not None:
                    translated_text = response[0]["translations"][0]["text"]
                    if user.dm_channel is None:
                        await user.create_dm()
                    await user.dm_channel.send("Message `" + reaction.message.content + "` from user " + reaction.message.author.name +  " \ntranslated message : `" + translated_text + "`")
                else:
                    print(response)
                    await reaction.message.channel.send("Translation Failed")
            else:
                print(response)
                await reaction.message.channel.send("We were not able to detect input language")

        else:
            await reaction.message.channel.send("Languages of {} are currently not supported".format(country_name["name"]["common"]))
    else:
        print("Normal emoji found exiting")
    return

@client.event
async def on_message(message):
    content = message.content
    list_content = str(content).split()
    if len(list_content) == 2 and list_content[1] == "help":
        mentions = message.raw_mentions
        if mentions is not None:
            for mention in mentions:
                if mention == client.user.id:
                    if message.author.dm_channel is None:
                        await message.author.create_dm()
                    await message.author.dm_channel.send(help_message)

    return
    
@client.event
async def on_ready():
  print(f"Bot {client.user.name} is ready!")
  await client.change_presence(activity=discord.Streaming(
      name='Translation', url='https://www.twitch.tv/example_channel'))    


client.run(bot_token)
