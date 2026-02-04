import discord
from discord.ext import commands, tasks
import os, time, json
import datetime
from datetime import timedelta
import difflib

# ==========================
# 🔑 TOKEN
# ==========================
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    print("❌ Bạn chưa thêm TOKEN vào Variables!")
    exit()

# ==========================
# 📌 ID KÊNH (SỬA LẠI ĐÚNG SERVER)
# ==========================
CHANNEL_PHU_ID = 1465291905368854570
CHANNEL_CHINH_ID = 1466801337361764506

CHANNEL_TOP_NONG_SAN = 1468562267267141877
CHANNEL_TOP_CONG_CU = 1468562389443280927
CHANNEL_TOP_THOI_TIET = 1468562439930118367

# ==========================
# 🌾 ROLE PING TOP
# ==========================
ROLE_PING_TOP = 1465291719087100059

# ==========================
# 🎖️ ROLE THƯỞNG STREAK
# ==========================
ROLE_CHAM_CHI_ID = 1468564029508292618   # 1 ngày
ROLE_CHUYEN_CAN_ID = 1468564132608344076 # 3 ngày
ROLE_UU_TU_ID = 1468564197309808661     # 7 ngày

# ==========================
# 🖼️ BANNER EMBED
# ==========================
BANNER_URL = "https://i.imgur.com/6QZ7W9N.png"

# ==========================
# 🌾 NÔNG SẢN (PLACEHOLDER EMOJI)
# ==========================
NONG_SAN = {
    "bí ngô": ("Bí Ngô", "<:bi_ngo:1468559344676110529>"),
    "dưa hấu": ("Dưa Hấu", "<:dua_hau:1468559217316331624>"),
    "dừa": ("Dừa", "<:dua:1468559538159357972>"),
    "xoài": ("Xoài", "<:xoai:1468559607247933513>"),
    "đậu thần": ("Đậu Thần", "<:dau_than:1468559814236962972>"),
    "khế": ("Khế", "<:khe:1468559895602397343>"),
    "táo đường": ("Táo Đường", "<:tao_duong:1468559984693612656>"),
    "trái cổ đại": ("Trái Cổ Đại", "<:trai_co_dai:1468559690278502462>")
}

# ==========================
# 🛠️ CÔNG CỤ (PLACEHOLDER)
# ==========================
CONG_CU = {
    "vòi đỏ": ("Vòi Đỏ", "<:voi_do:1468565773592301619>"),
    "vòi xanh": ("Vòi Xanh", "<:voi_xanh:1468565853074362440>")
}

# ==========================
# 🌦️ THỜI TIẾT + BIẾN THỂ
# ==========================
THOI_TIET = {
    "bão tuyết": ("Bão Tuyết", "<:bao_tuyet:1468560083465015443>", "Băng"),
    "tuyết": ("Tuyết", "<:tuyet:1468560669879308322>", "Khí Lạnh"),
    "mưa rào": ("Mưa Rào", "<:mua_rao:1468560753060741140>", "Ẩm Ướt"),
    "mưa bão": ("Mưa Bão", "<:mua_bao:1468560932325294205>", "Nhiễm Điện"),
    "sương mù": ("Sương Mù", "<:suong_mu:1468561014844035237>", "Ẩm Ướt"),
    "sương sớm": ("Sương Sớm", "<:suong_som:1468561105428152543>", "Sương"),
    "gió": ("Gió", "<:gio:1468561516872732703>", "Gió"),
    "gió cát": ("Gió Cát", "<:gio_cat:1468561637593190632>", "Cát"),
    "cực quang": ("Cực Quang", "<:cuc_quang:1468561214786371696>", "Cực Quang"),
    "ánh trăng": ("Ánh Trăng", "<:anh_trang:1468561408416546853>", "Ánh Trăng"),
    "nắng nóng": ("Nắng Nóng", "<:nang_nong:1468561712411316356>", "Khô")
}

ALL_KEYWORDS = {**NONG_SAN, **CONG_CU, **THOI_TIET}

