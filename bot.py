import discord
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
warning_counts = {}

class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Seraphina is alive!')
    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(('0.0.0.0', port), HealthCheck).serve_forever()

@client.event
async def on_ready():
    print(f'lovely angels! {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == "lovely":
        await message.channel.send("‧˚꒰ lovely angels! ୭ ˚. ᵎᵎ ʚɞ")
    if message.content.lower().startswith("!warning "):
        parts = message.content.split(" ", 1)
        if len(parts) < 2 or not parts[1].strip():
            await message.channel.send("Usage: `!warning {user}`")
            return
        user_mentioned = parts[1].strip()
        key = user_mentioned.lower()
        warning_counts[key] = warning_counts.get(key, 0) + 1
        count = warning_counts[key]
        if count >= 3:
            embed = discord.Embed(title="{Warning_msg}", description=f"˚ ⊹ ࣪ ˖ {user_mentioned} is banned! ₊ ݁ . ⊹ ࣪ ໒꒱", color=0xFFFFFF)
            embed.set_footer(text=f"⚠️ {count}/3 warnings reached — BANNED")
            warning_counts[key] = 0
        else:
            embed = discord.Embed(title="{Warning_msg}", description=f"˚  ⊹  ࣪   ˖  {user_mentioned} is warned! ₊ ݁ . ⊹  ࣪ ໒꒱", color=0xFFFFFF)
            embed.set_footer(text=f"⚠️ {count}/3 warnings")
        await message.channel.send(embed=embed)

threading.Thread(target=run_server, daemon=True).start()
client.run(os.environ.get("DISCORD_BOT_TOKEN"))
