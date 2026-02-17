from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8548299975:AAHJcGcDIzbvj8u4A5p3xL8hsEc9vxmHHhc"
OWNER_ID = 7659864091  # Apna Telegram numeric ID daalo

TERMS_MESSAGE = """Hey, Please state the terms of the deal.

• What is the deal?
• Who is the buyer/seller?
• What is the agreed price?
• Any conditions like when to release or when to refund?"""

COMPLETE_MESSAGE = """Thank you for using my Middleman service 🤝🏻

Please leave me a vouch here
@middIemem in the comment section."""

def owner_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != OWNER_ID:
            return
        return await func(update, context)
    return wrapper

@owner_only
async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    # Change Group Name
    await chat.set_title("Ziox MM | @middlemem")

    # Set Group Profile Photo
    try:
        with open("pfp.jpg", "rb") as photo:
            await chat.set_photo(photo)
    except:
        pass

    # Send & Pin Terms Message
    msg = await update.message.reply_text(TERMS_MESSAGE)
    await msg.pin()

@owner_only
async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    await chat.set_title("Ziox MM | @Completed")

    await chat.set_permissions(
        ChatPermissions(can_send_messages=False)
    )

@owner_only
async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    await chat.set_permissions(
        ChatPermissions(can_send_messages=True)
    )

@owner_only
async def complete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(COMPLETE_MESSAGE)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("setup", setup))
app.add_handler(CommandHandler("lock", lock))
app.add_handler(CommandHandler("unlock", unlock))
app.add_handler(CommandHandler("complete", complete))

app.run_polling()