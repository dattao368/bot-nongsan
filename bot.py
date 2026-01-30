import discord
from discord.ext import commands
import os
import difflib
import time

# ==========================
# 🔑 TOKEN
# ==========================
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    print("❌ LỖI: Bạn chưa thêm TOKEN vào Variables!")
    exit()

# ==========================
# 📡 ID KÊNH
# ==========================
CHANNEL_PHU_ID = 1465291905368854570      # Kênh phụ: người dùng gửi
CHANNEL_CHINH_ID = 1466801337361764506    # Kênh chính: bot gửi thông báo

# ==========================
# 🌾 ROLE ID NÔNG DÂN
# ==========================
ROLE_NONG_DAN_ID = 1465291719087100059

# ==========================
# INTENTS
# ==========================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================
# 🌱 TỪ KHÓA
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

DUNG_CU = {
    "vòi xanh": ("Vòi Xanh", "<:voi_xanh:1465937030994202699>"),
    "vòi đỏ": ("Vòi Đỏ", "<:voi_do:1465938120175517777>")
}

ALL_KEYWORDS = {**NONG_SAN, **THOI_TIET, **DUNG_CU}

# ==========================
# 🕒 COOLDOWN 7 GIÂY
# ==========================
cooldown = {}
COOLDOWN_TIME = 7

# ==========================
# 📌 GỬI THÔNG BÁO
# ==========================
async def gui_thong_bao(message, loai, ten, emoji):
    channel = bot.get_channel(CHANNEL_CHINH_ID)
    role = message.guild.get_role(ROLE_NONG_DAN_ID)

    embed = discord.Embed(
        title=f"📢 THÔNG BÁO {loai}",
        description=f"{emoji} **{ten}** đã xuất hiện!",
        color=0x00ff99
    )

    await channel.send(content=f"{role.mention}", embed=embed)

    # Ghi log
    with open("log_bao.txt", "a", encoding="utf-8") as f:
        f.write(f"{message.author} báo {loai} | {ten}\n")

# ==========================
# 🤖 BOT ONLINE
# ==========================
@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user}")

# ==========================
# 📩 XỬ LÝ TIN NHẮN
# ==========================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # ❗ Chỉ đọc tin nhắn từ kênh phụ
    if message.channel.id != CHANNEL_PHU_ID:
        return

    user_id = message.author.id
    now = time.time()

    # COOLDOWN
    if user_id in cooldown and now - cooldown[user_id] < COOLDOWN_TIME:
        return

    cooldown[user_id] = now

    text = message.content.lower().strip()

    # TỪ KHÓA HỢP LỆ
    if text in NONG_SAN:
        ten, emoji = NONG_SAN[text]
        await gui_thong_bao(message, "NÔNG SẢN", ten, emoji)

    elif text in THOI_TIET:
        ten, emoji = THOI_TIET[text]
        await gui_thong_bao(message, "THỜI TIẾT", ten, emoji)

    elif text in DUNG_CU:
        ten, emoji = DUNG_CU[text]
        await gui_thong_bao(message, "DỤNG CỤ", ten, emoji)

    else:
        # Gợi ý từ gần giống
        suggestion = difflib.get_close_matches(text, ALL_KEYWORDS.keys(), n=1, cutoff=0.6)

        if suggestion:
            await message.reply(f"❌ **Không có từ khóa** `{text}`.\n👉 Bạn có muốn nhập: **`{suggestion[0]}`** không?")
        else:
            await message.reply("❌ Từ khóa không hợp lệ! Hãy kiểm tra lại.")

    await bot.process_commands(message)

# ==========================
# 🚀 CHẠY BOT
# ==========================
bot.run(TOKEN)
