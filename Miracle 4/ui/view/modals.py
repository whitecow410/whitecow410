# The Bot Made By AwkwardTeam. (WhiteCow, Sear_, YT Mango)
# Made For Miracle.
# Comment By  Sear_
# The Comment is for helping the code investigator/developer understand Codes.
# Credits to Miracle Development Team.


# Import Packages #
import discord
from discord.ext import commands

from utils import utils

emoji = utils.load("./core/emoji.json")

__all__ = (
    "modals",
)


class modals:
    class feedback_modal(discord.ui.Modal, title="意見回饋"):
        def __init__(self, bot):
            super().__init__()
            self.bot = bot

        description = discord.ui.TextInput(
            label=f"填寫您想回饋的意見或感受",
            placeholder="把您想回饋意見出來吧:D",
            min_length=1,
            max_length=4000,
            required=True,
            style=discord.TextStyle.paragraph,
        )

        async def on_submit(self, interaction: discord.Interaction):
            embed = discord.Embed(
                description=f"{emoji['SUCCESS']}**感謝您的意見回饋，我們會很快作出改進**", color=0xDB7BFF
            )
            embed.set_footer(
                text=f"{self.bot.user.name} • {self.bot.description}",
                icon_url=self.bot.user.display_avatar,
            )
            channel = self.bot.get_channel(937333239700414474)
            webhooks = await channel.webhooks()
            webhook = discord.utils.get(webhooks, name=str(self.bot.user))
            if webhook is None:
                webhook = await channel.create_webhook(name=self.bot.user)
            await webhook.send(
                self.description,
                username=f"{interaction.user.name}#{interaction.user.discriminator}",
                avatar_url=interaction.user.avatar.url,
            )
            await webhook.delete()
            return await interaction.response.send_message(embed=embed, ephemeral=True)
