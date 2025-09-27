import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

# Load environment variables from .env file
load_dotenv()

# ── Core bot config ────────────────────────────────────────────────────────────
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN")

OWNER_ID = int(getenv("OWNER_ID", ""))
OWNER_USERNAME = getenv("OWNER_USERNAME", "")
BOT_USERNAME = getenv("BOT_USERNAME", "")
BOT_NAME = getenv("BOT_NAME", "˹ ♪")
ASSUSERNAME = getenv("ASSUSERNAME", "")

# ── Database & logging ─────────────────────────────────────────────────────────
MONGO_DB_URI = getenv("MONGO_DB_URI")
LOGGER_ID = int(getenv("LOGGER_ID", ))
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", "True")
# ── Limits (durations in min/sec; sizes in bytes) ──────────────────────────────
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 30000))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "120000"))
SONG_DOWNLOAD_DURATION_LIMIT = int(
    getenv("SONG_DOWNLOAD_DURATION_LIMIT", "180000"))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "15728640000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "128849018900"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "50"))

# ── External APIs ──────────────────────────────────────────────────────────────
COOKIE_URL = getenv("COOKIE_URL")  # required (paste link)
API_URL = getenv("API_URL")        # optional
API_KEY = getenv("API_KEY")        # optional
DEEP_API = getenv("DEEP_API")      # optional

# ── Hosting / deployment ───────────────────────────────────────────────────────
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ── Git / updates ──────────────────────────────────────────────────────────────
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO", "https://github.com/tmq247/tram4")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv("GIT_TOKEN")  # needed if repo is private

# ── Support links ──────────────────────────────────────────────────────────────
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/COIHAYCOC")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/muoimuoimusicbot")

# ── Assistant auto-leave ───────────────────────────────────────────────────────
AUTO_LEAVING_ASSISTANT = False
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "3600"))

# ── Debug ──────────────────────────────────────────────────────────────────────
DEBUG_IGNORE_LOG = True

# ── Spotify (optional) ─────────────────────────────────────────────────────────
SPOTIFY_CLIENT_ID = getenv(
    "SPOTIFY_CLIENT_ID", "22b6125bfe224587b722d6815002db2b")
SPOTIFY_CLIENT_SECRET = getenv(
    "SPOTIFY_CLIENT_SECRET", "c9c63c6fbf2f467c8bc68624851e9773")

# ── Session strings (optional) ─────────────────────────────────────────────────
STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")

# ── Media assets ───────────────────────────────────────────────────────────────
START_VIDS = [
    "https://telegra.ph/file/9b7e1b820c72a14d90be7.mp4",
    "https://telegra.ph/file/72f349b1386d6d9374a38.mp4",
    "https://telegra.ph/file/a4d90b0cb759b67d68644.mp4"
]

STICKERS = [
    "CAACAgUAAx0Cd6nKUAACASBl_rnalOle6g7qS-ry-aZ1ZpVEnwACgg8AAizLEFfI5wfykoCR4h4E",
    "CAACAgUAAx0Cd6nKUAACATJl_rsEJOsaaPSYGhU7bo7iEwL8AAPMDgACu2PYV8Vb8aT4_HUPHgQ"
]
HELP_IMG_URL = "https://files.catbox.moe/139oue.png"
PING_VID_URL = "https://files.catbox.moe/hssx04.png"
PLAYLIST_IMG_URL = "https://files.catbox.moe/k2yqsd.png"
STATS_VID_URL = "https://telegra.ph/file/e2ab6106ace2e95862372.mp4"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/bnzdl9.png"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/bnzdl9.png"
STREAM_IMG_URL = "https://files.catbox.moe/bnzdl9.png"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/bnzdl9.png"
YOUTUBE_IMG_URL = "https://files.catbox.moe/bnzdl9.png"
SPOTIFY_ARTIST_IMG_URL = SPOTIFY_ALBUM_IMG_URL = SPOTIFY_PLAYLIST_IMG_URL = YOUTUBE_IMG_URL

# ── Helpers ────────────────────────────────────────────────────────────────────


def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))


DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")

