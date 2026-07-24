import os
import logging
import asyncio
import threading
from flask import Flask
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
    filters,
    Defaults
)
from telegram.constants import ParseMode
from telegram.error import TelegramError, Conflict, TimedOut, NetworkError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Developer Credit
DEVELOPER_CREDIT = "ᴅᴇᴠᴇʟᴏᴘᴇʀ :- [ᴋᴀᴜꜱᴛᴀᴠ ᴋᴀɴᴛɪ ʀᴀʏ @ɪᴀᴍᴋᴋʀᴏɴʟʏ](https://t.me/iamkkronly)"
ERROR_FOOTER = f"\n\n⚠️ ɪꜰ ᴛʜɪꜱ ᴇʀʀᴏʀ ᴘᴇʀꜱɪꜱᴛꜱ, ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ {DEVELOPER_CREDIT}"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Fetch bot token
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8080))

# Web Server for UptimeRobot
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!", 200

def run_web_server():
    app.run(host='0.0.0.0', port=PORT)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message and the main menu with native picker buttons."""
    try:
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
            ],
            [
                KeyboardButton("Owned Private Groups", request_chat=KeyboardButtonRequestChat(request_id=17, chat_is_channel=False, chat_has_username=False, chat_is_created=True)),
                KeyboardButton("Owned Public Groups", request_chat=KeyboardButtonRequestChat(request_id=18, chat_is_channel=False, chat_has_username=True, chat_is_created=True))
            ],
            [
                KeyboardButton("Owned Private Channels", request_chat=KeyboardButtonRequestChat(request_id=19, chat_is_channel=True, chat_has_username=False, chat_is_created=True)),
                KeyboardButton("Owned Public Channels", request_chat=KeyboardButtonRequestChat(request_id=20, chat_is_channel=True, chat_has_username=True, chat_is_created=True))
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
            "🌐 ᴀᴅᴍɪɴ ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟꜱ — ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟꜱ ᴡʜᴇʀᴇ ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀᴅᴍɪɴ\n"
            "🏠 ᴏᴡɴᴇᴅ ᴘʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴘꜱ — ɢʀᴏᴜᴘꜱ ʏᴏᴜ ᴏᴡɴ ᴡɪᴛʜᴏᴜᴛ ᴀ ᴜꜱᴇʀɴᴀᴍᴇ\n"
"🌐 ᴏᴡɴᴇᴅ ᴘᴜʙʟɪᴄ ɢʀᴏᴜᴘꜱ — ɢʀᴏᴜᴘꜱ ʏᴏᴜ ᴏᴡɴ ᴡɪᴛʜ ᴀ ᴜꜱᴇʀɴᴀᴍᴇ\n"
"🏠 ᴏᴡɴᴇᴅ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟꜱ — ᴄʜᴀɴɴᴇʟꜱ ʏᴏᴜ ᴏᴡɴ ᴡɪᴛʜᴏᴜᴛ ᴀ ᴜꜱᴇʀɴᴀᴍᴇ\n"
"🌐 ᴏᴡɴᴇᴅ ᴘᴜʙʟɪᴄ ᴄʜᴀɴɴᴇʟꜱ — ᴄʜᴀɴɴᴇʟꜱ ʏᴏᴜ ᴏᴡɴ ᴡɪᴛʜ ᴀ ᴜꜱᴇʀɴᴀᴍᴇ\n\n"
            "👇 ᴊᴜꜱᴛ ᴛᴀᴘ ᴀ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ, ᴘɪᴄᴋ ꜰʀᴏᴍ ᴛʜᴇ ɴᴀᴛɪᴠᴇ ᴛᴇʟᴇɢʀᴀᴍ ʟɪꜱᴛ, ᴀɴᴅ ᴛʜᴇ ᴅᴇᴛᴀɪʟꜱ ᴡɪʟʟ ʙᴇ ꜱᴇɴᴛ ɪɴꜱᴛᴀɴᴛʟʏ\n\n"
            f"{DEVELOPER_CREDIT}"
        )
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text(f"❌ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇꜱꜱɪɴɢ ʏᴏᴜʀ ʀᴇQᴜᴇꜱᴛ.{ERROR_FOOTER}", parse_mode=ParseMode.MARKDOWN)

async def on_user_shared(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the result when a user is shared."""
    try:
        user_ids = update.message.users_shared.user_ids
        await update.message.reply_text(
            f"✅ **ᴜꜱᴇʀ ᴅᴇᴛᴀɪʟꜱ ꜰᴇᴛᴄʜᴇᴅ!**\n\n"
            f"🆔 **ɪᴅ:** `{user_ids[0]}`\n"
            f"👤 **ᴛʏᴘᴇ:** ᴜꜱᴇʀ/ʙᴏᴛ\n\n"
            f"{DEVELOPER_CREDIT}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Error in on_user_shared: {e}")
        await update.message.reply_text(f"❌ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ꜰᴇᴛᴄʜɪɴɢ ᴜꜱᴇʀ ᴅᴇᴛᴀɪʟꜱ.{ERROR_FOOTER}", parse_mode=ParseMode.MARKDOWN)

async def on_chat_shared(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the result when a chat (group/channel) is shared."""
    try:
        chat_id = update.message.chat_shared.chat_id
        await update.message.reply_text(
            f"✅ **ᴄʜᴀᴛ ᴅᴇᴛᴀɪʟꜱ ꜰᴇᴛᴄʜᴇᴅ!**\n\n"
            f"🆔 **ɪᴅ:** `{chat_id}`\n"
            f"📢 **ᴛʏᴘᴇ:** ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ\n\n"
            f"{DEVELOPER_CREDIT}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Error in on_chat_shared: {e}")
        await update.message.reply_text(f"❌ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ꜰᴇᴛᴄʜɪɴɢ ᴄʜᴀᴛ ᴅᴇᴛᴀɪʟꜱ.{ERROR_FOOTER}", parse_mode=ParseMode.MARKDOWN)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to the user."""
    logger.error(f"Exception while handling an update: {context.error}")
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            f"❌ ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ! ᴛʜᴇ ʙᴏᴛ ᴇɴᴄᴏᴜɴᴛᴇʀᴇᴅ ᴀɴ ᴜɴᴇxᴘᴇᴄᴛᴇᴅ ɪꜱꜱᴜᴇ.{ERROR_FOOTER}",
            parse_mode=ParseMode.MARKDOWN
        )

def main() -> None:
    """Start the bot."""
    if not TOKEN:
        logger.error("No BOT_TOKEN environment variable found.")
        return

    # Start web server in a separate thread
    threading.Thread(target=run_web_server, daemon=True).start()

    # Performance Optimizations:
    # 1. Increase concurrent updates handling
    # 2. Use a high number of workers for background tasks
    # 3. Configure request parameters for speed
    defaults = Defaults(parse_mode=ParseMode.MARKDOWN)
    
    application = (
        Application.builder()
        .token(TOKEN)
        .defaults(defaults)
        .concurrent_updates(True) # Handle multiple users at once
        .read_timeout(7)
        .connect_timeout(7)
        .pool_timeout(7)
        .write_timeout(7)
        .get_updates_read_timeout(42)
        .build()
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.USERS_SHARED, on_user_shared))
    application.add_handler(MessageHandler(filters.StatusUpdate.CHAT_SHARED, on_chat_shared))
    
    # Global error handler
    application.add_error_handler(error_handler)

    # Run the bot with high worker count
    # Workers handle the background processing of updates
    logger.info(f"Starting bot on port {PORT} with high performance settings...")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        close_loop=False
    )

if __name__ == "__main__":
    main()
