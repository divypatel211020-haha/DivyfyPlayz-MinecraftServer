import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

MINECRAFT_SERVER_DOMAIN = "divyfyplayz.minecraftr.us"

# ==========================================
# PASTE YOUR TWO CHANNEL IDs HERE:
# ==========================================
COMMAND_CHANNEL_ID = 1531990888039841845  # <- Put your bot commands channel ID here
CHAT_SYNC_CHANNEL_ID = 1531991558042419340 # <- Put your Minecraft chat mirror channel ID here

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} successfully!")
    await bot.change_presence(activity=discord.Game(name="divyfyplayz.minecraftr.us"))

@bot.group(name="mc", invoke_without_command=True)
async def mc(ctx):
    # Restrict main command to the Command Channel
    if ctx.channel.id != COMMAND_CHANNEL_ID:
        return await ctx.send(f"⚠️ Please use bot commands in <#{COMMAND_CHANNEL_ID}>!", delete_after=5)
    
    help_text = """
**🎮 DivyfyPlayz Server Panel Commands:**
`!mc status` - Check if the server is online/offline & view players
`!mc ip` - Display your custom server domain
    """
    await ctx.send(help_text)

@mc.command(name="status")
async def server_status(ctx):
    if ctx.channel.id != COMMAND_CHANNEL_ID:
        return await ctx.send(f"⚠️ Please use bot commands in <#{COMMAND_CHANNEL_ID}>!", delete_after=5)

    url = f"https://api.mcsrvstat.us/2/{MINECRAFT_SERVER_DOMAIN}"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("online"):
            version = data.get("version", "Unknown")
            players_online = data["players"]["online"]
            max_players = data["players"]["max"]
            
            embed = discord.Embed(title="🟢 Server is ONLINE", color=discord.Color.green())
            embed.add_field(name="Domain", value=MINECRAFT_SERVER_DOMAIN, inline=False)
            embed.add_field(name="Version", value=version, inline=True)
            embed.add_field(name="Players", value=f"{players_online}/{max_players}", inline=True)
            
            if players_online > 0 and "list" in data["players"]:
                player_list = ", ".join(data["players"]["list"])
                embed.add_field(name="Online Players", value=player_list, inline=False)
                
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="🔴 Server is OFFLINE", color=discord.Color.red())
            embed.add_field(name="Domain", value=MINECRAFT_SERVER_DOMAIN, inline=False)
            await ctx.send(embed=embed)
            
    except Exception as e:
        await ctx.send(f"❌ Error fetching server status: {e}")

@mc.command(name="ip")
async def server_ip(ctx):
    if ctx.channel.id != COMMAND_CHANNEL_ID:
        return await ctx.send(f"⚠️ Please use bot commands in <#{COMMAND_CHANNEL_ID}>!", delete_after=5)
    await ctx.send(f"🌐 Connect to your cross-play server using: **`{MINECRAFT_SERVER_DOMAIN}`**")

bot.run(TOKEN if TOKEN else "YOUR_BOT_TOKEN_HERE")
