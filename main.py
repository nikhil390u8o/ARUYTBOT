import os
import time
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineKeyboardMarkup,
    InlineKeyboardButton, CallbackQuery
)

# ── ᴄᴏɴꜰɪɢ ───────────────────────────────────────────────────────
API_ID     = int(os.environ.get("API_ID", "20898349"))
API_HASH   = os.environ.get("API_HASH", "9fdb830d1e435b785f536247f49e7d87")
BOT_TOKEN  = os.environ.get("BOT_TOKEN", "8628709880:AAHw1FOZ2-7KS7S2v0jxlip1m4yB0jG-Whc")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@sxypndu")
MASTER_KEY = os.environ.get("MASTER_KEY", "YukiMasterAdmin2026")
API_BASE   = os.environ.get("API_BASE", "https://web-production-6415.up.railway.app")

# ── ɪᴍᴀɢᴇs ───────────────────────────────────────────────────────
IMG_START  = os.environ.get("IMG_START",  "https://files.catbox.moe/bd3cqo.jpg")
IMG_KEY    = os.environ.get("IMG_KEY",    "https://files.catbox.moe/bd3cqo.jpg")
IMG_USAGE  = os.environ.get("IMG_USAGE",  "https://files.catbox.moe/bd3cqo.jpg")
IMG_PING   = os.environ.get("IMG_PING",   "https://files.catbox.moe/bd3cqo.jpg")

bot = Client("ARUAPIBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# ── ʜᴇʟᴘᴇʀs ──────────────────────────────────────────────────────

async def check_joined(client, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(CHANNEL_ID, user_id)
        return member.status.name not in ["LEFT", "BANNED", "RESTRICTED"]
    except:
        return False

async def api_get(endpoint: str, params: dict) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_BASE}{endpoint}",
                params=params,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                return await resp.json()
    except Exception as e:
        return {"error": str(e)}

def join_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}"),
        InlineKeyboardButton("✅ ɪ ᴊᴏɪɴᴇᴅ", callback_data="check_join")
    ]])

def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔑 ᴍʏ ᴀᴘɪ ᴋᴇʏ", callback_data="my_key"),
            InlineKeyboardButton("📈 ᴍʏ ᴜsᴀɢᴇ", callback_data="my_usage"),
        ],
        [
            InlineKeyboardButton("🗑 ᴅᴇʟᴇᴛᴇ ᴋᴇʏ", callback_data="del_key"),
            InlineKeyboardButton("🏓 ᴘɪɴɢ ᴀᴘɪ", callback_data="ping"),
        ],
        [
            InlineKeyboardButton("🌐 ᴡᴇʙ ᴘᴀɴᴇʟ", url=f"{API_BASE}/web"),
            InlineKeyboardButton("📢 ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}"),
        ]
    ])


# ── /sᴛᴀʀᴛ ───────────────────────────────────────────────────────

@bot.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    user = message.from_user
    joined = await check_joined(client, user.id)

    if not joined:
        await message.reply_photo(
            photo=IMG_START,
            caption=(
                f"**⚡ ᴡᴇʟᴄᴏᴍᴇ, {user.first_name}!**\n\n"
                f"╔══════════════════╗\n"
                f"║  ᴀʀᴜ ʏᴛ ᴀᴘɪ ʙᴏᴛ  ║\n"
                f"╚══════════════════╝\n\n"
                f"📢 ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ, ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ\n"
                f"ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴄʟɪᴄᴋ **✅ ɪ ᴊᴏɪɴᴇᴅ**"
            ),
            reply_markup=join_keyboard()
        )
        return

    result = await api_get("/userkey", {
        "master_key": MASTER_KEY,
        "user_id": str(user.id)
    })

    if result.get("found"):
        key = result["key"]
        key_line = f"\n🔑 **ʏᴏᴜʀ ᴋᴇʏ:** `{key[:20]}...`"
        status = "✅ ᴀᴄᴛɪᴠᴇ"
    else:
        key_line = "\n⚠️ ɴᴏ ᴋᴇʏ ꜰᴏᴜɴᴅ — ᴄʟɪᴄᴋ **🔑 ᴍʏ ᴀᴘɪ ᴋᴇʏ**"
        status = "🔴 ɴᴏ ᴋᴇʏ"

    await message.reply_photo(
        photo=IMG_START,
        caption=(
            f"**⚡ ᴀʀᴜ ʏᴛ ᴀᴘɪ ʙᴏᴛ**\n\n"
            f"╔══════════════════╗\n"
            f"║  ʜᴇʟʟᴏ, {user.first_name[:10]}  \n"
            f"╚══════════════════╝\n\n"
            f"🎵 ꜰᴀsᴛ ʏᴏᴜᴛᴜʙᴇ ᴀᴜᴅɪᴏ & ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅs\n"
            f"📊 ᴛʀᴀᴄᴋ ʏᴏᴜʀ ᴜsᴀɢᴇ sᴛᴀᴛs\n"
            f"🔑 ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴀᴘɪ ᴋᴇʏs\n"
            f"{key_line}\n\n"
            f"**sᴛᴀᴛᴜs:** {status}\n"
            f"**ᴅᴇᴠ:** ᴘᴀɴᴅᴀ-ʙᴀʙʏ | **sᴜᴘᴘᴏʀᴛ:** @sxypndu"
        ),
        reply_markup=main_keyboard()
    )


