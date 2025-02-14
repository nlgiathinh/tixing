import discord  
from discord.ext import tasks  
import asyncio  
import os  
from flask import Flask  
import threading  
import time  
import platform  

# Flask web server  
app = Flask(__name__)  

@app.route('/')  
def home():  
    return "Bot is running!"  

def run_flask():  
    port = int(os.environ.get('PORT', 10000))  
    app.run(host='0.0.0.0', port=port)  

# Discord bot code  
intents = discord.Intents.default()  
intents.message_content = True  
intents.members = True  
client = discord.Client(intents=intents)  

# Add a cooldown dictionary  
last_reminder = {}  

# Define your specific server ID  
TARGET_SERVER_ID = 1136120835237740547  # Replace with your server ID  
YOUR_USER_ID = 600231556035903518  # Replace with your Discord user ID  
RYUJIN_BOT_ID = 1056379876988440647  # Ryujin bot's ID  

# Only import winotify if running on Windows  
if platform.system() == 'Windows':  
    from winotify import Notification, audio  
    
    def create_notification(title, message, channel_url):  
        toast = Notification(  
            app_id="Discord Bot",  
            title=title,  
            msg=message,  
            duration="short",  
        )  
        
        toast.add_actions(label="Go to Channel", launch=channel_url)  
        toast.set_audio(audio.Mail, loop=False)  
        return toast  
else:  
    def create_notification(title, message, channel_url):  
        pass  

@client.event  
async def on_ready():  
    print(f'Bot is ready as {client.user}')  

@client.event  
async def on_message(message):  
    # Check for mentions in the specific server  
    if message.guild and message.guild.id == TARGET_SERVER_ID:  
        if client.user.id != message.author.id:  # Prevent self-notifications  
            # Check if the specified user is mentioned  
            for mention in message.mentions:  
                if mention.id == YOUR_USER_ID:  
                    channel_url = f"discord://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"  
                    
                    if platform.system() == 'Windows':  
                        notification = create_notification(  
                            f"Mentioned in {message.guild.name}",  
                            f"{message.author.name}: {message.content[:50]}...",  
                            channel_url  
                        )  
                        notification.show()  
                    break  

    # New cooldown reminder code  
    # Check if the message is from Ryujin bot and contains a cooldown embed  
    if message.author.id == RYUJIN_BOT_ID and message.interaction and message.interaction.command.name == "cooldowns":  
        current_time = time.time()  
        
        # Add cooldown check  
        if message.channel.id in last_reminder:  
            if current_time - last_reminder[message.channel.id] < 10:  # 10 seconds cooldown  
                return  

        # Get the user who initiated the cooldown command  
        command_user = message.interaction.user  
        
        await asyncio.sleep(5)  # 15 minutes = 900 seconds  
        await message.channel.send(f"{command_user.mention} 15 minutes have passed since your drop!")  
        last_reminder[message.channel.id] = current_time  

# Run both Flask and Discord bot  
def run_bot():  
    client.run(os.getenv('DISCORD_TOKEN'))  

if __name__ == '__main__':  
    threading.Thread(target=run_flask).start()  
    run_bot()
