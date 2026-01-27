import discord
import os
import time
import json
import threading
from flask import Flask

# ================== CHỐNG SLEEP RENDER ==================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive"

def run_web():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_web).start()
# ========================================================

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

ROLE_NONG_DAN_ID = 1465291719087100059
CONFIG_FILE = "config.json"
COOLDOWN = 5  # giây

last_send = 0

# ================== LOAD / SAVE CONFIG ==================
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

config = load_config()
# ========================================================

# ================== DỮ LIỆU ==================
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
# ========================================================

@client.event
async def on_ready():
    print(f"✅ Bot đã online: {client.user}")

@client.event
async def on_message(message):
    global last_send

    if message.author.bot or message.guild is None:
        return

    guild_id = str(message.guild.id)
    text = message.content.lower().strip()

    # ===== LỆNH SET CHANNEL =====
    if text == "!setchannel":
        if not message.author.guild_permissions.administrator:
            await message.channel.send("❌ Chỉ admin mới dùng được lệnh này.")
            return

        config[guild_id] = {
            "channel_id": message.channel.id
        }
        save_config(config)

        await message.channel.send("✅ Đã đặt kênh này làm **kênh báo nông sản**.")
        return

    # ===== CHƯA SET CHANNEL =====
    if guild_id not in config:
        return

    # ===== KHÁC CHANNEL =====
    if message.channel.id != config[guild_id]["channel_id"]:
        return

    # ===== CHỐNG SPAM =====
    if time.time() - last_send < COOLDOWN:
        return

    ket_qua = []

    for ten, emoji in nong_san.items():
        if ten in text:
            ket_qua.append(f"{emoji} **Nông sản:** {ten.title()}")
            break

    for ten, emoji in thoi_tiet.items():
        if ten in text:
            ket_qua.append(f"{emoji} **Thời tiết:** {ten.title()}")
            break

    for ten, emoji in dung_cu.items():
        if ten in text:
            ket_qua.append(f"{emoji} **Dụng cụ:** {ten.title()}")
            break

    if not ket_qua:
        return

    role = message.guild.get_role(ROLE_NONG_DAN_ID)
    tag_role = role.mention if role else ""

    await message.channel.send(
        f"{tag_role}\n"
        f"📢 **THÔNG BÁO PLAY TOGETHER**\n"
        + "\n".join(ket_qua)
    )

    last_send = time.time()

TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