# ── ᴄʜᴇᴄᴋ ᴊᴏɪɴ ────────────────────────────────────────────────

@bot.on_callback_query(filters.regex("check_join"))
async def check_join_cb(client: Client, cb: CallbackQuery):
    user = cb.from_user
    joined = await check_joined(client, user.id)

    if not joined:
        await cb.answer("❌ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ʏᴇᴛ!", show_alert=True)
        return

    await cb.answer("✅ ᴠᴇʀɪꜰɪᴇᴅ!")

    result = await api_get("/userkey", {
        "master_key": MASTER_KEY,
        "user_id": str(user.id)
    })

    key_line = f"\n🔑 **ʏᴏᴜʀ ᴋᴇʏ:** `{result['key'][:20]}...`" if result.get("found") else \
               "\n⚠️ ᴄʟɪᴄᴋ **🔑 ᴍʏ ᴀᴘɪ ᴋᴇʏ** ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴏɴᴇ!"

    await cb.message.edit_caption(
        caption=(
            f"**✅ ᴠᴇʀɪꜰɪᴇᴅ! ᴡᴇʟᴄᴏᴍᴇ {user.first_name}!**\n\n"
            f"╔══════════════════╗\n"
            f"║  ᴀʀᴜ ʏᴛ ᴀᴘɪ ʙᴏᴛ  ║\n"
            f"╚══════════════════╝\n\n"
            f"🎵 ꜰᴀsᴛ ʏᴏᴜᴛᴜʙᴇ ᴀᴜᴅɪᴏ & ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅs\n"
            f"📊 ᴛʀᴀᴄᴋ ʏᴏᴜʀ ᴜsᴀɢᴇ sᴛᴀᴛs\n"
            f"🔑 ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴀᴘɪ ᴋᴇʏs"
            f"{key_line}\n\n"
            f"**ᴅᴇᴠ:** ᴘᴀɴᴅᴀ-ʙᴀʙʏ | **sᴜᴘᴘᴏʀᴛ:** @sxypndu"
        ),
        reply_markup=main_keyboard()
    )


# ── 🔑 ᴍʏ ᴀᴘɪ ᴋᴇʏ ───────────────────────────────────────────────

