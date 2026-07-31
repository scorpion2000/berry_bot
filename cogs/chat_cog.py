from discord.ext import commands
from discord import app_commands
from config import chat_channel

class ChatCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.chat_service = bot.chat_service
        self.joke_service = bot.joke_service
        self.checkin_service = bot.checkin_service
        self.banking = bot.banking_service
        self.chat_channel = chat_channel

    @commands.Cog.listener()
    async def on_message(self, message):

        # Ignore self
        if message.author.bot:
            return

        self.banking.add_bits(message.author.name, 1 + self.checkin_service.get_level(message.author.id)["level"])

        if message.channel.id != chat_channel:
            return

        # Check if berry was mentioned
        berry_mentioned = self.chat_service.is_berry_mentioned(message.content)

        if not berry_mentioned:
            return

        # Generate response
        response = self.chat_service.get_response(message.content, berry_mentioned)

        if response:
            await message.channel.send(response)

    """@app_commands.command(
        name="help",
        description="List all of Berry's functionalities!"
    )
    async def help(self, interaction: discord.Interaction, to_user: discord.User, amount: int):

        await interaction.response.send_message(
            f"**Banking**\n"
            f"You generally get one bit per message you sent. "
            f"use `/send_bits` to send bits to your friends"
            f"{amount} bits to "
            f"{to_user.mention}!",
            ephemeral=True
        )"""


async def setup(bot):
    await bot.add_cog(ChatCog(bot))