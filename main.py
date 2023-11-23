import discord
from discord.ext import commands
from googletrans import Translator

# Dein Bot-Token
TOKEN = ''
# Erstelle einen Bot-Client mit Intents
intents = discord.Intents.default()
intents.message_content = True  # Aktiviere das message_content-Event

bot = commands.Bot(command_prefix='!', intents=intents)
translator = Translator()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_raw_reaction_add(payload):
    # Überprüfe, ob die Reaktion von einem Bot stammt
    if payload.member.bot:
        return

    # Überprüfe, ob die Nachricht in Deutsch oder Englisch ist
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    # Überprüfe die Reaktion und rufe die entsprechende Übersetzungsfunktion auf
    if payload.emoji.name == '🇩🇪':
        translated_message = translate_to_german(message.content)
    elif payload.emoji.name == '🇬🇧':
        translated_message = translate_to_english(message.content)
    else:
        return  # Ignoriere Reaktionen mit anderen Emojis

    # Antworte auf die ursprüngliche Nachricht und füge das React-Emoji hinzu
    original_author = message.author
    emoji = payload.emoji
    await message.reply(f"{emoji}: {translated_message}", mention_author=False)


def translate_to_german(message):
    # Hier wird die googletrans-Bibliothek verwendet, um den Text zu übersetzen
    translation = translator.translate(message, dest='de')
    translated_message = translation.text
    return translated_message


def translate_to_english(message):
    # Hier wird die googletrans-Bibliothek verwendet, um den Text zu übersetzen
    translation = translator.translate(message, dest='en')
    translated_message = translation.text
    return translated_message


# Starte den Bot
bot.run(TOKEN)
