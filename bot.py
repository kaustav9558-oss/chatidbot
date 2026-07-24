
import os
import logging
from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    KeyboardButtonRequestUsers, 
    KeyboardButtonRequestChat,
    ChatAdministratorRights
)
from telegram.ext import (
    Application, 
    CommandHandler, 
    ContextTypes, 
    MessageHandler, 
    filters
)
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Fetch bot token from environment variable
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message and the main menu with native picker buttons."""
    
    # Define the keyboard with native request buttons
    # Note: user_privileges uses ChatAdministratorRights in PTB
    keyboard = [
        [
            KeyboardButton("Select Users", request_users=KeyboardButtonRequestUsers(request_id=1, user_is_bot=False)),
            KeyboardButton("Select Bots", request_users=KeyboardButtonRequestUsers(request_id=2, user_is_bot=True))
        ],
        [
            KeyboardButton("Select Channels", request_chat=KeyboardButtonRequestChat(request_id=3, chat_is_channel=True))
        ],
        [
            KeyboardButton("Private Channels", request_chat=KeyboardButtonRequestChat(request_id=4, chat_is_channel=True, chat_has_username=False)),
            KeyboardButton("Public Channels", request_chat=KeyboardButtonRequestChat(request_id=5, chat_is_channel=True, chat_has_username=True))
        ],
        [
            KeyboardButton("Select Groups", request_chat=KeyboardButtonRequestChat(request_id=6, chat_is_channel=False))
        ],
        [
            KeyboardButton("Private Groups", request_chat=KeyboardButtonRequestChat(request_id=7, chat_is_channel=False, chat_has_username=False)),
            KeyboardButton("Public Groups", request_chat=KeyboardButtonRequestChat(request_id=8, chat_is_channel=False, chat_has_username=True))
        ],
        [
            KeyboardButton("Select Premium Users", request_users=KeyboardButtonRequestUsers(request_id=9, user_is_premium=True)),
            KeyboardButton("Premium Users", request_users=KeyboardButtonRequestUsers(request_id=12, user_is_premium=True))
        ],
        [
            KeyboardButton("Admin Groups", request_chat=KeyboardButtonRequestChat(request_id=10, chat_is_channel=False, user_administrator_rights=ChatAdministratorRights.all_rights())),
            KeyboardButton("Admin Channels", request_chat=KeyboardButtonRequestChat(request_id=11, chat_is_channel=True, user_administrator_rights=ChatAdministratorRights.all_rights()))
        ],
        [
            KeyboardButton("Admin Private Groups", request_chat=KeyboardButtonRequestChat(request_id=13, chat_is_channel=False, chat_has_username=False, user_administrator_rights=ChatAdministratorRights.all_rights())),
            KeyboardButton("Admin Public Groups", request_chat=KeyboardButtonRequestChat(request_id=14, chat_is_channel=False, chat_has_username=True, user_administrator_rights=ChatAdministratorRights.all_rights()))
        ],
        [
            KeyboardButton("Admin Private Channels", request_chat=KeyboardButtonRequestChat(request_id=15, chat_is_channel=True, chat_has_username=False, user_administrator_rights=ChatAdministratorRights.all_rights())),
            KeyboardButton("Admin Public Channels", request_chat=KeyboardButtonRequestChat(request_id=16, chat_is_channel=True, chat_has_username=True, user_administrator_rights=ChatAdministratorRights.all_rights()))
        ]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = (
        "👋 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴄʜᴀᴛ ɪɴꜰᴏ ʙᴏᴛ!\n\n"
        "ᴛʜɪꜱ ʙᴏᴛ ʟᴇᴛꜱ ʏᴏᴜ ꜰᴇᴛᴄʜ ᴛʜᴇ ɪᴅ, ᴜꜱᴇʀɴᴀᴍᴇ, ɴᴀᴍᴇ ᴀɴᴅ ᴛʏᴘᴇ ᴏꜰ ᴀɴʏ ᴜꜱᴇʀ, ʙᴏᴛ, ɢʀᴏᴜᴘ ᴏʀ ᴄʜᴀɴɴᴇʟ — ɴᴏ ᴍᴀᴛᴛᴇʀ ᴛʜᴇɪʀ ᴘʀɪᴠᴀᴄʏ ꜱᴇᴛᴛɪɴɢꜱ.\n\n"
        "📖 ʜᴏᴡ ᴛᴏ ᴜꜱᴇ\n\n"
        "👤 ꜱᴇʟᴇᴄᴛ ᴜꜱᴇʀꜱ — ɢᴇᴛ ɪᴅ ᴀɴᴅ ᴜꜱᴇʀɴᴀᴍᴇ ᴏꜰ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴜꜱᴇʀ\n"
        "🤖 ꜱᴇʟᴇᴄᴛ ʙᴏᴛꜱ — ɢᴇᴛ ɪᴅ ᴀɴᴅ ᴜꜱᴇʀɴᴀᴍᴇ ᴏꜰ ᴀɴʏ ʙᴏᴛ\n"
        "📢 ꜱᴇʟᴇᴄᴛ ᴄʜᴀɴɴᴇʟꜱ — ɢᴇᴛ ɪᴅ ᴏꜰ ᴀɴʏ ᴄʜᴀɴɴᴇʟ\n"
        "🔒 ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟꜱ — ᴏɴʟʏ ᴄʜᴀɴɴᴇʟꜱ ᴡɪᴛʜᴏᴜᴛ ᴀ ᴘᴜʙʟɪᴄ ᴜꜱᴇʀɴᴀᴍᴇ\n"
        "🌐 ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟꜱ — ᴏɴʟʏ ᴄʜᴀɴɴᴇʟꜱ ᴡɪᴛʜ ᴀ ᴘᴜʙʟɪᴄ ᴜꜱᴇʀɴᴀᴍᴇ\n"
        "👥 ꜱᴇʟᴇᴄᴛ ɢʀᴏᴜᴘꜱ — ɢᴇᴛ ɪᴅ ᴏꜰ ᴀɴʏ ɢʀᴏᴜᴘ\n"
        "🔒 ᴘʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴘꜱ — ᴏɴʟʏ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜᴏᴜᴛ ᴀ ᴘᴜʙʟɪᴄ ᴜꜱᴇʀɴᴀᴍᴇ\n"
        "🌐 ᴘᴜʙʟɪᴄ ɢʀᴏᴜᴘꜱ — ᴏɴʟʏ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜ ᴀ ᴘᴜʙʟɪᴄ ᴜꜱᴇʀɴᴀᴍᴇ\n"
        "💎 ꜱᴇʟᴇᴄᴛ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ — ᴏɴʟʏ ᴛᴇʟᴇɢʀᴀᴍ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ\n"
        "💎 ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ — ꜰᴇᴛᴄʜ ɪɴꜰᴏ ꜰᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ ᴏɴʟʏ\n"
        "🛡 ᴀᴅᴍɪɴ ɢʀᴏᴜᴘꜱ — ɢʀᴏᴜᴘꜱ ᴡʜᴇʀᴇ ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀᴅᴍɪɴ\n"
        "🛡 ᴀᴅᴍɪɴ ᴄʜᴀɴɴᴇʟꜱ — ᴄʜᴀɴɴᴇʟꜱ ᴡʜᴇʀᴇ ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀᴅᴍɪɴ\n"
        "🔒 ᴀᴅᴍɪɴ ᴘʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴘꜱ — ᴘʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴘꜱ ᴡʜᴇʀᴇ ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀᴅᴍɪɴ\n"
        "🌐 ᴀᴅᴍɪɴ ᴘᴜʙʟɪᴄ ɢʀᴏᴜᴘꜱ — ᴘᴜʙʟɪᴄ ɢʀᴏᴜᴘꜱ ᴡʜᴇʀᴇ ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀᴅᴍɪɴ\n"
        "🔒 ᴀᴅᴍɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟꜱ — ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟꜱ ᴡʜᴇʀᴇ ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀᴅᴍɪɴ\n"
        "🌐 ᴀᴅᴍɪɴ ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟꜱ — ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟꜱ ᴡʜᴇʀᴇ ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀᴅᴍɪɴ\n\n"
        "👇 ᴊᴜꜱᴛ ᴛᴀᴘ ᴀ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ, ᴘɪᴄᴋ ꜰʀᴏᴍ ᴛʜᴇ ɴᴀᴛɪᴠᴇ ᴛᴇʟᴇɢʀᴀᴍ ʟɪꜱᴛ, ᴀɴᴅ ᴛʜᴇ ᴅᴇᴛᴀɪʟꜱ ᴡɪʟʟ ʙᴇ ꜱᴇɴᴛ ɪɴꜱᴛᴀɴᴛʟʏ"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def on_user_shared(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the result when a user is shared."""
    user_ids = update.message.users_shared.user_ids
    await update.message.reply_text(
        f"✅ **User Details Fetched!**\n\n"
        f"🆔 **ID:** `{user_ids[0]}`\n"
        f"👤 **Type:** User/Bot",
        parse_mode="Markdown"
    )

async def on_chat_shared(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the result when a chat (group/channel) is shared."""
    chat_id = update.message.chat_shared.chat_id
    await update.message.reply_text(
        f"✅ **Chat Details Fetched!**\n\n"
        f"🆔 **ID:** `{chat_id}`\n"
        f"📢 **Type:** Group/Channel",
        parse_mode="Markdown"
    )

def main() -> None:
    """Start the bot."""
    if not TOKEN:
        logger.error("No BOT_TOKEN environment variable found.")
        return

    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.USERS_SHARED, on_user_shared))
    application.add_handler(MessageHandler(filters.StatusUpdate.CHAT_SHARED, on_chat_shared))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
