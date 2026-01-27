import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# DANH SÁCH NÔNG SẢN
NONG_SAN = {
    "bí ngô": "🎃 Bí Ngô",
    "dưa hấu": "🍉 Dưa Hấu",
    "dừa": "🥥 Dừa",
    "xoài": "🥭 Xoài",
    "trái cổ đại": "🗿 Trái Cổ Đại",
    "đậu thần": "🫘 Đậu Thần",
    "khế": "⭐ Khế",
    "táo đường": "🍎 Táo Đường"
}

# DANH SÁCH THỜI TIẾT
THOI_TIET = {
    "bão tuyết": "❄️ Bão Tuyết",
    "tuyết": "🌨️ Tuyết",
    "mưa": "🌧️ Mưa",
    "bão": "🌪️ Bão",
    "sương mù": "🌫️ Sương Mù",
    "sương sớm": "🌁 Sương Sớm",
    "ánh trăng": "🌙 Ánh Trăng",
    "cực quang": "🌌 Cực Quang",
    "gió": "💨 Gió",
    "gió cát": "🏜️ Gió Cát",
    "nắng nóng": "☀️ Nắng Nóng"
}

@client.event
async def on_ready():
    print(f"✅ Bot online: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content.lower().strip()

    # KIỂM TRA NÔNG SẢN
    for key in NONG_SAN:
        if key in text:
            await message.channel.send(f"🌾 **Phát hiện nông sản:** {NONG_SAN[key]}")
            return

    # KIỂM TRA THỜI TIẾT
    for key in THOI_TIET:
        if key in text:
            await message.channel.send(f"🌦️ **Phát hiện thời tiết:** {THOI_TIET[key]}")
            return

# LẤY TOKEN TỪ RENDER
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    print("❌ CHƯA CÓ DISCORD_TOKEN TRÊN RENDER")
else:
    client.run(TOKEN)
