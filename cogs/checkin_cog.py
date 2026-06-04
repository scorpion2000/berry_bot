import discord

from discord.ext import commands
from discord import app_commands
from discord.ext import tasks
from config import MAX_LEVEL

class CheckInCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.checkin = bot.checkin_service
        self.timeout_sweep.start()

    def cog_unload(self):
        self.timeout_sweep.cancel()

    @tasks.loop(hours=1)
    async def timeout_sweep(self):
        reset_ids = self.checkin.sweep_timeouts()

        # Old implementation for dms was here, decided that was too invasive

    @timeout_sweep.before_loop
    async def before_sweep(self):
        await self.bot.wait_until_ready()

    @app_commands.command(
        name="check-in",
        description="Daily check-in to level up your bit rewards! (Resets after 48 hours of inactivity)"
    )
    async def check_in(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        result = self.checkin.check_in(user_id)

        if result["status"] == "already_checked_in":
            await interaction.response.send_message(
                f"You've already checked in today, {interaction.user.mention}! "
                f"Come back tomorrow to keep your streak going.\n"
                f"You now receive {1+result["level"]} bits per message!",
                ephemeral=True
            )
            return

        line = ""

        if result["capped"]:
            line = f"Checked in! You've reached the max extra rewards — keep checking in to not loose it, {interaction.user.mention}!"
        else:
            line = f"Checked in! You now receive {1+result["level"]} bits per message!, {interaction.user.mention}!"

        await interaction.response.send_message(line)


async def setup(bot):
    await bot.add_cog(CheckInCog(bot))
