# ================================================================
#  ᴀʀᴜ ʏᴛ ᴀᴘɪ — ᴛᴇʟᴇɢʀᴀᴍ ʙᴏᴛ
#  ᴅᴇᴠ: ᴘᴀɴᴅᴀ-ʙᴀʙʏ | sᴜᴘᴘᴏʀᴛ: @sxypndu
# ================================================================

import os
import time
import json
import asyncio
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineKeyboardMarkup,
    InlineKeyboardButton, CallbackQuery, WebAppInfo
)

# ── ᴄᴏɴꜰɪɢ ───────────────────────────────────────────────────────
API_ID     = int(os.environ.get("API_ID", "20898349"))
API_HASH   = os.environ.get("API_HASH", "9fdb830d1e435b785f536247f49e7d87")
BOT_TOKEN  = os.environ.get("BOT_TOKEN", "8628709880:AAHw1FOZ2-7KS7S2v0jxlip1m4yB0jG-Whc")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@sxypndu")
MASTER_KEY = os.environ.get("MASTER_KEY", "YukiMasterAdmin2026")
API_BASE   = os.environ.get("API_BASE", "https://web-production-6415.up.railway.app")
LOG_GROUP  = os.environ.get("LOG_GROUP", "-1003468477782")

# ── ɪᴍᴀɢᴇs ───────────────────────────────────────────────────────
IMG_START = os.environ.get("IMG_START", "https://files.catbox.moe/bd3cqo.jpg")
IMG_KEY   = os.environ.get("IMG_KEY",   "https://files.catbox.moe/bd3cqo.jpg")

bot = Client("ARUAPIBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ── ᴄᴀᴄʜᴇ — reduces API calls drastically ────────────────────────
# {user_id: {"key": ..., "found": ..., "ts": ...}}
_key_cache: dict = {}
CACHE_TTL = 300  # 5 minutes

def _get_cached_key(user_id: int):
    c = _key_cache.get(user_id)
    if c and time.time() - c["ts"] < CACHE_TTL:
        return c
    return None

def _set_cached_key(user_id: int, data: dict):
    _key_cache[user_id] = {**data, "ts": time.time()}

def _invalidate_cache(user_id: int):
    _key_cache.pop(user_id, None)

# ── ᴜsᴇʀs ────────────────────────────────────────────────────────
USERS_FILE  = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(list(users), f)

known_users = load_users()

# ── ʜᴇʟᴘᴇʀs ──────────────────────────────────────────────────────

# Shared aiohttp session for speed
_session: aiohttp.ClientSession = None

async def get_session():
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=20, ttl_dns_cache=300),
            timeout=aiohttp.ClientTimeout(total=15)
        )
    return _session

async def api_get(endpoint: str, params: dict) -> dict:
    try:
        session = await get_session()
        async with session.get(f"{API_BASE}{endpoint}", params=params) as resp:
            return await resp.json()
    except Exception as e:
        return {"error": str(e)}

async def check_joined(client, user_id: int) -> bool:
    try:
        member = await client.get_chat_member(CHANNEL_ID, user_id)
        return member.status.name not in ["LEFT", "BANNED", "RESTRICTED"]
    except:
        return False

async def get_user_key(user_id: int) -> dict:
    """Get key with cache"""
    cached = _get_cached_key(user_id)
    if cached:
        return cached
    result = await api_get("/userkey", {
        "master_key": MASTER_KEY,
        "user_id": str(user_id)
    })
    _set_cached_key(user_id, result)
    return result

async def log_new_user(client, user):
    global known_users
    if user.id not in known_users:
        known_users.add(user.id)
        save_users(known_users)
        username  = f"@{user.username}" if user.username else "ɴ/ᴀ"
        text_link = f"[{user.first_name}](tg://user?id={user.id})"
        try:
            await client.send_message(
                LOG_GROUP,
                f"**ɴᴇᴡ ᴜsᴇʀ** 🚀\n\n"
                f"**ɴᴀᴍᴇ :** {text_link}\n"
                f"**ɪᴅ :** `{user.id}`\n"
                f"**ᴜsᴇʀɴᴀᴍᴇ :** {username}\n"
                f"**ᴛᴏᴛᴀʟ :** `{len(known_users)}`",
                disable_web_page_preview=True
            )
        except:
            pass

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
            InlineKeyboardButton("🌐 ᴀᴘɪ ᴜʀʟ", url=f"{API_BASE}"),
            InlineKeyboardButton("📢 ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}"),
        ],
        [
            InlineKeyboardButton("🌍 ᴡᴇʙ ᴘᴀɴᴇʟ", web_app=WebAppInfo(url=f"{API_BASE}/web"))
        ]
    ])

