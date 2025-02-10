import discord  
from discord.ext import tasks  
import asyncio  
import os  

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

client.run(os.getenv('DISCORD_TOKEN'))