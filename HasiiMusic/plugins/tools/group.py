from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import ChatSendPlainForbidden, ChatWriteForbidden, Forbidden, ChannelPrivate

from HasiiMusic import app
from config import OWNER_ID


async def _safe_reply_text(message: Message, *args, **kwargs):
    chat = getattr(message, "chat", None)
    if not chat or chat.type == ChatType.CHANNEL:
        return
    try:
        await message.reply_text(*args, **kwargs)
    except (ChatSendPlainForbidden, ChatWriteForbidden, Forbidden, ChannelPrivate):
        pass


@app.on_message(filters.video_chat_started & filters.group)
async def on_voice_chat_started(_, message: Message):
    await _safe_reply_text(message, "🎙 **Cuộc trò chuyện thoại đã bắt đầu!**")


@app.on_message(filters.video_chat_ended & filters.group)
async def on_voice_chat_ended(_, message: Message):
    await _safe_reply_text(message, "🔕 **Cuộc trò chuyện thoại đã kết thúc.**")


@app.on_message(filters.video_chat_participants_invited_filter & filters.group)
async def on_voice_chat_members_invited(_, message: Message):
    inviter = "Someone"
    if message.from_user:
        try:
            inviter = message.from_user.mention(message.from_user.first_name)
        except Exception:
            inviter = message.from_user.first_name or "Someone"

    invited = []
    vcmi = getattr(message, "video_chat_participants_invited_filter", None)
    users = getattr(vcmi, "users", []) if vcmi else []
    for user in users:
        try:
            name = user.first_name or "User"
            invited.append(f"[{name}](tg://user?id={user.id})")
        except Exception:
            continue

    if invited:
        await _safe_reply_text(
            message,
            f"👥 {inviter} Đã mời {', '.join(invited)} vào cuộc trò chuyện thoại. 😉",
        )


@app.on_message(filters.command("leavegroup") & filters.user(OWNER_ID) & filters.group)
async def leave_group(_, message: Message):
    await _safe_reply_text(message, "👋 **Đang rời nhóm này...**")
    try:
        await app.leave_chat(chat_id=message.chat.id, delete=True)
    except (ChatWriteForbidden, Forbidden, ChannelPrivate):
        pass