def start_caption(user, key_line, status):
    return (
        f"**⚡ ᴀʀᴜ ʏᴛ ᴀᴘɪ ʙᴏᴛ**\n\n"
        f"╔══════════════════╗\n"
        f"║  ʜᴇʟʟᴏ, {user.first_name[:10]}\n"
        f"╚══════════════════╝\n\n"
        f"🎵 ꜰᴀsᴛ ʏᴏᴜᴛᴜʙᴇ ᴀᴜᴅɪᴏ & ᴠɪᴅᴇᴏ\n"
        f"📊 ᴛʀᴀᴄᴋ ʏᴏᴜʀ ᴜsᴀɢᴇ sᴛᴀᴛs\n"
        f"🔑 ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴀᴘɪ ᴋᴇʏs\n"
        f"{key_line}\n\n"
        f"**sᴛᴀᴛᴜs:** {status}\n"
        f"**ᴅᴇᴠ:** ᴘᴀɴᴅᴀ-ʙᴀʙʏ | **sᴜᴘᴘᴏʀᴛ:** @sxypndu"
    )


# ── /sᴛᴀʀᴛ ───────────────────────────────────────────────────────

@bot.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    user = message.from_user

    # Run join check + log + key fetch in parallel
    joined, _ = await asyncio.gather(
        check_joined(client, user.id),
        log_new_user(client, user)
    )

    if not joined:
        await message.reply_photo(
            photo=IMG_START,
            caption=(
                f"**⚡ ᴡᴇʟᴄᴏᴍᴇ, {message.from_user.mention}!**\n\n"
                f"╔══════════════════╗\n"
                f"║  ᴀʀᴜ ʏᴛ ᴀᴘɪ ʙᴏᴛ  ║\n"
                f"╚══════════════════╝\n\n"
                f"📢 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ & ᴄʟɪᴄᴋ **✅ ɪ ᴊᴏɪɴᴇᴅ**"
            ),
            reply_markup=join_keyboard()
        )
        return

    result = await get_user_key(user.id)
    if result.get("found"):
        key_line = f"\n🔑 **ʏᴏᴜʀ ᴋᴇʏ:** `{result['key'][:20]}...`"
        status   = "✅ ᴀᴄᴛɪᴠᴇ"
    else:
        key_line = "\n⚠️ ɴᴏ ᴋᴇʏ — ᴄʟɪᴄᴋ **🔑 ᴍʏ ᴀᴘɪ ᴋᴇʏ**"
        status   = "🔴 ɴᴏ ᴋᴇʏ"

    await message.reply_photo(
        photo=IMG_START,
        caption=start_caption(user, key_line, status),
        reply_markup=main_keyboard()
    )


# ── /sᴛᴀᴛs ───────────────────────────────────────────────────────

@bot.on_message(filters.command("stats") & filters.private)
async def stats_cmd(client: Client, message: Message):
    await message.reply_photo(
        photo=IMG_START,
        caption=(
            f"**📊 ʙᴏᴛ sᴛᴀᴛs**\n\n"
            f"╔══════════════════╗\n"
            f"║   ʀᴇᴀʟ ᴛɪᴍᴇ     ║\n"
            f"╚══════════════════╝\n\n"
            f"👥 **ᴛᴏᴛᴀʟ ᴜsᴇʀs :** `{len(known_users)}`\n"
            f"✅ **ʙᴏᴛ sᴛᴀᴛᴜs :** ᴀᴄᴛɪᴠᴇ\n\n"
            f"**ᴅᴇᴠ:** ᴘᴀɴᴅᴀ-ʙᴀʙʏ | **sᴜᴘᴘᴏʀᴛ:** @sxypndu"
        )
    )


