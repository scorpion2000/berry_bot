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
    
    @app_commands.command(
        name="get_bits",
        description="Check how many bits you have in the bank!"
    )
    async def get_bits(self, interaction: discord.Interaction):
        sender = interaction.user

        bits = self.banking.get_balance(sender.name)

        await interaction.response.send_message(
            f"You currently own {bits} bits!",
            ephemeral=True
        )
    
    @app_commands.command(
        name="get_top_bit_holders",
        description="Get the top 5 bit holders in the server!"
    )
    async def get_top_bit_holders(self, interaction: discord.Interaction):
        sorted_items = self.banking.get_top_bit_holders(5)
        results = []
        for key, value in sorted_items:
            results.append(f'{key} has: {value} bits!')
        response = "\n".join(results)
        await interaction.response.send_message(response)


async def setup(bot):
    await bot.add_cog(BankingCog(bot))