import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# 👉 DÁN ID ROLE NÔNG DÂN VÀO ĐÂY
ROLE_NONG_DAN_ID = 1465291719087100059  # <-- đổi số này

nong_san = {
    "bí ngô": "🎃",
    "dưa hấu": "🍉",
    "dừa": "🥥",
    "xoài": "🥭",
    "trái cổ đại": "🗿",
    "đậu thần": "🌱",
    "khế": "⭐",
    "táo đường": "🍎"
}

thoi_tiet = {
    "bão tuyết": "🌨️",
    "tuyết": "❄️",
    "mưa": "🌧️",
    "bão": "🌪️",
    "sương mù": "🌫️",
    "sương sớm": "🌁",
    "ánh trăng": "🌙",
    "cực quang": "🌌",
    "gió": "💨",
    "gió cát": "🏜️",
    "nắng nóng": "☀️"
}

@client.event
async def on_ready():
    print(f"✅ Bot đã online: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content.lower()

    role = message.guild.get_role(ROLE_NONG_DAN_ID)
    tag_role = role.mention if role else ""

    for ten, emoji in nong_san.items():
        if ten in text:
            await message.channel.send(
                f"{tag_role}\n{emoji} **NÔNG SẢN XUẤT HIỆN: {ten.upper()}**"
            )
            return

    for ten, emoji in thoi_tiet.items():
        if ten in text:
            await message.channel.send(
                f"{tag_role}\n{emoji} **THỜI TIẾT: {ten.upper()}**"
            )
            return


TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
