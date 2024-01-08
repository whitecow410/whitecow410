# The Bot Made By AwkwardTeam. (WhiteCow, Sear_, YT Mango)
# Made For Miracle.
# Comment By  Sear_
# The Comment is for helping the code investigator/developer understand Codes.
# Credits to Miracle Development Team.


# Import Packages #
import discord
from discord.ext import commands
from discord.ui import View, Button

from utils import utils
from ui.view import modals

emoji = utils.load("./core/emoji.json")

__all__ = (
    "buttons",
)


class buttons:
    class warning(discord.ui.View):
        def __init__(self, ctx, timeout=180):
            super().__init__(timeout=timeout)
            self.ctx = ctx
            self.value = None

        @discord.ui.button(label="取消", custom_id="false")
        async def cancel(
            self, interaction: discord.Interaction, button: discord.ui.Button
        ):
            self.clear_items()
            await interaction.response.edit_message(view=self)
            self.value = "false"
            self.stop()

        @discord.ui.button(label="確定", style=discord.ButtonStyle.red, custom_id="true")
        async def sure(
            self, interaction: discord.Interaction, button: discord.ui.Button
        ):
            self.clear_items()
            await interaction.response.edit_message(view=self)
            self.value = "true"
            self.stop()

        async def interaction_check(self, interaction):
            if interaction.user != self.ctx.author:
                await interaction.response.defer()
                return False
            else:
                return True

        async def on_timeout(self):
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)

    class commands:
        class update_ping(discord.ui.View):
            def __init__(self, bot, func, timeout=180):
                super().__init__(timeout=timeout)
                self.bot = bot
                self.func = func

            @discord.ui.button(
                label="刷新", style=discord.ButtonStyle.green, custom_id="update"
            )
            async def callback(
                self, interaction: discord.Interaction, button: discord.ui.Button
            ):
                await interaction.response.edit_message(embed=self.func(self.bot))

            async def on_timeout(self):
                for button in self.children:
                    button.disabled = True
                await self.message.edit(view=self)

        class info_bot(discord.ui.View):
            def __init__(self, bot):
                super().__init__(timeout=None)
                self.bot = bot
                self.add_item(
                    Button(
                        label="伺服器支援",
                        style=discord.ButtonStyle.link,
                        url="https://discord.gg/N57vF6d76U",
                    )
                )
                self.add_item(
                    Button(
                        label="邀請機器人",
                        style=discord.ButtonStyle.link,
                        url="https://discord.com/api/oauth2/authorize?client_id=826244062612553780&permissions=8&scope=bot%20applications.commands",
                    )
                )

            @discord.ui.button(
                label="更多資訊", style=discord.ButtonStyle.green, custom_id="more_info"
            )
            async def callback(
                self, interaction: discord.Interaction, button: discord.ui.Button
            ):
                embed = discord.Embed(
                    description=f"**{self.bot.user.name} - {self.bot.description}**\n更詳細的資訊都在這裡 !", color=0xFFFFFF)
                embed.set_author(
                    name=self.bot.user,
                    url="https://discord.com/api/oauth2/authorize?client_id=826244062612553780&permissions=8&scope=bot%20applications.commands",
                    icon_url=self.bot.user.display_avatar,
                )
                embed.set_thumbnail(url=self.bot.user.display_avatar)
                embed.add_field(
                    name=f"{emoji['TIMER']} 使用量比率 (CPU / RAM)", value=f"`{psutil.cpu_percent()}%` / `{psutil.virtual_memory().percent}%`", inline=True
                )
                embed.add_field(
                    name=f"{emoji['HELP_INFO']} 提示", value="點擊下方下拉選單可以查看其它資訊", inline=False
                )
                embed.set_footer(text=f"Developed by AwkwardTeam")
                select = selects.info_select(self.bot)
                select.message = await interaction.response.send_message(
                    embed=embed, view=select, ephemeral=True
                )