# ==========================
# ⏳ RESET TIME
# ==========================
RESET_TIME = {
    "nong_san": 300,     # 5 phút
    "cong_cu": 1800,     # 30 phút
    "thoi_tiet": 300     # 5 phút
}

da_bao = {"nong_san": {}, "cong_cu": {}, "thoi_tiet": {}}

# ==========================
# 🏆 JSON DATA
# ==========================
DATA_FILE = "thuong.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

thuong_data = load_data()

# ==========================
# 🤖 BOT SETUP
# ==========================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================
# 🎖️ THƯỞNG ROLE STREAK
# ==========================
async def cap_nhat_role(member, streak):
    guild = member.guild

    role1 = guild.get_role(ROLE_CHAM_CHI_ID)
    role3 = guild.get_role(ROLE_CHUYEN_CAN_ID)
    role7 = guild.get_role(ROLE_UU_TU_ID)

    await member.remove_roles(role1, role3, role7)

    if streak >= 7:
        await member.add_roles(role7)
    elif streak >= 3:
        await member.add_roles(role3)
    else:
        await member.add_roles(role1)

# ==========================
# 📢 EMBED THÔNG BÁO
# ==========================
async def gui_embed(channel, desc):
    embed = discord.Embed(title="📢 THÔNG BÁO", description=desc, color=0x00ff99)
    embed.set_image(url=BANNER_URL)
    await channel.send(embed=embed)

# ==========================
# 📌 XỬ LÝ BÁO
# ==========================
async def xu_ly_bao(message, loai, ten, emoji, bien_the=None):
    now = time.time()

    # chống trùng
    if ten in da_bao[loai]:
        if now - da_bao[loai][ten] < RESET_TIME[loai]:
            await message.reply("❌ Đã có người báo rồi!")
            return

    da_bao[loai][ten] = now

    channel = bot.get_channel(CHANNEL_CHINH_ID)

    if loai == "nong_san":
        desc = f"{emoji} **{ten} đang bán ở shop Yeongman**\n⏳ Reset: 5 phút"

    elif loai == "cong_cu":
        desc = f"{emoji} **{ten} đang bán ở shop Lena**\n⏳ Reset: 30 phút"

    else:
        desc = f"{emoji} **{ten} xuất hiện**\n✨ Xuất hiện biến thể: [{bien_the}]"

    await gui_embed(channel, desc)

# ==========================
# 👤 LỆNH !me
# ==========================
@bot.command()
async def me(ctx):
    uid = str(ctx.author.id)

    if uid not in thuong_data:
        await ctx.send("❌ Bạn chưa có dữ liệu!")
        return

    info = thuong_data[uid]

    embed = discord.Embed(title="👤 Thống kê cá nhân", color=0xffcc00)
    embed.add_field(name="🔥 Streak", value=f"{info['streak']} ngày", inline=False)

    await ctx.send(embed=embed)

# ==========================
# 📩 ON MESSAGE
# ==========================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CHANNEL_PHU_ID:
        return

    text = message.content.lower().strip()

    if text in NONG_SAN:
        ten, emoji = NONG_SAN[text]
        await xu_ly_bao(message, "nong_san", ten, emoji)

    elif text in CONG_CU:
        ten, emoji = CONG_CU[text]
        await xu_ly_bao(message, "cong_cu", ten, emoji)

    elif text in THOI_TIET:
        ten, emoji, bien_the = THOI_TIET[text]
        await xu_ly_bao(message, "thoi_tiet", ten, emoji, bien_the)

    else:
        sug = difflib.get_close_matches(text, ALL_KEYWORDS.keys(), n=1)
        if sug:
            await message.reply(f"❌ Sai từ khóa. Bạn muốn `{sug[0]}`?")
        else:
            await message.reply("❌ Không hợp lệ!")

    await bot.process_commands(message)

# ==========================
# ✅ READY
# ==========================
@bot.event
async def on_ready():
    print("✅ Bot Online!")

bot.run(TOKEN)
