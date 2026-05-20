import discord

from discord.ext import commands
from discord import app_commands

class BankingCog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.banking = bot.banking_service

    @app_commands.command(
        name="send_bits",
        description="Send your bits to someone else!"
    )
    async def send_bits(self, interaction: discord.Interaction, to_user: discord.User, amount: int):
        sender = interaction.user

        success, error = self.banking.transfer_bits(sender.name,to_user.name,amount)

        if not success:
            await interaction.response.send_message(error,ephemeral=True)
            return

        await interaction.response.send_message(
            f"{sender.mention} sent "
            f"{amount} bits to "
            f"{to_user.mention}!"
        )


async def setup(bot):
    await bot.add_cog(BankingCog(bot))