@bot.on_callback_query(filters.regex("my_key"))
async def my_key_cb(client: Client, cb: CallbackQuery):
    user = cb.from_user
    await cb.answer()
    await cb.message.edit_caption(
        caption="**⏳ ꜰᴇᴛᴄʜɪɴɢ ʏᴏᴜʀ ᴋᴇʏ...**"
    )

    result = await api_get("/userkey", {
        "master_key": MASTER_KEY,
        "user_id": str(user.id)
    })

    if result.get("found"):
        key     = result["key"]
        created = result.get("created_at", "ɴ/ᴀ")
        label   = result.get("label", "ᴜsᴇʀ")
        await cb.message.edit_caption(
            caption=(
                f"**🔑 ʏᴏᴜʀ ᴀᴘɪ ᴋᴇʏ**\n\n"
                f"╔══════════════════╗\n"
                f"║  ᴀᴄᴛɪᴠᴇ ᴋᴇʏ ✅  ║\n"
                f"╚══════════════════╝\n\n"
                f"🔑 **ᴋᴇʏ:**\n`{key}`\n\n"
                f"📛 **ʟᴀʙᴇʟ:** `{label}`\n"
                f"🕐 **ᴄʀᴇᴀᴛᴇᴅ:** `{created}`\n\n"
                f"⚡ ᴜsᴇ ᴛʜɪs ᴀs `SHRUTI_API_KEY` ɪɴ ʏᴏᴜʀ ʙᴏᴛ\n"
                f"🌐 ᴄʜᴇᴄᴋ ᴜsᴀɢᴇ ᴀᴛ: `{API_BASE}/web`"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
                InlineKeyboardButton("📈 ᴜsᴀɢᴇ", callback_data="my_usage"),
            ]])
        )
    else:
        # Auto generate
        label = f"tg_{user.first_name[:10]}"
        gen = await api_get("/keygen", {
            "master_key": MASTER_KEY,
            "label":      label,
            "user_id":    str(user.id)
        })

        if gen.get("key"):
            key = gen["key"]
            await cb.message.edit_caption(
                caption=(
                    f"**✅ ᴀᴘɪ ᴋᴇʏ ɢᴇɴᴇʀᴀᴛᴇᴅ!**\n\n"
                    f"╔══════════════════╗\n"
                    f"║  ɴᴇᴡ ᴋᴇʏ ᴄʀᴇᴀᴛᴇᴅ  ║\n"
                    f"╚══════════════════╝\n\n"
                    f"🔑 **ʏᴏᴜʀ ᴋᴇʏ:**\n`{key}`\n\n"
                    f"📛 **ʟᴀʙᴇʟ:** `{label}`\n"
                    f"🕐 **ᴄʀᴇᴀᴛᴇᴅ:** `{gen.get('created_at', '')}`\n\n"
                    f"⚠️ **ᴋᴇᴇᴘ ᴛʜɪs ᴋᴇʏ sᴀꜰᴇ!**\n"
                    f"ᴅᴏɴ'ᴛ sʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ."
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
                    InlineKeyboardButton("📈 ᴜsᴀɢᴇ", callback_data="my_usage"),
                ]])
            )
        else:
            await cb.message.edit_caption(
                caption=f"**❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴋᴇʏ!**\n\n`{gen}`",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔄 ʀᴇᴛʀʏ", callback_data="my_key"),
                    InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
                ]])
            )


# ── 📈 ᴍʏ ᴜsᴀɢᴇ ──────────────────────────────────────────────────

@bot.on_callback_query(filters.regex("my_usage"))
async def my_usage_cb(client: Client, cb: CallbackQuery):
    user = cb.from_user
    await cb.answer()
    await cb.message.edit_caption(caption="**⏳ ꜰᴇᴛᴄʜɪɴɢ sᴛᴀᴛs...**")

    result = await api_get("/usage", {
        "master_key": MASTER_KEY,
        "user_id":    str(user.id)
    })

    if result.get("status") == "no_key":
        await cb.message.edit_caption(
            caption=(
                f"**❌ ɴᴏ ᴀᴘɪ ᴋᴇʏ ꜰᴏᴜɴᴅ!**\n\n"
                f"ɢᴇɴᴇʀᴀᴛᴇ ᴀ ᴋᴇʏ ꜰɪʀsᴛ ᴛᴏ sᴇᴇ sᴛᴀᴛs."
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔑 ɢᴇᴛ ᴋᴇʏ", callback_data="my_key"),
                InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
            ]])
        )
        return

    if result.get("status") == "success":
        t   = result["today"]
        a   = result["alltime"]
        key = result.get("api_key", "")
        await cb.message.edit_caption(
            caption=(
                f"**📈 ʏᴏᴜʀ ᴜsᴀɢᴇ sᴛᴀᴛs**\n\n"
                f"╔══════════════════╗\n"
                f"║    ᴛᴏᴅᴀʏ         ║\n"
                f"╠══════════════════╣\n"
                f"║ 📊 ʀᴇQᴜᴇsᴛs : `{t['requests']}`\n"
                f"║ 🎵 ᴀᴜᴅɪᴏ   : `{t['audio']}`\n"
                f"║ 🎬 ᴠɪᴅᴇᴏ   : `{t['video']}`\n"
                f"╠══════════════════╣\n"
                f"║    ᴀʟʟ-ᴛɪᴍᴇ      ║\n"
                f"╠══════════════════╣\n"
                f"║ 📊 ᴛᴏᴛᴀʟ   : `{a['total']}`\n"
                f"║ 🎵 ᴀᴜᴅɪᴏ   : `{a['audio']}`\n"
                f"║ 🎬 ᴠɪᴅᴇᴏ   : `{a['video']}`\n"
                f"╚══════════════════╝\n\n"
                f"🔑 **ᴋᴇʏ:** `{key[:18]}...`"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 ʀᴇꜰʀᴇsʜ", callback_data="my_usage"),
                InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
            ]])
        )
    else:
        await cb.message.edit_caption(
            caption=f"**❌ ᴇʀʀᴏʀ!**\n\n`{result}`",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
            ]])
        )


