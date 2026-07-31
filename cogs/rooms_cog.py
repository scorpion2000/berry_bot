import discord

from discord.ext import commands
from discord import app_commands
from config import member_role_id


class RoomsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rooms = bot.room_service
        self.member_role_id = member_role_id

    @app_commands.command(
        name="create_room",
        description="Creates a private room."
    )
    async def create_room(self, interaction: discord.Interaction, your_partner: discord.User, channel_name: str):
        if not self.rooms.can_create_room_here(interaction.channel):
            await interaction.response.send_message(
                "You can't use that here!",
                ephemeral=True
            )
            return
        creator = interaction.user

        channel = await self.rooms.create_room(interaction.guild, creator, your_partner, channel_name)

        await channel.send(
            f"Welcome to your private room, {creator.mention} and {your_partner.mention}!\n"
            f'This is channel is restricted to you, and the admins. Server rules still apply!\n'
            f'You can use `/invite` here to get more people in, should you need~\n'
            f'Lastly, use `/toggle_room_visibility` to make this channel visible to every server member!\n'
            f'Enjoy your stay!'
        )

        await interaction.response.send_message(f"Created {channel.mention}", ephemeral=True)

    @app_commands.command(name="archive", description="Archives this room.")
    async def archive(self, interaction: discord.Interaction):
        if not self.rooms.is_admin(interaction.user):
            await interaction.response.send_message(
                "Admins only!",
                ephemeral=True
            )
            return

        if not self.rooms.is_private_room(interaction.channel):
            await interaction.response.send_message(
                "Not a private room!",
                ephemeral=True
            )
            return

        await self.rooms.archive_room(interaction.channel, interaction.guild)

        await interaction.response.send_message(
            "Room archived!",
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

        await interaction.channel.send(f"Hey {user.mention}, you were invited by {interaction.user.mention}!")

        await interaction.response.send_message(
            "User invited!",
            ephemeral=True
        )

    @app_commands.command(
        name="toggle_room_visibility",
        description="Toggle the visibiltiy of your room for members!"
    )
    async def toggle_room_visibility(
        self,
        interaction: discord.Interaction
    ):
        member_role = interaction.guild.get_role(self.member_role_id)

        overwrite = interaction.channel.overwrites_for(member_role)
        visible = overwrite.view_channel
        overwrite.view_channel = not visible

        await interaction.channel.set_permissions(
            member_role,
            overwrite=overwrite
        )

        visibility_state = "visible to" if overwrite.view_channel else "hidden from"

        await interaction.response.send_message(
            f"Room is now {visibility_state} all members!\nRemember, you still need to `/invite` chat participants (spam protection)!"
        )


async def setup(bot):
    await bot.add_cog(RoomsCog(bot))