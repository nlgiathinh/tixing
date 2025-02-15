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

# Define your specific server ID and user ID  
TARGET_SERVER_ID = 1136120835237740547  
TARGET_USER_ID = 600231556035903518  
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
        # Check if message is from Ryujin AND mentions the target user ID  
        if message.author.name == "Ryujin" and str(TARGET_USER_ID) in message.content:  
            print(f"Trigger detected: Ryujin mentioned user with ID {TARGET_USER_ID}")  
            current_time = time.time()  
            
            # Add cooldown check  
            if message.channel.id in last_reminder:  
                if current_time - last_reminder[message.channel.id] < 30:  
                    print("Cooldown still active, skipping reminder")  
                    return  
            
            try:  
                # Find frostdrop_'s member object  
                target_member = message.guild.get_member(TARGET_USER_ID)  

                await asyncio.sleep(900)  # 15 minutes delay  
                if target_member:  
                    await message.channel.send(f"{target_member.mention} Cooldown timer!")  
                else:  
                    await message.channel.send(f"<@{TARGET_USER_ID}> Cooldown timer!")  
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
