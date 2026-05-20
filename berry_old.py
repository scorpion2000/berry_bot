import discord
import random
import json
import re
import asyncio
from urllib.request import urlopen
from discord.ext import commands, tasks
from discord import app_commands
from pprint import pprint
from datetime import datetime
import zoneinfo
try:
    import cPickle as pickle
except ImportError:  # Python 3.x
    import pickl
from config import chat_channel

berry_bit_bank = {}
game_blackjack_players = {}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

try:
    with open('bit_bank.json', 'r') as fp:
        berry_bit_bank = json.load(fp)
except Exception as e:
    print('Bit bank save probably does not exist...')
    print(e)

class BerryFlames(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.presences = True
        intents.members = True
        super().__init__(intents = intents)
        self.tree = app_commands.CommandTree(self)
        self.last_run = None
        self.cet = zoneinfo.ZoneInfo("Europe/Budapest")

    async def setup_hook(self):
        await self.tree.sync()
        #self.check_time.start()

    async def on_ready(self):
        print(f'We have logged in as {client.user}')

    @tasks.loop(minutes=1)
    async def check_time(self):
        print("minute check")
        now = datetime.now(self.cet)
        print(f'{now.hour} : {now.minute}')
        if True or (now.hour == 0 and now.minute == 9):
            print("Good time")
            if self.last_run == now.date():
                return
            
            print("Getting my owner")
            self.last_run = now.date()
            guild = self.get_guild(1237887421153280040)
            if not guild:
                return
            member = guild.get_member(my_creators_user_id)

            print("Sending the message")
            print(member.status)
            if member.status != discord.Status.offline:
                print("Sending for real")
                channel = await self.fetch_channel(chat_channel)
                print(channel)
                await channel.send(f"{member.mention} go to sleep! It's past midnight!")
    
    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.channel.id != chat_channel:
            await self.ber_checkForBumps(message)
            return
        
        berry_mentioned = any(word in message.content.lower() for word in ["berry", "berry flames"])

        await self.manage_bank_account(message.author, 1)
        
        #print(f'Message from {message.author}: {message.content}')

        if await self.ber_game_blackjack(message, berry_mentioned): return

        # Reply tests
        if await self.ber_reply_bankMention(message, berry_mentioned): return
        if await self.ber_reply_bankCheck(message, berry_mentioned): return
        if await self.ber_reply_bankTopHolders(message, berry_mentioned): return
        if await self.ber_reply_berryPat(message, berry_mentioned): return
        if await self.ber_reply_rollDice(message, berry_mentioned): return
        if await self.ber_reply_randomJoke(message, berry_mentioned): return
        if await self.ber_reply_curseMe(message, berry_mentioned): return
        #if await self.ber_reply_creator(message): return
        if await self.ber_reply_love(message, berry_mentioned): return
        if await self.ber_reply_callout(message, berry_mentioned): return
        if await self.ber_reply_question(message, berry_mentioned): return
        if await self.ber_reply_penisJoke(message, berry_mentioned): return
        if random.randint(1, 100) > 2:
            return
            
        response = random.choice(random_responses)
        #await message.channel.send(response)

    async def ber_checkForBumps(self, message):
        print("Potential bot message:")
        print(f"Message sender: {message.author}")
        if (message.reference):
            ref = await message.channel.fetch_message(message.reference.message_id)
            print(f"Reply to: {ref.author}")
        if "bump" in message.content.lower():
            print("Message contains a bump")
        if message.embeds:
            embed = message.embeds[0]
            if embed.description and "Bump done!" in embed.description:
                print("Detected bump")
        if message.author.id == 302050872383242240:
            print("Message by disboard")


    async def ber_reply_berryPat(self, message, berry_mentioned):
        if not berry_mentioned:
            return False
        if "pats berry" in message.content.lower() or "pat berry" in message.content.lower():
            await message.channel.send("eep!")
            await self.manage_bank_account(message.author, 2)
            return True
        return False

    async def ber_reply_bankTopHolders(self, message, berry_mentioned):
        if not berry_mentioned:
            return False
        if ("who has" in message.content.lower() or "who owns" in message.content.lower() or "who holds" in message.content.lower()) and "the most" in message.content.lower() and "bits" in message.content.lower():
            await message.channel.send("sure! here are the top five bit holders:")

            sorted_items = sorted(berry_bit_bank.items(), key=lambda x: x[1], reverse=True)[:5]
            results = []
            for key, value in sorted_items:
                results.append(f'{key} has: {value} bits!')
            response = "\n".join(results)
            await message.channel.send(response)

            if len(sorted_items) < 5:
                await message.channel.send("it seems i have less than five accounts in my bank..")
            return True
        return False

    async def ber_reply_bankCheck(self, message, berry_mentioned):
        if not berry_mentioned:
            return False
        if "how many" in message.content.lower() and "bits" in message.content.lower():
            await message.channel.send(f'You have {berry_bit_bank.get(message.author.name, 0)} bits!')
            if berry_bit_bank.get(message.author.name, 0) < 100 and random.randint(1, 100) < 10:
                await message.channel.send(f'i feel so bad... here, have 20 bits!')
                await self.manage_bank_account(message.author, 20)
            if message.author.name == "hullahopp" and random.randint(1, 100) > 10:
                await message.channel.send("as my creator, i feel the need to remind you not to cheat with my bank..!")
            return True
        return False

    async def ber_reply_bankMention(self, message, berry_mentioned):
        if not berry_mentioned:
            return False
        if "bank" in message.content.lower() and ("are you" in message.content.lower() or "do you" in message.content.lower()):
            await message.channel.send("I manage all your bits!")
            return True
        return False

    async def ber_reply_randomJoke(self, message, berry_mentioned):
        if not berry_mentioned:
            return False
        if any(word in message.content.lower() for word in random_joke_words):
            print("I think they want me to tell a joke")
            if "joke" in message.content.lower():
                joke = await self.get_joke()
                await message.channel.send(
                    f"{joke['setup']}\n{joke['punchline']}"
                )
                return True
        return False

    async def ber_reply_penisJoke(self, message, fixed_message):
        if any(word in message.content.lower() for word in penisJoke_words):
            if not fixed_message and random.randint(1, 100) > 20:
                print("Penis found, decided to say nothing")
                return False
            
            response = random.choice(penisJoke_responses)
            await message.channel.send(response)
            return True
        return False

    async def ber_reply_curseMe(self, message, berry_mentioned):
        if not berry_mentioned:
            return False
        
        if any(word in message.content.lower() for word in curse_words):
            response = random.choice(curse_responses)
            await message.channel.send(response)
            return True
        return False

    async def ber_reply_rollDice(self, message, berry_mentioned):
        if not berry_mentioned:
            return False
        
        if "roll" in message.content.lower():
            if "dice" in message.content.lower():
                d = random.randint(1, 20)
                await message.channel.send(f'{d}!')
                return True
            match = re.search(r"d(\d+)", message.content.lower())
            if not match:
                return False
            d = random.randint(1, int(match.group(1)))
            await message.channel.send(f'{d}!')
            return True
        return False

    async def ber_reply_creator(self, message):
        if message.author.display_name != "Hulla~":
            return False
        if random.randint(1, 100) > 5:
            print("My creator said something! But I was too shy..")
            return False
        response = random.choice(creator_responses)
        await message.channel.send(response)
        return True

    async def ber_reply_love(self, message, berry_mentioned):
        if not berry_mentioned:
            return False

        if any(word in message.content.lower() for word in love_words):
            response = random.choice(love_responses)
            await message.channel.send(response)
            return True
        return False
    
    async def ber_reply_callout(self, message, berry_mentioned):
        if not berry_mentioned:
            return False
        
        if message.content.lower() == "berry" or message.content.lower() == "berry!":
            response = random.choice(berry_responses)
            await message.channel.send(response)
            return True
        print("My name was mentioned, but they clearly ment regular berries...")
        return False
    
    async def ber_reply_question(self, message, berry_mentioned):
        if not berry_mentioned:
            return False
        if "?" in message.content.lower():
            response = random.choice(random_reply_responses)
            await message.channel.send(response)
            return True
        return False

    async def get_joke(self):
        url = "https://official-joke-api.appspot.com/random_joke"

        with urlopen(url) as response:
            data = response.read()
            return json.loads(data)

    async def manage_bank_account(self, user, bits):
        print(f'Adding {bits} bits for {user.name} who currently owns {berry_bit_bank.get(user.name, 0)}')
        if (berry_bit_bank.get(user.name, 0) + bits) < 0:
            return False
        berry_bit_bank.update({user.name : berry_bit_bank.get(user.name, 0) + bits})
        with open('bit_bank.json', 'w') as fp:
            json.dump(berry_bit_bank, fp)
        return True
    
    async def ber_game_blackjack(self, message, berry_mentioned):
        if not berry_mentioned:
            return False

        if "hit me" in message.content.lower():
            total = await self.ber_game_blackjack_playCards(True, game_blackjack_players.get(message.author.name)[1], message)
            game_blackjack_players.update({message.author.name : [game_blackjack_players.get(message.author.name)[0], game_blackjack_players.get(message.author.name)[1] + total]})
            if not await self.ber_game_blackjack_checkWinCondition(game_blackjack_players.get(message.author.name)[1], message.author, game_blackjack_players.get(message.author.name)[0], message): #This looks like ass
                await message.channel.send("shall I hit you, or will you stay?")
            return True

        if "i stay" in message.content.lower():
            await message.channel.send(f"staying? Okay, my turn! :3")
            berry_total = 0
            berry_total += await self.ber_game_blackjack_playCards(False, berry_total, message)
            if berry_total > game_blackjack_players.get(message.author.name)[1]:
                await message.channel.send(f"hehe, thanks for the {game_blackjack_players.get(message.author.name)[0]} bits!")
                game_blackjack_players.update({message.author.name : [0, 0]})
                manage_bank_account(message.author, wager)
            while True: # Gotta be careful here
                await asyncio.sleep(1)
                berry_total += await self.ber_game_blackjack_playCards(True, berry_total, message)

                if berry_total > 21:
                    await message.channel.send(f"crap.. alright, here's your {game_blackjack_players.get(message.author.name)[0]} bits!")
                    game_blackjack_players.update({message.author.name : [0, 0]})
                    manage_bank_account(message.author, wager)
                    return True
                if berry_total > game_blackjack_players.get(message.author.name)[1]:
                    await message.channel.send("i win! I'll take your {game_blackjack_players.get(message.author.name)[0]} bits now, thank you!")
                    game_blackjack_players.update({message.author.name : [0, 0]})
                    manage_bank_account(message.author, -wager)
                    return True

        if "blackjack" in message.content.lower() and "bits" in message.content.lower():
            if game_blackjack_players.get(message.author.name, [0, 0])[0] != 0:
                await message.channel.send('you already have a blackjack game going! cancel, or finish it!')
            match = re.search(r"\d+", message.content.lower())
            wager = int(match.group()) if match else 0

            if wager < 10:
                await message.channel.send('err.. that is not a valid wager. you need at least 10 bits')
                return True
            if wager > berry_bit_bank.get(message.author.name, 0):
                await message.channel.send("you don't have enough bits to play! :c")
                return True
            
            total = await self.ber_game_blackjack_playCards(False, 0, message)
            game_blackjack_players.update({message.author.name : [wager, total]})
            if not await self.ber_game_blackjack_checkWinCondition(game_blackjack_players.get(message.author.name)[1], message.author, game_blackjack_players.get(message.author.name)[0], message): #This looks like ass
                await message.channel.send("shall I hit you, or will you stay?")

        if "blackjack" in message.content.lower() and "cancel" in message.content.lower():
            if game_blackjack_players.get(message.author.name, [0, 0])[0] != 0:
                game_blackjack_players.update({message.author.name : [0, 0]})
                await message.channel.send('alright, i cancelled your blackjack game! no bits lost!')
                return True
        return False

    async def ber_game_blackjack_playCards(self, single, current_total, message):
        card_num = 3 if not single else 2
        total = 0
        cards = []
        for x in range(1, card_num):
            i = random.randint(1, 13)
            if i == 1:
                if current_total + 11 > 21:
                    total += 1
                else:
                    total += 11
            elif i > 10:
                total += 10
            else:
                total += i
            
            if i == 1:
                cards.append("Ace")
            elif i == 11:
                cards.append("Jack")
            elif i == 12:
                cards.append("Queen")
            elif i == 13:
                cards.append("King")
            else:
                cards.append(str(i))
        if card_num == 3:
            await message.channel.send(f'the cards are... {cards[0]} and {cards[1]}! the total is: {current_total+total}')
        else:
            await message.channel.send(f'next card is... {cards[0]}! the total is: {current_total+total}')
        return total

    async def ber_game_blackjack_checkWinCondition(self, current_total, user, wager, message):
        if current_total > 21:
            await message.channel.send(f"busted! I'll take your {wager} bits >:3")
            game_blackjack_players.update({user.name : [0, 0]})
            manage_bank_account(user, -wager)
            return True
        if current_total == 21:
            await message.channel.send(f"you won! Here's your {wager} bits! ^^")
            game_blackjack_players.update({user.name : [0, 0]})
            manage_bank_account(user, wager)
            return True
        return False


client = BerryFlames()

@client.tree.command(name="send_bits", description="CreSend your bits to someone else!")
async def create_channel(interaction: discord.Interaction, to_user: discord.User, amount: int):
    sender = interaction.user
    bits = 0 - amount
    if (berry_bit_bank.get(sender.name, 0) + bits) < 0:
        await interaction.response.send_message(f"You only have {berry_bit_bank.get(sender.name, 0)} bits!", ephemeral=True)
        return
    berry_bit_bank.update({sender.name : berry_bit_bank.get(sender.name, 0) + bits})
    berry_bit_bank.update({to_user.name : berry_bit_bank.get(to_user.name, 0) + amount})
    with open('bit_bank.json', 'w') as fp:
        json.dump(berry_bit_bank, fp)
    await interaction.response.send_message(f'Hey {to_user.mention}, {sender.mention} sent you {amount} bits!')

@client.tree.command(name="create_room", description="Creates a private channel for two people.")
async def create_channel(interaction: discord.Interaction, user1: discord.User, user2: discord.User, channel_name: str):
    curr_channel = interaction.channel
    print(f'Custom channel creation started from: {curr_channel.category.id}, it needs to be in {room_creation_channel}')
    if not curr_channel.category or curr_channel.category.id != room_creation_channel:
        await interaction.response.send_message("I can't let you use that command here~. Go to https://discord.com/channels/1237887421153280040/1238264672642142390", ephemeral=True)
        return
    channel_name = channel_name.replace(" ", "-")
    channel_name = channel_name.lower()

    guild = interaction.guild
    category = guild.get_channel(main_category_id)

    perm_overrides = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user1: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        user2: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }

    channel = await guild.create_text_channel(
        channel_name,
        category=category,
        overwrites=perm_overrides
    )

    await channel.send(
        f'Welcome to your private room, {user1.mention} and {user2.mention}!\n'
        f'This is channel is restricted to you, and the admins. Server rules still apply!\n'
        f'You can use `/invite` here to get more people in, should you need~\n'
        f'Enjoy your stay!'
    )

    await interaction.response.send_message(f'Creating room for {user1.display_name} and {user2.display_name}, called {channel_name} ;3')

