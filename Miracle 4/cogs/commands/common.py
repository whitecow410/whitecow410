# The Bot Made By AwkwardTeam. (WhiteCow, Sear_, YT Mango)
# Made For Miracle.
# Comment By  Sear_
# The Comment is for helping the code investigator/developer understand Codes.
# Credits to Miracle Development Team.


## Import Packages ##
import discord
from discord import app_commands
from discord import app_commands
from discord.ext import commands

from ..import Cog_Extension
from utils import utils

from ui.view import buttons
from ui.view import modals


class Common(Cog_Extension):
    @commands.hybrid_command(description='command.ping.description', aliases=['pong'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def ping(self, ctx: commands.Context):
        await ctx.typing()

        def get_embed(bot):
            color = 0xFCFCFC if int(round(bot.latency * 1000)) <= 50 else 0x43B582 if int(round(
                bot.latency * 1000)) <= 100 else 0xF04A47
            embed = discord.Embed(
                title=f"{round(bot.latency*1000)} ms", color=color)
            embed.set_footer(
                text=f"{bot.user.name} • {bot.description}",
                icon_url=bot.user.display_avatar,
            )
            return embed
        button = buttons.commands.update_ping(
            self.bot, embed=get_embed(self.bot))
        button.message = await ctx.send(embed=get_embed(self.bot), view=button)

    @commands.command(description='command.info.description')
    async def info(self, ctx: commands.Context):
        language = utils.Language(self.bot, ctx.guild)

        embed = discord.Embed(
            description=f"**{self.bot.user.name} - {self.bot.description}**", color=discord.Color.random())
        embed.set_author(
            name=self.bot.user,
            url="https://discord.com/api/oauth2/authorize?client_id=826244062612553780&permissions=8&scope=bot%20applications.commands",
            icon_url=self.bot.user.display_avatar,
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar)
        embed.add_field(
            name=f"{self.emoji['command.update']} "+language.get_lang(
                'command.info.field_01.name').format(self.bot.versin),
            value=language.get_lang('command.info.field_01.value').format(
                self.bot.last_update, self.bot.strat_timestamp),
            inline=True,
        )
        embed.add_field(
            name=f"{self.emoji['common.server']} "+language.get_lang('command.info.field_02.name').format(
                len(self.bot.guilds)),
            value=language.get_lang('command.info.field_01.value').format(
                len(self.bot.users)),
            inline=True,
        )
        embed.set_footer(text=language.get_lang(
            'command.info.discord_version').format(discord.__version__))
        embed.timestamp = ctx.message.created_at
        button = buttons.commands.info_bot(self.bot)
        button.message = await ctx.send(embed=embed, view=button)

    @app_commands.command(description='app_command.feedback.description')
    async def feedback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(modals.feedback_modal(self.bot))

    @commands.command(description='command.feedback.description')
    async def feedback(self, ctx: commands.Context):
        language = utils.Language(self.bot, ctx.guild)

        embed = discord.Embed(
            description=f"{self.emoji['common.edit']} "+language.get_lang('command.feedback.respond'), color=0xDB7BFF
        )
        embed.set_footer(
            text=f"{self.bot.user.name} • {self.bot.description}",
            icon_url=self.bot.user.display_avatar,
        )
        button = buttons.feedback_button(self.bot)
        button.message = await ctx.send(embed=embed, view=button)

    @commands.hybrid_command(description='command.say.description', help="<message>", usage="Hello World!")
    async def say(self, ctx: commands.Context, *, message: str):
        mentions = discord.AllowedMentions(
            everyone=False, users=True, roles=False, replied_user=True
        )
        if "@everyone" in message or "@here" in message:
            if ctx.author.guild_permissions.mention_everyone:
                mentions = discord.AllowedMentions(
                    everyone=True, users=True, roles=True, replied_user=True
                )
        try:
            await ctx.message.delete()
        except:
            pass
        if ctx.message.reference:
            channel = self.bot.get_channel(ctx.message.reference.channel_id)
            msg = await channel.fetch_message(ctx.message.reference.message_id)
            await msg.reply(message, allowed_mentions=mentions)
        else:
            await ctx.send(message, allowed_mentions=mentions)

    @commands.command(description='command.embed.description', help="<message>", usage="Hello World!")
    async def embed(self, ctx: commands.Context, *, message: str):
        mentions = discord.AllowedMentions(
            everyone=False, users=True, roles=False, replied_user=True
        )
        if "@everyone" in message or "@here" in message:
            if not ctx.author.guild_permissions.mention_everyone:
                mentions = discord.AllowedMentions(
                    everyone=True, users=True, roles=True, replied_user=True
                )
        embed = discord.Embed(description=message, color=ctx.author.color)
        embed.set_author(
            name=ctx.author.display_name, icon_url=(ctx.author.display_avatar)
        )
        embed.timestamp = ctx.message.created_at
        try:
            await ctx.message.delete()
        except:
            pass
        if ctx.message.reference:
            channel = self.bot.get_channel(ctx.message.reference.channel_id)
            msg = await channel.fetch_message(ctx.message.reference.message_id)
            await msg.reply(embed=embed, allowed_mentions=mentions)
        else:
            await ctx.send(embed=embed, allowed_mentions=mentions)


async def setup(bot: commands.Bot):
    await bot.add_cog(Common(bot))
