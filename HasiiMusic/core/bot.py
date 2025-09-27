import sys
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import config
from ..logging import LOGGER


class JARVIS(Client):
    def __init__(self):
        super().__init__(
            name="AnnieXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            workers=48,
            max_concurrent_transmissions=7,
        )
        LOGGER(__name__).info("Bot client đã được khởi tạo ✅.")

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username, self.id = me.username, me.id
        self.name = f"{me.first_name} {me.last_name or ''}".strip()
        self.mention = me.mention

        try:
            await self.send_message(
                config.LOGGER_ID,
                (
                    f"<u><b>» {self.mention} bot đã khởi động :</b></u>\n\n"
f"id : <code>{self.id}</code>\n"
f"tên : {self.name}\n"
f"username : @{self.username}"
                ),
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error("❌ Bot không thể truy cập nhóm/kênh log – hãy thêm bot vào và nâng quyền trước!")
            sys.exit()
        except Exception as exc:
            LOGGER(__name__).error(f"❌ Bot đã không thể truy cập nhóm log.\nLý do: {type(exc).__name__}")
            sys.exit()

        try:
            member = await self.get_chat_member(config.LOGGER_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("❌ Thăng cấp bot làm quản trị viên trong nhóm/kênh log.")
                sys.exit()
        except Exception as e:
            LOGGER(__name__).error(f"❌ Không thể kiểm tra trạng thái quản trị viên: {e}")
            sys.exit()

        LOGGER(__name__).info(f"✅ Music Bot đã khởi động là {self.name} (@{self.username})")
