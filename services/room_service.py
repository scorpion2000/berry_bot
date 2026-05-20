import discord
from config import main_category_id
from config import archive_category_id
from config import room_creation_channel

class RoomService:
    def __init__(self):
        self.main_category_id = main_category_id
        self.archive_category_id = archive_category_id
        self.room_creation_channel = room_creation_channel

    def is_admin(self, member):
        return any(role.name in ["Admin", "Trial Mod"]for role in member.roles)
    
    def is_private_room(self, channel):
        return (channel.category and channel.category.id == self.main_category_id)

    def can_create_room_here(self, channel):
        return (channel.category and channel.category.id == self.room_creation_channel)
    
    async def create_room(self, guild, user1, user2, channel_name):
        category = guild.get_channel(self.main_category_id)

        channel_name = (channel_name.replace(" ", "-").lower())

        overwrites = {
            guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            user1:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True
                ),

            user2:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True
                )
        }   # This sudden indent will forever piss me off in python

        channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)

        return channel
    
    async def archive_room(self, channel, guild):
        archive_category = guild.get_channel(self.archive_category_id)

        overwrites = channel.overwrites

        for target, overwrite in overwrites.items():
            if isinstance(target, discord.Member):
                if self.is_admin(target):
                    continue
            elif isinstance(target, discord.Role):
                if target.name in ["Admin", "Trial Mod"]:
                    continue

            overwrite.send_messages = False
            overwrite.manage_messages = False

            overwrites[target] = overwrite

        await channel.edit(
            category=archive_category,
            overwrites=overwrites
        )
    
    async def invite_user(self, channel, user):
        overwrites = channel.overwrites
        overwrites[user] = (
            discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True
            )
        )

        await channel.edit(
            overwrites=overwrites
        )