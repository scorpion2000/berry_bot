import discord

from discord.ext import commands
from discord import app_commands


class RoomsCog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.rooms = bot.room_service

    @app_commands.command(
        name="create_room",
        description="Creates a private room."
    )
    async def create_room(self, interaction: discord.Interaction, user1: discord.User,user2: discord.User, channel_name: str):
        if not self.rooms.can_create_room_here(interaction.channel):
            await interaction.response.send_message(
                "You can't use that here.",
                ephemeral=True
            )

            return

        channel = await self.rooms.create_room(interaction.guild, user1, user2, channel_name)

        await channel.send(f"Welcome {user1.mention} and {user2.mention}!")

        await interaction.response.send_message(f"Created {channel.mention}", ephemeral=True)

    @app_commands.command(name="archive", description="Archives this room.")
    async def archive(self, interaction: discord.Interaction):
        if not self.rooms.is_admin(interaction.user):
            await interaction.response.send_message(
                "Admins only.",
                ephemeral=True
            )
            return

        if not self.rooms.is_private_room(interaction.channel):
            await interaction.response.send_message(
                "Not a private room.",
                ephemeral=True
            )
            return

        await self.rooms.archive_room(interaction.channel, interaction.guild)

        await interaction.response.send_message(
            "Room archived.",
            ephemeral=True
        )

    @app_commands.command(
        name="invite",
        description="Invite a user."
    )
    async def invite(self, interaction: discord.Interaction, user: discord.User):
        if not self.rooms.is_private_room(interaction.channel):
            await interaction.response.send_message(
                "Not a private room.",
                ephemeral=True
            )
            return

        await self.rooms.invite_user(interaction.channel,user)

        await interaction.channel.send(f"{user.mention} was invited by {interaction.user.mention}")

        await interaction.response.send_message(
            "User invited!",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(RoomsCog(bot))