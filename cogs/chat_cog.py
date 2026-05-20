from discord.ext import commands

class ChatCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.chat_service = bot.chat_service
        self.joke_service = bot.joke_service

    @commands.Cog.listener()
    async def on_message(self, message):

        # Ignore self
        if message.author.bot:
            return

        # Check if berry was mentioned
        berry_mentioned = self.chat_service.is_berry_mentioned(message.content)

        if not berry_mentioned:
            return

        # Generate response
        response = self.chat_service.get_response(message.content, berry_mentioned)

        if response:
            await message.channel.send(response)


async def setup(bot):
    await bot.add_cog(ChatCog(bot))