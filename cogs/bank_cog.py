import discord

from discord.ext import commands
from discord import app_commands

class Bankingog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.economy = bot.economy_service

    @app_commands.command(
        name="send_bits",
        description="Send your bits to someone else!"
    )
    async def send_bits(
        self,
        interaction: discord.Interaction,
        to_user: discord.User,
        amount: int
    ):
        # Oh jesus python looks scuffed
        sender = interaction.user

        success, error = self.economy.transfer_bits(sender.name,to_user.name,amount)

        if not success:
            await interaction.response.send_message(error,ephemeral=True)
            return

        await interaction.response.send_message(
            f"{sender.mention} sent "
            f"{amount} bits to "
            f"{to_user.mention}!"
        )


async def setup(bot):
    await bot.add_cog(EconomyCog(bot))