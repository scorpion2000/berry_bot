import discord

from discord.ext import commands
from discord import app_commands
from config import bot_channel

class ChangelogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.changelog = bot.changelog_service
        self.bot_channel = bot_channel

    @app_commands.command(
        name="changelog",
        description="Display the latest changelog! (Admin only)"
    )
    async def changelog(self, interaction: discord.Interaction):
        if any(role.name in ["Admin"]for role in interaction.user.roles):
            await interaction.response.send_message(
                "Must be an admin to do this!",
                ephemeral=True
            )
        bot_channel = self.bot.get_channel(self.bot_channel)
        file = discord.File("berry.png")

        changelog = ""
        with open("changelog.txt", "r", encoding="utf-8") as file:
            changelog = file.read()

        #if interaction.user.role not in ["Admin", "Trial Mod"]:
        #    continue

        embed = discord.Embed(
            title = "Berry Changelog!",
            description = changelog,
            color = discord.Color.teal()
        )

        #await bot_channel.send(file = file, embed = embed)
        await bot_channel.send(embed = embed)

        await interaction.response.send_message(
            "Changelog sent!",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(ChangelogCog(bot))