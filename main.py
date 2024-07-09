import os
import random
import sys
import logging
import asyncio
from discord import Intents, Client, Message
from flask import Flask, send_from_directory

# Setup logging to standard output to monitor bot activity
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Setup Flask for health check
app = Flask(__name__)

# Define a static map pool
MAP_POOL = ['dust2', 'mirage', 'inferno', 'nuke', 'train', 'vertigo', 'ancient', 'anubis', 'cache']

# Define the directory to serve static files
HEALTH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'health')

@app.route('/')
def health_check():
    return send_from_directory(HEALTH_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(HEALTH_DIR, filename)

# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
# Load the TOKEN variable from os ENVIRONMENT variables
TOKEN = os.getenv('TOKEN')

# STEP 1: BOT SETUP
# Setup the bot's intents to receive specific events
intents: Intents = Intents.default()
intents.message_content = True  # Allows the bot to read message content
client: Client = Client(intents=intents)

# STEP 2: MESSAGE FUNCTIONALITY
# Define the event handler for incoming messages
@client.event
async def on_message(message: Message) -> None:
    # Ignore messages sent by the bot itself to prevent feedback loop
    if message.author == client.user:
        return


    # Handle the !mix_teams command
    if message.content.startswith('!mix_team') or message.content.startswith('!mix_teams'):
        players = message.content.split()[1:]
        # Check if the correct number of players is provided
        if len(players) != 10:
            await message.channel.send('You need to provide exactly 10 player names.')
            return

        # Capitalize player names
        players = [player.capitalize() for player in players]

        # Shuffle players and divide them into two teams
        random.shuffle(players)
        team1 = players[:5]
        team2 = players[5:]

        # Shuffle players and divide them into two teams
        random.shuffle(players)
        team1 = players[:5]
        team2 = players[5:]

        # Create the table-like structure for display
        team1_table = "\n".join(team1)
        team2_table = "\n".join(team2)
        
        response = (
            "```\n"
            f"Team A:\n{team1_table}\n"
            "```\n"
            "```\n"
            f"Team B:\n{team2_table}\n"
            "```"
        )

        # Send the formatted teams to the channel
        await message.channel.send(response)

    # Handle the !mix_pair command
    if message.content.startswith('!mix_pairs') or message.content.startswith('!mix_pair'):
        players = message.content.split()[1:]
        # Check if the correct number of players is provided
        if len(players) != 10:
            await message.channel.send('You need to provide exactly 10 player names.')
            return

        # Capitalize player names
        players = [player.capitalize() for player in players]

        # Create pairs of players
        pairs = [(players[i], players[i+1]) for i in range(0, len(players), 2)]
        
        # Generate a random 5-bit binary number
        binary_number = f"{random.randint(0, 31):05b}"  # 31 is 11111 in binary

        # Split players into teams based on the binary number
        team1 = []
        team2 = []
        for i, bit in enumerate(binary_number):
            if bit == '0':
                team1.append(pairs[i][0])
                team2.append(pairs[i][1])
            else:
                team1.append(pairs[i][1])
                team2.append(pairs[i][0])

        # Create the table-like structure for display
        team1_table = "\n".join(team1)
        team2_table = "\n".join(team2)
        
        response = (
            "```\n"
            f"Team A:\n{team1_table}\n"
            "```\n"
            "```\n"
            f"Team B:\n{team2_table}\n"
            "```"
        )

        # Send the formatted teams to the channel
        await message.channel.send(response)

    # Handle the !mix_map and !mix_maps commands
    elif message.content.startswith('!mix_map') or message.content.startswith('!mix_maps'):
        maps = message.content.split()[1:]
        
        # Use the predefined map pool if no maps are provided
        if not maps:
            maps = MAP_POOL

        # Select a random map from the provided options
        selected_map = random.choice(maps)
        selected_map_uppercase = selected_map.upper()
        # Send the chosen map to the channel in bold and larger text
        await message.channel.send(f'# **__MAP: {selected_map_uppercase}__**')


    # Handle the !mix_all commands
    elif message.content.startswith('!mix_all'):
        players = message.content.split()[1:]
        # Check if the correct number of players is provided
        if len(players) != 10:
            await message.channel.send('You need to provide exactly 10 player names.')
            return

        # Capitalize player names
        players = [player.capitalize() for player in players]

        # Shuffle players and divide them into two teams
        random.shuffle(players)
        team1 = players[:5]
        team2 = players[5:]

        # Shuffle players and divide them into two teams
        random.shuffle(players)
        team1 = players[:5]
        team2 = players[5:]

        # Create the table-like structure for display
        team1_table = "\n".join(team1)
        team2_table = "\n".join(team2)
    
        maps = MAP_POOL

        # Select a random map from the provided options
        selected_map = random.choice(maps)
        selected_map_uppercase = selected_map.upper()

        response = (
            "```\n"
            f"Team A:\n{team1_table}\n"
            "```\n"
            "```\n"
            f"Team B:\n{team2_table}\n"
            "```"
            f'**__MAP: {selected_map_uppercase}__**'
        )

        # Send the formatted teams to the channel
        await message.channel.send(response)


    # Handle the !mixer_bot command for printing USAGE
    elif message.content.startswith('!mixer_bot'):
        usage = (
            "###################"
            "\n**__USAGE:__**\n"
            "`!mix_teams` or `!mix_team` - Mix 10 provided players into two random teams of 5.\n"
            "`!mix_map` or `!mix_maps` - Select a random map from a predefined pool or from a user-provided list.\n"
            "`!mix_pair` or `!mix_pairs` - From 10 provided players create 5 pairs(1st two players, 2nd two players,3rd two players...) and then randomize the teams in such a way that players that are pairs cannot play together.\n"
            "`!mix_all` - Mix 10 provided players into two teams of 5 and select a random map from the predefined map pool.\n\n"
            "PREDEFINED MAP POOL: Dust2 Mirage Inferno Nuke Train Vertigo Ancient Anubis Cache\n\n"
            "examples:\n"
            "!mix_teams Alice Bob Carol Dave Eve Frank Grace Heidi Ivan Judy\n"
            "!mix_all Alice Bob Carol Dave Eve Frank Grace Heidi Ivan Judy\n"
            "!mix_map Dust2 Mirage Inferno Nuke - returns 1 random map from provided list (Dust2 Mirage Inferno Nuke)\n"
            "!mix_map - returns 1 random map from a predefined map pool (Dust2 Mirage Inferno Nuke Train Vertigo Ancient Anubis Cache)\n\n"
        )
        await message.channel.send(usage)


# STEP 3: HANDLING THE STARTUP FOR OUR BOT
# Define the event handler for when the bot is ready
@client.event
async def on_ready() -> None:
    logging.info(f'{client.user} is now running!')

# STEP 4: MAIN ENTRY POINT
async def main() -> None:
    try:
        # Run the client
        await client.start(TOKEN)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        # Exit the program to allow container orchestration to restart it
        sys.exit(1)

if __name__ == '__main__':
    # Start the health check server
    from threading import Thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

    # Run the Discord bot
    asyncio.run(main())
