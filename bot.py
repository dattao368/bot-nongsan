import discord
import os
import time
import threading
from flask import Flask

# ===== CHỐNG SLEEP RENDER =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive"

def run_web():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_web).start()
# ==============================

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

ROLE_NONG_DAN_ID = 1465291719087100059  # đổi nếu cần

last_send = 0  # chống spam

nong_san = {
    "bí ngô": "🎃",
    "bí": "🎃",
    "dưa hấu": "🍉",
    "dưa": "🍉",
    "dừa": "🥥",
    "xoài": "🥭",
    "trái cổ đại": "🗿",
    "đậu thần": "🌱",
    "đậu": "🌱",
    "khế": "⭐",
    "táo đường": "🍎"
}

thoi_tiet = {
    "bão tuyết": "🌨️",
    "tuyết": "❄️",
    "mưa": "🌧️",
    "bão": "⛈️",
    "sương mù": "🌫️",
    "sương sớm": "🌁",
    "ánh trăng": "🌙",
    "cực quang": "🌌",
    "gió": "💨",
    "gió cát": "🏜️",
    "nắng nóng": "☀️"
}

dung_cu = {
    "vòi đỏ": "🚿"
}

@client.event
async def on_ready():
    print(f"✅ Bot đã online: {client.user}")

@client.event
async def on_message(message):
    global last_send

    if message.author.bot:
        return

    if message.guild is None:
        return

    guild_id = str(message.guild.id)

    if guild_id not in config:
        return

    if message.channel.id != config[guild_id]["channel_id"]:
        return


    if time.time() - last_send < 5:
        return

    text = message.content.lower()

    role = message.guild.get_role(ROLE_NONG_DAN_ID)
    tag_role = role.mention if role else ""

    for ten, emoji in nong_san.items():
        if ten in text:
            await message.channel.send(
                f"{tag_role}\n{emoji} **NÔNG SẢN ĐANG BÁN: {ten.upper()}**"
            )
            last_send = time.time()
            return

    for ten, emoji in thoi_tiet.items():
        if ten in text:
            await message.channel.send(
                f"{tag_role}\n{emoji} **THỜI TIẾT XUẤT HIỆN: {ten.upper()}**"
            )
            last_send = time.time()
            return

    for ten, emoji in dung_cu.items():
        if ten in text:
            await message.channel.send(
                f"{tag_role}\n{emoji} **DỤNG CỤ ĐANG BÁN: {ten.upper()}**"
            )
            last_send = time.time()
            return

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