@client.tree.command(name="archive", description="Moves this channel to the archives, and removes writing permissions.")
async def archive(interaction: discord.Interaction):
    if not any((role.name == "Admin" or role.name == "Trial Mod") for role in interaction.user.roles):
        await interaction.response.send_message("Only admins can archive a channel. Tag one!", ephemeral=True)
        return
    
    channel = interaction.channel
    guild = interaction.guild

    if not channel.category or channel.category.id != main_category_id:
        await interaction.response.send_message("I can't let you use that command here~", ephemeral=True)
        return

    archive_category = guild.get_channel(archive_category_id)

    perm_overrides = channel.overwrites
    for target, overwrite in perm_overrides.items():
        if isinstance(target, discord.Member):
            if any((role.name == "Admin" or role.name == "Trial Mod") for role in target.roles):
                continue
        elif isinstance(target, discord.Role):
            if target.name == "Admin" or target.name == "Trial Mod":
                continue

        overwrite.send_messages = False
        overwrite.manage_messages = False
        perm_overrides[target] = overwrite

    await channel.edit(
        category = archive_category,
        overwrites = perm_overrides
    )

    await interaction.response.send_message(f'{channel.mention} has been archived! Hope you all enjoyed your stay~', ephemeral=True)

@client.tree.command(name="invite", description="Invites another user to a private channel.")
async def invite_user(interaction: discord.Interaction, user: discord.User):
    channel = interaction.channel

    if not channel.category or channel.category.id != main_category_id:
        await interaction.response.send_message("Err.. this is not a private channel~", ephemeral=True)
        return
    
    perm_overrides = channel.overwrites
    perm_overrides[user] = discord.PermissionOverwrite(
        view_channel=True,
        send_messages=True
    )

    await channel.edit(overwrites=perm_overrides)

    await channel.send(
        f"Hey {user.mention}! You've been invited by {interaction.user.mention} to the channel. Have fun~"
    )

    await interaction.response.send_message(f'{user.mention} successfully invited! Mwah~', ephemeral=True)

client.run('MTQ5OTQwMzExMTYyOTA2MjMxNQ.GayhtV.qprTYPGRRcZt4JsHclQ0Ts6XD9dBDEJ1efy8Gc')