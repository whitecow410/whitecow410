# The Bot Made By AwkwardTeam. (WhiteCow, Sear_, YT Mango)
# Made For Miracle.
# Comment By  Sear_
# The Comment is for helping the code investigator/developer understand Codes.
# Credits to Miracle Development Team.


# Import Packages #
from discord.ext import commands
from core import Bot

import core.logger as logger
from utils import utils

import os

# Logger Setup #
logger = logger.logging.getLogger('bot')

__all__ = (
    "Cog_Extension",
    "Commands_GroupCog",
)


class Cog_Extension(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def cog_load(self) -> None:
        logger.info(f"Loaded {self.qualified_name.lower()}")

    async def cog_unload(self) -> None:
        logger.info(f"Loaded {self.qualified_name.lower()}")


class Commands_GroupCog(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot
