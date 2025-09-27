import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatJoinRequest
from pyrogram.errors import (
    ChatAdminRequired,
    UserAlreadyParticipant,
    UserNotParticipant,
    ChannelPrivate,
    FloodWait,
    PeerIdInvalid,
    ChatWriteForbidden,
)

from HasiiMusic import app
from HasiiMusic.utils.admin_filters import dev_filter, admin_filter, sudo_filter
from HasiiMusic.utils.database import get_assistant


ACTIVE_STATUSES = {
    ChatMemberStatus.OWNER,
    ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.MEMBER,
    ChatMemberStatus.RESTRICTED,
}


async def _is_participant(client, chat_id, user_id) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ACTIVE_STATUSES
    except UserNotParticipant:
        return False
    except PeerIdInvalid:
        return False
    except Exception:
        return False


async def join_userbot(app, chat_id, chat_username=None):
    userbot = await get_assistant(chat_id)

    try:
        member = await app.get_chat_member(chat_id, userbot.id)
        if member.status == ChatMemberStatus.BANNED:
            try:
                await app.unban_chat_member(chat_id, userbot.id)
            except ChatAdminRequired:
                return "**❌ Tôi cần quyền gỡ cấm để thêm trợ lý.**"
        if member.status in ACTIVE_STATUSES:
            return "**🤖 Trợ lý đã có trong cuộc trò chuyện.**"
    except UserNotParticipant:
        pass
    except PeerIdInvalid:
        return "**❌ ID cuộc trò chuyện không hợp lệ.**"

    invite = None
    if chat_username:
        invite = chat_username if chat_username.startswith("@") else f"@{chat_username}"
    else:
        try:
            link = await app.create_chat_invite_link(chat_id)
            invite = link.invite_link
        except ChatAdminRequired:
            return "**❌ Tôi cần quyền tạo liên kết mời hoặc một @username công khai để thêm trợ lý.**"

    try:
        await userbot.join_chat(invite)
        return "**✅ Trợ lý đã tham gia thành công.**"
    except UserAlreadyParticipant:
        return "**🤖 Trợ lý đã là một thành viên.**"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        try:
            await userbot.join_chat(invite)
            return "**✅ Trợ lý đã tham gia thành công.**"
        except Exception as ex:
            return f"**❌ Không thể thêm trợ lý sau khi chờ:** `{str(ex)}`"
    except Exception as e:
        return f"**❌ Không thể thêm trợ lý:** `{str(e)}`"


@app.on_chat_join_request()
async def approve_join_request(client, chat_join_request: ChatJoinRequest):
    userbot = await get_assistant(chat_join_request.chat.id)
    if chat_join_request.from_user.id != userbot.id:
        return
    chat_id = chat_join_request.chat.id

    try:
        if await _is_participant(client, chat_id, userbot.id):
            return
        try:
            await client.approve_chat_join_request(chat_id, userbot.id)
        except UserAlreadyParticipant:
            return
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.approve_chat_join_request(chat_id, userbot.id)
            except UserAlreadyParticipant:
                return
        try:
            await client.send_message(chat_id, "**✅ Trợ lý đã được chấp thuận và tham gia cuộc trò chuyện.**")
        except ChatWriteForbidden:
            pass
    except ChatAdminRequired:
        return
    except PeerIdInvalid:
        return
    except Exception:
        return


@app.on_message(
    filters.command(["userbotjoin", "assistantjoin"], prefixes=[".", "/"])
    & (filters.group | filters.private)
    & admin_filter
    & sudo_filter
)
async def join_group(app, message):
    chat_id = message.chat.id
    status_message = await message.reply("**⏳ Vui lòng chờ, đang mời trợ lý...**")

    try:
        me = await app.get_me()
        chat_member = await app.get_chat_member(chat_id, me.id)
        if chat_member.status != ChatMemberStatus.ADMINISTRATOR:
            await status_message.edit_text("**❌ Tôi cần là quản trị viên để mời trợ lý.**")
            return
    except ChatAdminRequired:
        await status_message.edit_text("**❌ Tôi không có quyền kiểm tra trạng thái quản trị viên trong cuộc trò chuyện này.**")
        return
    except Exception as e:
        await status_message.edit_text(f"**❌ Không thể xác minh quyền:** `{str(e)}`")
        return

    chat_username = message.chat.username or None
    response = await join_userbot(app, chat_id, chat_username)
    try:
        await status_message.edit_text(response)
    except ChatWriteForbidden:
        pass


@app.on_message(
    filters.command("userbotleave", prefixes=[".", "/"])
    & filters.group
    & admin_filter
    & sudo_filter
)
async def leave_one(app, message):
    chat_id = message.chat.id
    try:
        userbot = await get_assistant(chat_id)
        try:
            member = await userbot.get_chat_member(chat_id, userbot.id)
        except UserNotParticipant:
            await message.reply("**🤖 Trợ lý hiện không có trong cuộc trò chuyện này.**")
            return

        if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
            await message.reply("**🤖 Trợ lý hiện không có trong cuộc trò chuyện này.**")
            return

        await userbot.leave_chat(chat_id)
        try:
            await app.send_message(chat_id, "**✅ Trợ lý đã rời cuộc trò chuyện này.**")
        except ChatWriteForbidden:
            pass
    except ChannelPrivate:
        await message.reply("**❌ Lỗi: Cuộc trò chuyện này không thể truy cập hoặc đã bị xóa.**")
    except UserNotParticipant:
        await message.reply("**🤖 Trợ lý không có trong cuộc trò chuyện này.**")
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.reply("**✅ Đã thử lại sau khi chờ flood; hãy thử lại lệnh nếu cần.**")
    except Exception as e:
        await message.reply(f"**❌ Không thể xóa trợ lý:** `{str(e)}`")


@app.on_message(filters.command("leaveall", prefixes=["."]) & dev_filter)
async def leave_all(app, message):
    left = 0
    failed = 0
    status_message = await message.reply("🔄 **Trợ lý đang rời khỏi tất cả các cuộc trò chuyện...**")

    try:
        userbot = await get_assistant(message.chat.id)
        async for dialog in userbot.get_dialogs():
            if dialog.chat.id == -1001816641523:
                continue
            try:
                await userbot.leave_chat(dialog.chat.id)
                left += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await userbot.leave_chat(dialog.chat.id)
                    left += 1
                except Exception:
                    failed += 1
            except Exception:
                failed += 1

            try:
                await status_message.edit_text(
                    f"**Đang rời khỏi...**\n✅ Đã rời: `{left}`\n❌ Thất bại: `{failed}`"
                )
            except ChatWriteForbidden:
                pass
            await asyncio.sleep(1)
    except FloodWait as e:
        await asyncio.sleep(e.value)
    finally:
        try:
            await app.send_message(
                message.chat.id,
                f"**✅ Rời khỏi:** `{left}` nhóm.\n**❌ Thất bại tại:** `{failed}` nhóm.",
            )
        except ChatWriteForbidden:
            pass
