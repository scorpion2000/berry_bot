import discord
import os
from discord.ext import commands
from services.chat_service import ChatService
from services.joke_service import JokeService
from services.banking_service import BankingService
from services.room_service import RoomService
from services.changelog_service import ChangelogService
from services.bit_role_service import BitRoleService
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

class BerryFlames(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()
        intents.message_content = True
        intents.presences = True
        intents.members = True

        super().__init__(intents = intents, command_prefix='$')

        # Services
        self.chat_service = ChatService()
        self.joke_service = JokeService()
        self.banking_service = BankingService()
        self.room_service = RoomService()
        self.changelog_service = ChangelogService()
        self.bit_role_service = BitRoleService()

    async def setup_hook(self):

        # Load cogs
        await self.load_extension("cogs.chat_cog")
        await self.load_extension("cogs.bank_cog")
        await self.load_extension("cogs.rooms_cog")
        await self.load_extension("cogs.changelog_cog")
        await self.load_extension("cogs.bit_role_cog")
        await self.tree.sync()


bot = BerryFlames()

bot.run(TOKEN)