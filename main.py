import discord  
import asyncio  
import os  
from dotenv import load_dotenv  
import time  

# Load environment variables  
load_dotenv()  

# Discord bot code  
intents = discord.Intents.default()  
intents.message_content = True  
intents.members = True  
client = discord.Client(intents=intents)  

# Add a cooldown dictionary  
last_reminder = {}  

# Define your specific server ID  
TARGET_SERVER_ID = 1136120835237740547  
TARGET_USER = "frostdrop_"  

@client.event  
async def on_ready():  
    print(f'Bot is ready as {client.user}')  
    print(f'Connected to server: {[guild.name for guild in client.guilds]}')  
    print('------')  
    print('Waiting for messages...')  

@client.event  
async def on_message(message):  
    if message.guild and message.guild.id == TARGET_SERVER_ID:  
        # Check if message is from Ryujin AND mentions frostdrop_  
        if message.author.name == "Ryujin" and TARGET_USER in message.content:  
            print(f"Trigger detected: Ryujin mentioned {TARGET_USER}")  
            current_time = time.time()  
            
            # Add cooldown check  
            if message.channel.id in last_reminder:  
                if current_time - last_reminder[message.channel.id] < 30:  
                    print("Cooldown still active, skipping reminder")  
                    return  
            
            try:  
                await asyncio.sleep(900)  # 5 second delay  
                await message.channel.send(f"{message.author.mention} Cooldown timer!")  
                print("Reminder sent!")  
                last_reminder[message.channel.id] = current_time  
            except Exception as e:  
                print(f"Error sending reminder: {e}")  

# Run the bot  
if __name__ == "__main__":  
    token = os.getenv('DISCORD_TOKEN')  
    if not token:  
        print("Error: No token found! Make sure you have a .env file with DISCORD_TOKEN=your_token_here")  
    else:  
        print("Starting bot...")  
        client.run(token)