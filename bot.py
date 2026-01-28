import discord
from discord.ext import commands
import os

# ==========================
# 🔑 TOKEN (Railway Variables)
# ==========================
TOKEN = os.getenv("TOKEN")

# ==========================
# 🌾 ID ROLE NÔNG DÂN
# ==========================
ROLE_NONG_DAN_ID = 1465291719087100059  # <-- ĐỔI ROLE ID CỦA BẠN

# ==========================
# INTENTS
# ==========================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================
# 🌱 NÔNG SẢN + EMOJI
# ==========================
NONG_SAN = {
    "bí ngô": ("Bí Ngô", "<:bi_ngo:1465929149561704521>"),
    "nho": ("Nho", "<:nho:1465929423147761859>"),
    "dưa hấu": ("Dưa Hấu", "<:dua_hau:1465929236660490436>"),
    "dừa": ("Dừa", "<:dua:1465929313051349035>"),
    "xoài": ("Xoài", "<:xoai:1465929367031910514>"),
    "trái cổ đại": ("Trái Cổ Đại", "<:trai_co_dai:1465929696498684181>"),
    "đậu thần": ("Đậu Thần", "<:dau_than:1465929579775656069>"),
    "khế": ("Khế", "<:khe:1465929502533095475>"),
    "táo đường": ("Táo Đường", "<:tao_duong:1465929638365761571>")
}

# ==========================
# 🌦 THỜI TIẾT + EMOJI
# ==========================
THOI_TIET = {
    "bão tuyết": ("Bão Tuyết", "<:bao_tuyet:1465929805064306922>"),
    "tuyết": ("Tuyết", "<:tuyet:1465930053039689810>"),
    "mưa": ("Mưa", "<:mua:1465930166654996490>"),
    "mưa bão": ("Mưa Bão", "<:mua_bao:1465930483555635210>"),
    "sương mù": ("Sương Mù", "<:suong_mu:1465930208195510415>"),
    "sương sớm": ("Sương Sớm", "<:suong_som:1465930409648066581>"),
    "ánh trăng": ("Ánh Trăng", "<:anh_trang:1465930353968677004>"),
    "cực quang": ("Cực Quang", "<:cuc_quang:1465929983074762948>"),
    "nắng nóng": ("Nắng Nóng", "<:nang_nong:1465929883216777227>"),
    "gió": ("Gió", "<:gio:1465930114390032384>"),
    "gió cát": ("Gió Cát", "<:gio_cat:1465930264340599080>")
}

# ==========================
# 🔧 DỤNG CỤ + EMOJI
# ==========================
DUNG_CU = {
    "vòi xanh": ("Vòi Xanh", "<:voi_xanh:1465937030994202699>"),
    "vòi đỏ": ("Vòi Đỏ", "<:voi_do:1465938120175517777>")
}

# ==========================
# 📌 HÀM GỬI THÔNG BÁO
# ==========================
async def gui_thong_bao(message, loai, ten, emoji):
    role = message.guild.get_role(ROLE_NONG_DAN_ID)

    embed = discord.Embed(
        title=f"📢 THÔNG BÁO {loai}",
        description=f"{emoji} **{ten}** đã xuất hiện!",
        color=0x00ff99
    )

    await message.channel.send(
        content=f"{role.mention}" if role else "",
        embed=embed
    )

# ==========================
# ✅ BOT ONLINE
# ==========================
@bot.event
async def on_ready():
    print(f"✅ Bot đã online: {bot.user}")

# ==========================
# ✅ AUTO NHẬN TIN NHẮN
# ==========================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    text = message.content.lower().strip()

    # 🌱 Nông sản
    if text in NONG_SAN:
        ten, emoji = NONG_SAN[text]
        await gui_thong_bao(message, "NÔNG SẢN", ten, emoji)

    # 🌦 Thời tiết
    elif text in THOI_TIET:
        ten, emoji = THOI_TIET[text]
        await gui_thong_bao(message, "THỜI TIẾT", ten, emoji)

    # 🔧 Dụng cụ
    elif text in DUNG_CU:
        ten, emoji = DUNG_CU[text]
        await gui_thong_bao(message, "DỤNG CỤ", ten, emoji)

    await bot.process_commands(message)

# ==========================
# 🚀 CHẠY BOT
# ==========================
bot.run(TOKEN)