# ── ᴄʜᴇᴄᴋ ᴊᴏɪɴ ────────────────────────────────────────────────

@bot.on_callback_query(filters.regex("check_join"))
async def check_join_cb(client: Client, cb: CallbackQuery):
    user   = cb.from_user
    joined = await check_joined(client, user.id)

    if not joined:
        await cb.answer("❌ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ʏᴇᴛ!", show_alert=True)
        return

    await cb.answer("✅ ᴠᴇʀɪꜰɪᴇᴅ!")
    result   = await get_user_key(user.id)
    key_line = f"\n🔑 **ᴋᴇʏ:** `{result['key'][:20]}...`" if result.get("found") else \
               "\n⚠️ ᴄʟɪᴄᴋ **🔑 ᴍʏ ᴀᴘɪ ᴋᴇʏ**"
    status   = "✅ ᴀᴄᴛɪᴠᴇ" if result.get("found") else "🔴 ɴᴏ ᴋᴇʏ"

    await cb.message.edit_caption(
        caption=start_caption(user, key_line, status),
        reply_markup=main_keyboard()
    )


# ── 🔑 ᴍʏ ᴀᴘɪ ᴋᴇʏ ───────────────────────────────────────────────

@bot.on_callback_query(filters.regex("my_key"))
async def my_key_cb(client: Client, cb: CallbackQuery):
    user = cb.from_user
    await cb.answer()

    # Use cache — no waiting message needed if cache hit
    cached = _get_cached_key(user.id)
    if not cached:
        await cb.message.edit_caption(caption="**⏳ ꜰᴇᴛᴄʜɪɴɢ...**")

    result = await get_user_key(user.id)

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
                f"⚡ ᴜsᴇ ᴀs `SHRUTI_API_KEY` ɪɴ ʙᴏᴛ\n"
                f"🌐 `{API_BASE}`"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
                InlineKeyboardButton("📈 ᴜsᴀɢᴇ", callback_data="my_usage"),
            ]])
        )
    else:
        # Auto generate
        label = f"tg_{user.first_name[:10]}"
        gen   = await api_get("/keygen", {
            "master_key": MASTER_KEY,
            "label":      label,
            "user_id":    str(user.id)
        })
        if gen.get("key"):
            _set_cached_key(user.id, {**gen, "found": True})
            await cb.message.edit_caption(
                caption=(
                    f"**✅ ᴀᴘɪ ᴋᴇʏ ɢᴇɴᴇʀᴀᴛᴇᴅ!**\n\n"
                    f"╔══════════════════╗\n"
                    f"║  ɴᴇᴡ ᴋᴇʏ ᴄʀᴇᴀᴛᴇᴅ  ║\n"
                    f"╚══════════════════╝\n\n"
                    f"🔑 **ᴋᴇʏ:**\n`{gen['key']}`\n\n"
                    f"📛 **ʟᴀʙᴇʟ:** `{label}`\n"
                    f"🕐 **ᴄʀᴇᴀᴛᴇᴅ:** `{gen.get('created_at', '')}`\n\n"
                    f"⚠️ **ᴋᴇᴇᴘ ᴛʜɪs sᴀꜰᴇ!** ᴅᴏɴ'ᴛ sʜᴀʀᴇ."
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
                    InlineKeyboardButton("📈 ᴜsᴀɢᴇ", callback_data="my_usage"),
                ]])
            )
        else:
            await cb.message.edit_caption(
                caption=f"**❌ ꜰᴀɪʟᴇᴅ!**\n\n`{gen}`",
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
    await cb.message.edit_caption(caption="**⏳ ꜰᴇᴛᴄʜɪɴɢ...**")

    result = await api_get("/usage", {
        "master_key": MASTER_KEY,
        "user_id":    str(user.id)
    })

    if result.get("status") == "no_key":
        await cb.message.edit_caption(
            caption="**❌ ɴᴏ ᴀᴘɪ ᴋᴇʏ!**\nɢᴇɴᴇʀᴀᴛᴇ ᴏɴᴇ ꜰɪʀsᴛ.",
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
                f"🔑 `{key[:18]}...`"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔄 ʀᴇꜰʀᴇsʜ", callback_data="my_usage"),
                InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
            ]])
        )
    else:
        await cb.message.edit_caption(
            caption=f"**❌ ᴇʀʀᴏʀ!**\n`{result}`",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
            ]])
        )


