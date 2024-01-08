# The Bot Made By AwkwardTeam. (WhiteCow, Sear_, YT Mango)
# Made For Miracle.
# Comment By  Sear_
# The Comment is for helping the code investigator/developer understand Codes.
# Credits to Miracle Development Team.

# Import Packages #
import discord
from discord.ext import commands

from utils import utils
import core.logger as logger

import yaml
from dotenv import load_dotenv
import platform
import aiosqlite
import time
import os

# Loading Env #
load_dotenv()

# Loading config #
with open('config.yaml', 'r') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)

# Logger Setup #
logger = logger.logging.getLogger('bot')

# Loading Emoji #
emoji = utils.load('./core/emoji.json')

preefix = (
    config['PREFIX'] if config['STATE'].lower() not in [
        'developing', 'development'] else config['PREFIX_DEV']
)

__all__ = (
    "Bot",
)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(*preefix),
            intents=discord.Intents.all()
        )
        # Loading Settings into system #
        token = {
            'developing': 'TOKEN_DEV', 'development': 'TOKEN_DEV',
            'beta': 'TOKEN_BETA',
            'release': 'TOKEN'
        }
        self.token: str = os.getenv(token[config['STATE'].lower()])

        self.prefix: str = config['PREFIX']
        self.developer: list = config['DEVELOPER']
        self.whilelist: list = config['WHITELIST']
        self.beta_tester: list = config['BETATESTER']
        self.emoji: dict = emoji

        self.last_update: int = config['LAST_UPDATE']
        self.description: str = config['DESCRIPTION']
        self.team: str = config['TEAM']
        self.versin: str = config['VERSIN']

        self.remove_command('help')

    async def setup_hook(self) -> None:  # Cogs #
        logger.info("Loading-Cogs".center(40, '-'))
        for folder in os.listdir('cogs'):
            if not folder.startswith('_'):
                for file in os.listdir(f'cogs/{folder}'):
                    if not file.startswith('_') and file.endswith('.py'):
                        await self.load_extension(f"cogs.{folder}.{file[:-3]}")

        logger.info("Connect-Database".center(40, '-'))
        # Access The Database #
        self.db = await aiosqlite.connect("data/data.db")
        async with self.db.cursor() as cursor:
            tables = [
                "setting(guild INTEGER, language TEXT, plan TEXT, beta BLOB, PRIMARY KEY(guild))",
                "serSys(guild INTEGER, joinMessage TEXT, removeMessage TEXT, joinDm TEXT, autoRole TEXT, verify TEXT, tempVoice TEXT, ticket TEXT, gchat TEXT, leveling TEXT, PRIMARY KEY(guild))",
                "currency(user INTEGER, wallet REAL, bank REAL, area TEXT, job TEXT, PRIMARY KEY(user))",
                "gchatID(id TEXT, owner INTEGER, connected TEXT, baned TEXT, PRIMARY KEY(id))",
                "leveling(guild INTEGER, user INTEGER, level INTEGER, xp REAL, boost REAL, PRIMARY KEY(guild, user))",
                "XPBoost(guild INTEGER, role INTEGER, boost REAL, PRIMARY KEY(guild))",
                "awkward(user INTEGER, color TEXT, achievement TEXT, daily TEXT, violation TEXT, PRIMARY KEY(user))"
            ]
            for table in tables:
                await cursor.execute(
                    "CREATE TABLE IF NOT EXISTS {}".format(table)
                )
        await self.db.commit()  # Save Data to Database #
        logger.info(
            f"Connected data.db ({utils.get_file_size('data/data.db')})")
        self.strat_timestamp = int(time.time())

    async def on_connect(self) -> None:
        logger.info("Syncing-Commands".center(40, '-'))
        self.synced = await self.tree.sync()
        logger.info("Synced {} commands".format(len(self.synced)))

    async def on_ready(self) -> None:
        logger.info("Bot-Is-Ready".center(40, '-'))
        await self.change_presence(
            status=discord.Status.online,  # Change The Status to "Online" #
            activity=discord.Game(
                f"{preefix[0]}help - 查看命令"),  # m/help Hints #
        )
        # Information Printing on console when Starting up #
        logger.info("User: {} (ID: {})".format(
            self.user, self.user.id))
        logger.info("version (Python, Discord.py, Bot) : {}, {}, {}".format(
            platform.python_version(), discord.__version__, config['VERSIN']))
        logger.info("".center(40, '-'))
