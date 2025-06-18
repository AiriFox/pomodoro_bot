import os
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands
from dataclasses import dataclass

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = 1384735157285687306

intents = discord.Intents.default()
intents.message_content = True 

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="!", intents=intents)
session = Session()


@bot.event
async def on_ready():
    print("Bot is ready!")
    try:
        channel = await bot.fetch_channel(CHANNEL_ID)
        await channel.send("Hello from bot!")
    except Exception as e:
        print(f"Error sending message: {e}")

@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return
    
    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    await ctx.send(f"Session started at {human_readable_time}")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active.")
    
    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    await ctx.send(f"Session ended after {duration} seconds.")

bot.run(BOT_TOKEN)