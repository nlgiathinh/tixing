import discord  
from discord.ext import tasks  
import asyncio  
import os  
from flask import Flask  
import threading  

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

@client.event  
async def on_ready():  
    print(f'Bot is ready as {client.user}')  

@client.event  
async def on_message(message):  
    if "frostdrop_'s drop" in message.content.lower():  
        await asyncio.sleep(15 * 60)  
        for member in message.guild.members:  
            if member.name == "frostdrop_":  
                await message.channel.send(f"{member.mention} 15 minutes have passed since your drop!")  
                break  

# Run both Flask and Discord bot  
def run_bot():  
    client.run(os.getenv('DISCORD_TOKEN'))  

if __name__ == '__main__':  
    threading.Thread(target=run_flask).start()  
    run_bot()
