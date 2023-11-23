import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from googletrans import Translator

load_dotenv('.env')
TOKEN = os.getenv("BOTTOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
translator = Translator()

reacted_messages = set()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_raw_reaction_add(payload):
    if payload.member is None or payload.member.bot:
        print(f"Skipped reaction for None or bot member. Payload: {payload}")
        return

    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    lang = detect_language(message.content)

    if lang == 'en' and payload.emoji.name == '🇬🇧':
        await message.remove_reaction('🇬🇧', payload.member)

    if lang == 'de' and payload.emoji.name == '🇩🇪':
        await message.remove_reaction('🇩🇪', payload.member)

    if payload.message_id in reacted_messages:
        return

    if payload.emoji.name == '🇩🇪' and lang != 'de':

        reacted_messages.add(payload.message_id)
        translated_message = translate_to_german(message.content)
        user = await bot.fetch_user(payload.user_id)
        await reply_translated_message(message, user, '🇩🇪', translated_message)

    elif payload.emoji.name == '🇬🇧' and lang != 'en':

        reacted_messages.add(payload.message_id)
        translated_message = translate_to_english(message.content)
        user = await bot.fetch_user(payload.user_id)
        await reply_translated_message(message, user, '🇬🇧', translated_message)


async def reply_translated_message(original_message, user, emoji, translated_message):
    await original_message.reply(content=f"{emoji}: {translated_message}", mention_author=False)


def translate_to_german(message):
    translation = translator.translate(message, dest='de')
    translated_message = translation.text
    return translated_message


def translate_to_english(message):
    translation = translator.translate(message, dest='en')
    translated_message = translation.text
    return translated_message


def detect_language(text):
    detected_lang = translator.detect(text)
    return detected_lang.lang if detected_lang else None


bot.run(TOKEN)
