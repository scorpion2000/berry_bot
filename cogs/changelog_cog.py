import discord

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
        embed = discord.Embed(
            title = "Berry Changelog!",
            description = "- Test",
            color = discord.Color.teal()
        )

        embed.set_image(
            url="https://cdn.discordapp.com/attachments/437358356013907968/1508761916477280327/pony-town-Berry_Flames-boop-sit-padded-2x1.png?ex=6a16b788&is=6a156608&hm=d694f9c805abf4b766dccac7d5af090bd029326f0ca0ecdb8d27c1ab586201db"
        )

        await self.bot_channel.send(embed=embed)
        await interaction.response.send_message(
            "Changelog sent!",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(ChangelogCog(bot))