# ── 🗑 ᴅᴇʟᴇᴛᴇ ᴋᴇʏ ────────────────────────────────────────────────

@bot.on_callback_query(filters.regex("del_key"))
async def del_key_cb(client: Client, cb: CallbackQuery):
    user = cb.from_user
    await cb.answer()

    result = await api_get("/userkey", {
        "master_key": MASTER_KEY,
        "user_id":    str(user.id)
    })

    if not result.get("found"):
        await cb.message.edit_caption(
            caption="**❌ ɴᴏ ᴀᴘɪ ᴋᴇʏ ꜰᴏᴜɴᴅ!**",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
            ]])
        )
        return

    key = result["key"]
    await cb.message.edit_caption(
        caption=(
            f"**⚠️ ᴄᴏɴꜰɪʀᴍ ᴅᴇʟᴇᴛᴇ?**\n\n"
            f"╔══════════════════╗\n"
            f"║  ᴅᴀɴɢᴇʀ ᴢᴏɴᴇ ⚠️  ║\n"
            f"╚══════════════════╝\n\n"
            f"🔑 `{key[:22]}...`\n\n"
            f"ᴛʜɪs ᴡɪʟʟ **ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ ʀᴇᴠᴏᴋᴇ** ʏᴏᴜʀ ᴋᴇʏ!\n"
            f"ʏᴏᴜ ᴄᴀɴ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ɴᴇᴡ ᴏɴᴇ ᴀɴʏᴛɪᴍᴇ."
        ),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ ʏᴇs, ᴅᴇʟᴇᴛᴇ", callback_data="confirm_del"),
            InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="main_menu"),
        ]])
    )


@bot.on_callback_query(filters.regex("confirm_del"))
async def confirm_del_cb(client: Client, cb: CallbackQuery):
    user = cb.from_user
    await cb.answer()

    result = await api_get("/revoke", {
        "master_key": MASTER_KEY,
        "user_id":    str(user.id)
    })

    if result.get("status") == "success":
        await cb.message.edit_caption(
            caption=(
                f"**✅ ᴋᴇʏ ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ!**\n\n"
                f"ʏᴏᴜ ᴄᴀɴ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ɴᴇᴡ ᴋᴇʏ ᴀɴʏᴛɪᴍᴇ.\n\n"
                f"**ᴅᴇᴠ:** ᴘᴀɴᴅᴀ-ʙᴀʙʏ | **sᴜᴘᴘᴏʀᴛ:** @sxypndu"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔑 ɴᴇᴡ ᴋᴇʏ", callback_data="my_key"),
                InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
            ]])
        )
    else:
        await cb.message.edit_caption(
            caption=f"**❌ ꜰᴀɪʟᴇᴅ!**\n\n`{result}`",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
            ]])
        )


# ── 🏓 ᴘɪɴɢ ──────────────────────────────────────────────────────

