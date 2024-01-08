# The Bot Made By AwkwardTeam. (WhiteCow, Sear_, YT Mango)
# Made For Miracle.
# Comment By  Sear_
# The Comment is for helping the code investigator/developer understand Codes.
# Credits to Miracle Development Team.


# Import Packages #
import discord
from discord.ext import commands

from utils.func import utils

emoji = utils.load("./core/emoji.json")

__all__ = (
    "selects",
)


class selects:
    class commands:
        class info_select(discord.ui.View):
            def __init__(self, bot):
                super().__init__(timeout=None)
                self.bot = bot
