import discord
from discord.ext import commands, tasks
import os, time, json
import datetime
import difflib

# ==========================
# 🔑 TOKEN
# ==========================
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    print("❌ Bạn chưa thêm TOKEN vào Variables!")
    exit()

# ==========================
# 📌 ID KÊNH
# ==========================
CHANNEL_PHU_ID = 1465291905368854570
CHANNEL_CHINH_ID = 1466801337361764506

CHANNEL_TOP_NONG_SAN = 1468562267267141877
CHANNEL_TOP_CONG_CU = 1468562389443280927
CHANNEL_TOP_THOI_TIET = 1468562439930118367

# ==========================
# 🌾 ROLE PING THÔNG BÁO
# ==========================
ROLE_NONG_DAN_ID = 1465291719087100059

# ==========================
# 🖼️ 2 BANNER RIÊNG
# ==========================

# Banner khi bot báo ở kênh chính
BANNER_THONG_BAO = "https://cdn.discordapp.com/attachments/1443938299646312690/1468611704110841988/ChatGPT_Image_21_12_55_4_thg_2_2026.png?ex=6984a6bb&is=6983553b&hm=79c78ff2d2b94d0a807c56dd90d60c829da4cf568d88e0c9a2bb38e5f685f049&"

# Banner khi bot đăng TOP tuần
BANNER_TOP_TUAN = "https://cdn.discordapp.com/attachments/1443938299646312690/1468617424797434099/ChatGPT_Image_21_37_31_4_thg_2_2026.png?ex=6984ac0f&is=69835a8f&hm=9760b6a60d140db6403df21ab1726650fd9e59895a35797d1755a9d079fec596&"

# ==========================
# 🌾 NÔNG SẢN
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
# 🛠️ CÔNG CỤ
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
# ⏳ RESET TIME CHỐNG SPAM
# ==========================
RESET_TIME = {
    "nong_san": 300,
    "cong_cu": 1800,
    "thoi_tiet": 300
}

da_bao = {"nong_san": {}, "cong_cu": {}, "thoi_tiet": {}}

# ==========================
# 🏆 FILE TOP TUẦN
# ==========================
TOP_FILE = "top_week.json"

def load_top():
    try:
        with open(TOP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"nong_san": {}, "cong_cu": {}, "thoi_tiet": {}}

def save_top(data):
    with open(TOP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

top_data = load_top()

# ==========================
# ✅ LINK EMOJI THUMBNAIL
# ==========================
def get_emoji_url(emoji_text):
    if emoji_text.startswith("<:"):
        emoji_id = emoji_text.split(":")[2].replace(">", "")
        return f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
    return None

# ==========================
# 🤖 BOT SETUP
# ==========================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================
# 📌 XỬ LÝ BÁO
# ==========================
async def xu_ly_bao(message, loai, ten, emoji, bien_the=None):
    now = time.time()

    # chống spam trùng
    if ten in da_bao[loai]:
        if now - da_bao[loai][ten] < RESET_TIME[loai]:
            await message.reply("❌ Đã có người báo rồi!")
            return

    da_bao[loai][ten] = now

    # cộng TOP tuần
    uid = str(message.author.id)
    if uid not in top_data[loai]:
        top_data[loai][uid] = {"count": 0}
    top_data[loai][uid]["count"] += 1
    save_top(top_data)

    channel = bot.get_channel(CHANNEL_CHINH_ID)

    # ✅ Ping 1 dòng duy nhất
    ping_text = f"<@&{ROLE_NONG_DAN_ID}> | {ten}"

    # ======================
    # FORMAT ĐÚNG NPC
    # ======================
    if loai == "nong_san":
        title = "📢 THÔNG BÁO NÔNG SẢN"
        desc = (
            f"{emoji} **{ten}**\n"
            f"🛒 đang bán ở NPC: **[ Yeongman ]**\n"
            f"⏳ Làm mới sau: **5 phút**"
        )

    elif loai == "cong_cu":
        title = "📢 THÔNG BÁO CÔNG CỤ"
        desc = (
            f"{emoji} **{ten}**\n"
            f"🛠️ đang bán ở NPC: **[ Lena ]**\n"
            f"⏳ Làm mới sau: **30 phút**"
        )

    else:
        title = "📢 THÔNG BÁO THỜI TIẾT"
        desc = (
            f"{emoji} **{ten}**\n"
            f"xuất hiện biến thể: **[ {bien_the} ]**"
        )

    # ======================
    # EMBED THÔNG BÁO
    # ======================
    embed = discord.Embed(title=title, description=desc, color=0x00ff99)

    # thumbnail emoji
    url = get_emoji_url(emoji)
    if url:
        embed.set_thumbnail(url=url)

    # banner thông báo riêng
    embed.set_image(url=BANNER_THONG_BAO)

    # ✅ gửi 1 tin nhắn duy nhất
    await channel.send(content=ping_text, embed=embed)

# ==========================
# 🏆 AUTO TOP TUẦN (THỨ 2 00:00)
# ==========================
@tasks.loop(minutes=1)
async def auto_top_week():
    now = datetime.datetime.now()

    if now.weekday() == 0 and now.hour == 0 and now.minute == 0:

        async def send_top(loai, channel_id, title):
            channel = bot.get_channel(channel_id)
            if channel is None:
                return

            data = top_data.get(loai, {})
            if not data:
                await channel.send("❌ Tuần này chưa ai báo!")
                return

            top_list = sorted(
                data.items(),
                key=lambda x: x[1]["count"],
                reverse=True
            )[:5]

            medals = ["🥇", "🥈", "🥉", "🏅", "🏅"]
            text = ""

            for i, (uid, info) in enumerate(top_list):
                text += f"{medals[i]} **<@{uid}>** đã báo: **{info['count']}**\n"

            # embed TOP tuần
            embed = discord.Embed(
                title=f"🏆 {title} TUẦN",
                description=text,
                color=0xffcc00
            )

            # banner top tuần riêng
            embed.set_image(url=BANNER_TOP_TUAN)

            await channel.send(embed=embed)

            # reset tuần mới
            top_data[loai].clear()
            save_top(top_data)

        await send_top("nong_san", CHANNEL_TOP_NONG_SAN, "TOP TUẦN NÔNG SẢN")
        await send_top("cong_cu", CHANNEL_TOP_CONG_CU, "TOP TUẦN CÔNG CỤ")
        await send_top("thoi_tiet", CHANNEL_TOP_THOI_TIET, "TOP TUẦN THỜI TIẾT")

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
    auto_top_week.start()

bot.run(TOKEN)