@bot.on_callback_query(filters.regex("ping"))
async def ping_cb(client: Client, cb: CallbackQuery):
    await cb.answer()
    start_t = time.time()
    result  = await api_get("/ping", {})
    ms      = round((time.time() - start_t) * 1000)
    uptime  = result.get("uptime", 0)
    h       = int(uptime) // 3600
    m       = (int(uptime) % 3600) // 60

    status = "🟢 ᴇxᴄᴇʟʟᴇɴᴛ" if ms < 200 else "🟡 ɢᴏᴏᴅ" if ms < 500 else "🔴 sʟᴏᴡ"

    await cb.message.edit_caption(
        caption=(
            f"**🏓 ᴘᴏɴɢ!**\n\n"
            f"╔══════════════════╗\n"
            f"║   ᴀᴘɪ sᴛᴀᴛᴜs    ║\n"
            f"╠══════════════════╣\n"
            f"║ ⚡ ʟᴀᴛᴇɴᴄʏ : `{ms}ms`\n"
            f"║ 🕐 ᴜᴘᴛɪᴍᴇ  : `{h}ʜ {m}ᴍ`\n"
            f"║ 📶 sᴛᴀᴛᴜs  : {status}\n"
            f"╚══════════════════╝\n\n"
            f"**ᴅᴇᴠ:** ᴘᴀɴᴅᴀ-ʙᴀʙʏ | **sᴜᴘᴘᴏʀᴛ:** @sxypndu"
        ),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔄 ʀᴇꜰʀᴇsʜ", callback_data="ping"),
            InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
        ]])
    )


# ── 🏠 ᴍᴀɪɴ ᴍᴇɴᴜ ─────────────────────────────────────────────────

@bot.on_callback_query(filters.regex("main_menu"))
async def main_menu_cb(client: Client, cb: CallbackQuery):
    user = cb.from_user
    await cb.answer()

    result = await api_get("/userkey", {
        "master_key": MASTER_KEY,
        "user_id":    str(user.id)
    })

    if result.get("found"):
        key_line = f"\n🔑 **ᴋᴇʏ:** `{result['key'][:18]}...`"
        status   = "✅ ᴀᴄᴛɪᴠᴇ"
    else:
        key_line = "\n⚠️ ɴᴏ ᴋᴇʏ — ᴄʟɪᴄᴋ **🔑 ᴍʏ ᴀᴘɪ ᴋᴇʏ**"
        status   = "🔴 ɴᴏ ᴋᴇʏ"

    await cb.message.edit_caption(
        caption=(
            f"**⚡ ᴀʀᴜ ʏᴛ ᴀᴘɪ ʙᴏᴛ**\n\n"
            f"╔══════════════════╗\n"
            f"║  ʜᴇʟʟᴏ, {user.first_name[:10]}  \n"
            f"╚══════════════════╝\n\n"
            f"🎵 ꜰᴀsᴛ ʏᴏᴜᴛᴜʙᴇ ᴅᴏᴡɴʟᴏᴀᴅs\n"
            f"📊 ᴛʀᴀᴄᴋ ʏᴏᴜʀ ᴜsᴀɢᴇ"
            f"{key_line}\n\n"
            f"**sᴛᴀᴛᴜs:** {status}\n"
            f"**ᴅᴇᴠ:** ᴘᴀɴᴅᴀ-ʙᴀʙʏ | **sᴜᴘᴘᴏʀᴛ:** @sxypndu"
        ),
        reply_markup=main_keyboard()
    )


# ── /ᴍʏᴋᴇʏ ───────────────────────────────────────────────────────

@bot.on_message(filters.command("mykey") & filters.private)
async def mykey_cmd(client: Client, message: Message):
    user = message.from_user
    result = await api_get("/userkey", {
        "master_key": MASTER_KEY,
        "user_id":    str(user.id)
    })
    if result.get("found"):
        await message.reply_photo(
            photo=IMG_KEY,
            caption=(
                f"**🔑 ʏᴏᴜʀ ᴀᴘɪ ᴋᴇʏ**\n\n"
                f"`{result['key']}`\n\n"
                f"🕐 **ᴄʀᴇᴀᴛᴇᴅ:** `{result.get('created_at', 'ɴ/ᴀ')}`\n"
                f"**sᴛᴀᴛᴜs:** ✅ ᴀᴄᴛɪᴠᴇ"
            )
        )
    else:
        await message.reply_text(
            "**❌ ɴᴏ ᴋᴇʏ ꜰᴏᴜɴᴅ!**\n\nᴜsᴇ /start ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴏɴᴇ."
        )


# ── ʀᴜɴ ──────────────────────────────────────────────────────────

print("🚀 ᴀʀᴜ ʏᴛ ᴀᴘɪ ʙᴏᴛ sᴛᴀʀᴛɪɴɢ... | ᴅᴇᴠ: ᴘᴀɴᴅᴀ-ʙᴀʙʏ")
bot.run()