# ── 🗑 ᴅᴇʟᴇᴛᴇ ᴋᴇʏ ────────────────────────────────────────────────

@bot.on_callback_query(filters.regex("del_key"))
async def del_key_cb(client: Client, cb: CallbackQuery):
    user = cb.from_user
    await cb.answer()

    result = await get_user_key(user.id)
    if not result.get("found"):
        await cb.message.edit_caption(
            caption="**❌ ɴᴏ ᴋᴇʏ ꜰᴏᴜɴᴅ!**",
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
            f"ᴛʜɪs ᴡɪʟʟ **ᴘᴇʀᴍᴀɴᴇɴᴛʟʏ ʀᴇᴠᴏᴋᴇ** ʏᴏᴜʀ ᴋᴇʏ!"
        ),
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ ʏᴇs", callback_data="confirm_del"),
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

    _invalidate_cache(user.id)  # Clear cache after revoke

    if result.get("status") == "success":
        await cb.message.edit_caption(
            caption=(
                f"**✅ ᴋᴇʏ ᴅᴇʟᴇᴛᴇᴅ!**\n\n"
                f"ɢᴇɴᴇʀᴀᴛᴇ ᴀ ɴᴇᴡ ᴋᴇʏ ᴀɴʏᴛɪᴍᴇ.\n\n"
                f"**ᴅᴇᴠ:** ᴘᴀɴᴅᴀ-ʙᴀʙʏ | @sxypndu"
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔑 ɴᴇᴡ ᴋᴇʏ", callback_data="my_key"),
                InlineKeyboardButton("🏠 ᴍᴇɴᴜ", callback_data="main_menu"),
            ]])
        )
    else:
        await cb.message.edit_caption(
            caption=f"**❌ ꜰᴀɪʟᴇᴅ!**\n`{result}`",
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
    status  = "🟢 ᴇxᴄᴇʟʟᴇɴᴛ" if ms < 200 else "🟡 ɢᴏᴏᴅ" if ms < 500 else "🔴 sʟᴏᴡ"

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
            f"**ᴅᴇᴠ:** ᴘᴀɴᴅᴀ-ʙᴀʙʏ | @sxypndu"
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

    result   = await get_user_key(user.id)  # cached — instant
    key_line = f"\n🔑 **ᴋᴇʏ:** `{result['key'][:18]}...`" if result.get("found") else \
               "\n⚠️ ɴᴏ ᴋᴇʏ — ᴄʟɪᴄᴋ **🔑 ᴍʏ ᴀᴘɪ ᴋᴇʏ**"
    status   = "✅ ᴀᴄᴛɪᴠᴇ" if result.get("found") else "🔴 ɴᴏ ᴋᴇʏ"

    await cb.message.edit_caption(
        caption=start_caption(user, key_line, status),
        reply_markup=main_keyboard()
    )


# ── /ᴍʏᴋᴇʏ ───────────────────────────────────────────────────────

@bot.on_message(filters.command("mykey") & filters.private)
async def mykey_cmd(client: Client, message: Message):
    user   = message.from_user
    result = await get_user_key(user.id)
    if result.get("found"):
        await message.reply_photo(
            photo=IMG_KEY,
            caption=(
                f"**🔑 ʏᴏᴜʀ ᴀᴘɪ ᴋᴇʏ**\n\n"
                f"`{result['key']}`\n\n"
                f"🕐 `{result.get('created_at', 'ɴ/ᴀ')}`\n"
                f"**sᴛᴀᴛᴜs:** ✅ ᴀᴄᴛɪᴠᴇ"
            )
        )
    else:
        await message.reply_text("**❌ ɴᴏ ᴋᴇʏ!** ᴜsᴇ /start")


# ── ʀᴜɴ ──────────────────────────────────────────────────────────

print("🚀 ᴀʀᴜ ʏᴛ ᴀᴘɪ ʙᴏᴛ | ᴅᴇᴠ: ᴘᴀɴᴅᴀ-ʙᴀʙʏ")
bot.run()