# ───── Bot Introduction Messages ───── #
AYU = [
    "▰▱▱▱▱▱▱▱▱ Đang xử lý... 💞",
    "▰▰▱▱▱▱▱▱▱ Đang tìm kiếm... 🔍",
    "▰▰▰▱▱▱▱▱▱ Đang tải... ⚡",
    "▰▰▰▰▱▱▱▱▱ Đang kết nối... 🌐",
    "▰▰▰▰▰▱▱▱▱ Đang chuẩn bị... 🔧",
    "▰▰▰▰▰▰▱▱▱ Gần xong... ⏳",
    "▰▰▰▰▰▰▰▱▱ Đang xác minh... 🛡️",
    "▰▰▰▰▰▰▰▰▱ Đang bắt đầu... 🦋",
    "💞", "🦋", "🔍", "🧪", "⚡️", "🔥", "🎩", "🌈", "🍷", "🥂", "🥃", "🕊️", "🪄", "💌", "🧨"
]
AYUV = [
    "Xin chào {0}, 🥀\n\n Mình là {1} !\n\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ◆ Hỗ trợ nền tảng : YouTube, Spotify,\n┠ ◆ Resso, AppleMusic, SoundCloud v.v.\n┗━━━━━━━━━━━━━━━━━⧫\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ➥ Thời gian hoạt động : {2}\n┠ ➥ Bộ nhớ máy chủ : {3}\n┠ ➥ Tải CPU : {4}\n┠ ➥ RAM sử dụng : {5}\n┠ ➥ Người dùng : {6}\n┠ ➥ Nhóm/Chat : {7}\n┗━━━━━━━━━━━━━━━━━⧫\n\n🫧 Nhà phát triển 🪽 ➪ [Còi ✔︎](https://t.me/COIHAYCOC)",
    "Chào bạn, {0} ~\n\n◆ Mình là {1}, một bot phát trực tuyến trên Telegram với nhiều tính năng hữu ích.\n◆ Trình phát VC siêu nhanh.\n\n✨ Tính năng ⚡️\n◆ Bot dành cho nhóm Telegram.\n◆ Trình phát siêu nhanh, không lag.\n◆ Có thể phát nhạc + video.\n◆ Phát trực tiếp.\n◆ Không quảng cáo.\n◆ Chất lượng âm thanh tốt nhất.\n◆ Phát nhạc 24×7.\n◆ Thêm bot này vào nhóm của bạn, cấp quyền admin và thưởng thức âm nhạc 🎵.\n\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ◆ Hỗ trợ nền tảng : YouTube, Spotify,\n┠ ◆ Resso, AppleMusic, SoundCloud v.v.\n┗━━━━━━━━━━━━━━━━━⧫\n┏━━━━━━━━━━━━━━━━━⧫\n┠ ➥ Thời gian hoạt động : {2}\n┠ ➥ Bộ nhớ máy chủ : {3}\n┠ ➥ Tải CPU : {4}\n┠ ➥ RAM sử dụng : {5}\n┠ ➥ Người dùng : {6}\n┠ ➥ Nhóm/Chat : {7}\n┗━━━━━━━━━━━━━━━━━⧫\n\n🫧 Nhà phát triển 🪽 ➪ [Còi ✔︎](https://t.me/COIHAYCOC)",
]


# ── Runtime structures ─────────────────────────────────────────────────────────
BANNED_USERS = filters.user()
adminlist, lyrical, votemode, autoclean, confirmer = {}, {}, {}, [], {}

# ── Minimal validation ─────────────────────────────────────────────────────────
if SUPPORT_CHANNEL and not re.match(r"^https?://", SUPPORT_CHANNEL):
    raise SystemExit(
        "[ERROR] - Invalid SUPPORT_CHANNEL URL. Must start with https://")

if SUPPORT_CHAT and not re.match(r"^https?://", SUPPORT_CHAT):
    raise SystemExit(
        "[ERROR] - Invalid SUPPORT_CHAT URL. Must start with https://")

if not COOKIE_URL:
    raise SystemExit("[ERROR] - COOKIE_URL is required.")

# Only allow these cookie link formats
if not re.match(r"^https://(batbin\.me|pastebin\.com)/[A-Za-z0-9]+$", COOKIE_URL):
    raise SystemExit(
        "[ERROR] - Invalid COOKIE_URL. Use https://batbin.me/<id> or https://pastebin.com/<id>")
