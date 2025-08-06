import discord
from discord import app_commands
from discord.ext import commands
import dotenv
dotenv.load_dotenv()
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

SERVER_ID = 1293985828271427675 # PUT YOUR SERVER ID HERE
server = discord.Object(id=SERVER_ID)

def make_time_us(time):
    print(f"Time at start func maketimeus: {time}")
    hour, minute = map(int, time.split(":"))
    end = "AM"

    if hour == 0:
        hour = 12
    elif hour == 12:
        end = "PM"
    elif hour > 12:
        hour -= 12
        end = "PM" 
    
    print(f"Time after: {hour}:{minute:02d} {end}")
    return f"{hour}:{minute:02d} {end}"

def make_time_eu(time):
    print(f"Time at start func maketimemil: {time}")
    time_part, end = time.strip().split()  
    hour, minute = map(int, time_part.split(":"))       

    if end == "AM":
        if hour == 12:
            hour = 0
    elif end == "PM":
        if hour != 12:
            hour += 12

    print(f"Time: {hour:02d}:{minute:02d}")
    return f"{hour:02d}:{minute:02d}"

async def setup_commands():
    @bot.tree.command(name="ping", description="Check if the bot is alive")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")
    

@bot.tree.command(name="americify", description="Convert 24h time to 12h US format")
@app_commands.describe(time="Time in 24h format (e.g., 14:30)")
async def americify(interaction: discord.Interaction, time: str):
    result = make_time_us(time)
    await interaction.response.send_message(result)

@bot.tree.command(name="europeify", description="Convert 12h time to 24h format")
@app_commands.describe(time="Time in 12h format (e.g., 2:30 PM)")
async def europeify(interaction: discord.Interaction, time: str):
    result = make_time_eu(time)
    await interaction.response.send_message(result)

@bot.event
async def on_ready():
    await setup_commands()
    synced = await bot.tree.sync(guild=server)
    print(f"Synced {len(synced)} commands to guild {SERVER_ID}")
    print(f"Logged in as {bot.user}")


bot.run(os.getenv("BOT_TOKEN"))
