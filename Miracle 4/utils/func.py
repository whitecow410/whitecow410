# The Bot Made By AwkwardTeam. (WhiteCow, Sear_, YT Mango)
# Made For Miracle.
# Comment By  Sear_
# The Comment is for helping the code investigator/developer understand Codes.
# Credits to Miracle Development Team.


# Import Packages #
import discord
from discord.ext import commands

import yaml
import json
import datetime
import os
import asyncio
import aiofiles

from functools import lru_cache

with open("config.yaml", "r") as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)

with open("./core/emoji.json", "r", encoding="utf8") as emojiData:
    emoji = json.load(emojiData)

__all__ = (
    "utils",
    "SerSys",
)


class utils:
    def load(path, items=None, mode="r", encoding="utf8") -> list:
        if not items:
            with open(path, mode, encoding=encoding) as jdata:
                return json.load(jdata)
        else:
            with open(path, mode, encoding=encoding) as jdata:
                data = json.load(jdata)
                return data[str(items)]

    def save(path, data, mode="w", encoding="utf8") -> None:
        with open(path, mode, encoding=encoding) as jdata:
            json.dump(data, jdata, indent=4, ensure_ascii=False)

    def get_key(dicts, val):
        for key, value in dicts.items():
            if val == value:
                return key
        return None

    def get_file_size(file_path):
        size_in_bytes = os.path.getsize(file_path)
        size_in_kb = size_in_bytes / 1024
        size_in_mb = size_in_kb / 1024
        size_in_gb = size_in_mb / 1024

        if size_in_gb >= 1:
            return f"{size_in_gb:.2f} GB"
        elif size_in_mb >= 1:
            return f"{size_in_mb:.2f} MB"
        elif size_in_kb >= 1:
            return f"{size_in_kb:.2f} KB"
        else:
            return f"{size_in_bytes} bytes"

    def get_now(format_="%H:%M:%S UTC+8") -> str:
        now = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=+8))
        ).strftime(format_)
        return now

    def safe_num(num) -> float:
        if isinstance(num, str):
            num = float(num)
        return float('{:.3g}'.format(abs(num)))

    def format(num) -> str:
        magnitude = 0
        num = utils.safe_num(num)
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    def whitelist(ctx) -> bool:
        return ctx.author.id in (config["DEVELOPER"] + config["WHITELIST"])

    class Language:
        def __init__(self, bot=None, guild=None):
            if bot and guild:
                self.lang = asyncio.run(self.get_language(bot, guild))

        def get_lang(self, ID, lang=None):
            if lang is None:
                lang = self.lang
            self.get_translation(ID, lang)

        @lru_cache(maxsize=None)
        def get_translation(self, ID, lang):
            return asyncio.run(self.translate(ID, lang))

        async def _translate(self, ID, lang) -> str:
            async with aiofiles.open(f"{lang}.lang", 'r') as langFile:
                async for line in langFile:
                    line = line.strip()
                    if line:
                        key, value = line.split('=')
                        if key == ID:
                            return value.strip()
                return ID

        async def get_language(self, bot, guild) -> str:
            async with bot.db.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT language FROM setting WHERE guild = ?", (guild.id,))
                    lang = await cursor.fetchval()
            return lang or "zh_tw"

    def progress_bar(iteration, total, bar_length=10) -> str:
        progress = (iteration / total) * 100

        progress_bar = '█' * int(progress / 100 * bar_length)
        empty_bar = '-' * (bar_length - len(progress_bar))
        return "|{}{}| {}%".format(progress_bar, empty_bar, round(progress))

    def code(message, m=None) -> str:
        return f"```{m}\n{message}\n```"


class SerSys:

    def get(message) -> str:
        keywords = {
            "memberMention": "{member.mention}",
            "member": "{member}",
            "memberName": "{member.name}",
            "memberID": "{member.id}",
            "guildName": "{guild.name}",
            "guildID": "{guild.id}",
            "greenArrow": "{emoji['GREEN_ARROW']}",
            "redArrow": "{emoji['RED_ARROW']}",
        }
        return message.format(**keywords)

    async def setup(bot, guild) -> None:
        async with bot.db.cursor() as cursor:
            await cursor.execute("DELETE FROM setting WHERE guild = ?", (guild.id,))
            await cursor.execute("INSERT INTO setting(guild) VALUES (?)", (guild.id,))
            await cursor.execute("INSERT INTO version(guild) VALUES (?)", (guild.id,))
            await bot.db.commit()
