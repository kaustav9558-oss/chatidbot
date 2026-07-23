
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Fetch bot token from environment variable
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message and the main menu with buttons."""
    keyboard = [
        [InlineKeyboardButton("Select Users", callback_data="select_users"),
         InlineKeyboardButton("Select Bots", callback_data="select_bots")],
        [InlineKeyboardButton("Select Channels", callback_data="select_channels")],
        [InlineKeyboardButton("Private Channels", callback_data="private_channels"),
         InlineKeyboardButton("Public Channels", callback_data="public_channels")],
        [InlineKeyboardButton("Select Groups", callback_data="select_groups")],
        [InlineKeyboardButton("Private Groups", callback_data="private_groups"),
         InlineKeyboardButton("Public Groups", callback_data="public_groups")],
        [InlineKeyboardButton("Select Premium Users", callback_data="select_premium_users")],
        [InlineKeyboardButton("Premium Users", callback_data="premium_users")],
        [InlineKeyboardButton("Admin Groups", callback_data="admin_groups"),
         InlineKeyboardButton("Admin Channels", callback_data="admin_channels")],
        [InlineKeyboardButton("Admin Private Groups", callback_data="admin_private_groups"),
         InlineKeyboardButton("Admin Public Groups", callback_data="admin_public_groups")],
        [InlineKeyboardButton("Admin Private Channels", callback_data="admin_private_channels"),
         InlineKeyboardButton("Admin Public Channels", callback_data="admin_public_channels")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "👋 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴄʜᴀᴛ ɪᴅ ɪɴꜰᴏ ʙᴏᴛ!\n\n"
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

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the command /help is issued."""
    await update.message.reply_text("Use /start to see the main menu.")

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echoes the user's chat ID."""
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your Chat ID is: {chat_id}")

def main() -> None:
    """Start the bot."""
    if not TOKEN:
        logger.error("No BOT_TOKEN environment variable found.")
        return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("id", get_chat_id))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
