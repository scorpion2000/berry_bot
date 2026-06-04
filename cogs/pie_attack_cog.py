import discord

from discord.ext import commands
from discord import app_commands
from config import chat_channel


class PieAttackCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.pie = bot.pie_attack_service
        self.banking = bot.banking_service
        self.general_chat_id = chat_channel

    @app_commands.command(
        name="pie_attack",
        description="Launch a secret pie attack on an unsuspecting victim!"
    )
    @app_commands.describe(
        victim="The user who will be pied.",
        scope="Where the pie can be delivered."
    )
    @app_commands.choices(scope=[
        app_commands.Choice(name="General Chat (30 bits)", value="General Chat"),
        app_commands.Choice(name="Everywhere! (100 bits)",   value="Everywhere"),
    ])
    async def pie_attack(
        self,
        interaction: discord.Interaction,
        victim: discord.User,
        scope: app_commands.Choice[str],
    ):
        val = -30 if scope.value == "General Chat" else -100
        if not self.banking.add_bits(interaction.user.name, val):
            await interaction.response.send_message(
                "You don't seem to have enough bits for this!",
                ephemeral=True
            )
            return

        if victim.id == interaction.user.id:
            await interaction.response.send_message(
                "You can't pie yourself, silly!",
                ephemeral=True
            )
            return

        if self.pie.is_under_attack(victim.id):
            await interaction.response.send_message(
                f"{victim.display_name} is already being targeted! Patience!",
                ephemeral=True
            )
            return

        target = self.pie.start_attack(victim, scope.value)

        await interaction.response.send_message(
            f"🥧 Pie attack launched on **{victim.display_name}**! "
            f"Counting their messages in **{scope.value}**. "
            f"They'll never see it coming... (will be hit in {target} messages)",
            ephemeral=True
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if not self.pie.should_track(message, self.general_chat_id):
            return

        hit = self.pie.record_message(message)

        if hit:
            attack = self.pie.pop_attack(message.author.id)

            await message.add_reaction("🥧")

            await message.channel.send(
                f"{message.author.mention} PIE ATTACK! You've been pied! :3"
            )


async def setup(bot):
    await bot.add_cog(PieAttackCog(bot))
