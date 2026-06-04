import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
from typing import List

class BitRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = bot.bit_role_service
        self.banking = bot.banking_service
        self.check_for_expired_roles.start()
        self.bit_bag_emoji_id = 1510292970585460928

    @app_commands.command(
        name="bit_role",
        description="Create a reaction role that will cost bits!"
    )
    @app_commands.choices(duration=[
        app_commands.Choice(name="1 Hour", value="hour"),
        app_commands.Choice(name="1 Day", value="day"),
        app_commands.Choice(name="1 Month", value="month"),
        app_commands.Choice(name="2 Months", value="2months"),
        app_commands.Choice(name="3 Months", value="3months"),
        app_commands.Choice(name="6 Months", value="6months"),
        app_commands.Choice(name="1 Year", value="year"),
        app_commands.Choice(name="Indefinite", value="indefinite"),
    ])
    async def bit_role(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        cost: int,
        duration: app_commands.Choice[str]
    ):
        emoji = "<:bit_bag:1510292943423012994>"
        embed = discord.Embed(
            title=f"{role.mention} now available!",
            description=(
                f"React with {emoji} to get {role.mention}\n"
                f"Price: {cost} bits\n"
                f"Lasts for {duration.name}"
            ),
            color=discord.Color.teal()
        )

        message = await interaction.channel.send(embed=embed)
        await message.add_reaction(emoji)

        data = self.service.load_data()

        data[str(message.id)] = {
            "role_id": role.id,
            "cost": cost,
            "duration": duration.value,
            "guild_id": interaction.guild.id
        }

        self.service.save_data(data)

        await interaction.response.send_message(
            "Bit role created! Let the bits flow~",
            ephemeral=True
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.id != 1510292943423012994:
            return
        
        data = self.service.load_data()

        if str(payload.message_id) not in data:
            return
        
        role_data = data[str(payload.message_id)]

        guild = self.bot.get_guild(role_data["guild_id"])
        if not guild:
            return

        member = guild.get_member(payload.user_id)
        if not member:
            return

        role = guild.get_role(role_data["role_id"])
        if not role:
            return

        cost = role_data["cost"]

        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if not self.banking.add_bits(member.name, -cost):
            await message.remove_reaction(emoji, member)
            return

        await member.add_roles(role)

        expiry = self.service.create_expiry(role_data["duration"])

        active_roles = data.get("active_roles", [])

        active_roles.append({
            "user_id": member.id,
            "role_id": role.id,
            "guild_id": guild.id,
            "expiry": expiry,
        })

        data["active_roles"] = active_roles

        self.service.save_data(data)

    @tasks.loop(minutes=1)
    async def check_for_expired_roles(self):
        data = self.service.load_data()

        active_roles = data.get("active_roles", [])

        now = datetime.utcnow().timestamp()

        remaining_roles = []

        for entry in active_roles:
            if entry["expiry"] is None:
                remaining_roles.append(entry)
                continue

            if now >= entry["expiry"]:
                guild = self.bot.get_guild(entry["guild_id"])

                if guild:
                    member = guild.get_member(entry["user_id"])
                    role = guild.get_role(entry["role_id"])

                    if member and role:
                        await member.remove_roles(role)
            else:
                remaining_roles.append(entry)

        data["active_roles"] = remaining_roles

        self.service.save_data(data)
    
    @check_for_expired_roles.before_loop
    async def before_checking_for_expired_roles(self):
        await self.bot.wait_until_ready()

    @app_commands.command(
        name="bit_role_clear",
        description="Times out all roles "
    )
    async def bit_role_clear(
        self,
        interaction: discord.Interaction
    ):
        data = self.service.load_data()
        active_roles = data.get("active_roles", [])
        print(active_roles)

        remaining_roles = []


        for entry in active_roles:
            if entry["expiry"] is None:
                remaining_roles.append(entry)
                continue

            if True:
                guild = self.bot.get_guild(entry["guild_id"])

                if guild:
                    member = guild.get_member(entry["user_id"])
                    role = guild.get_role(entry["role_id"])

                    if member and role:
                        await member.remove_roles(role)
            else:
                remaining_roles.append(entry)

        data["active_roles"] = remaining_roles

        self.service.save_data(data)

async def setup(bot):
    await bot.add_cog(BitRoleCog(bot))