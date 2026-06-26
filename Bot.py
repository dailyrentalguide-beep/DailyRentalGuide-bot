import os
import google.generativeai as genai

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ==========================
# API KEYS
# ==========================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# ==========================
# /start
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك في RG AI\n\n"
        "اكتب أي سؤال عن التأجير اليومي وسأجيبك مباشرة."
    )


# ==========================
# Chat
# ==========================
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = model.generate_content(user_message)

text = response.text

response = model.generate_content(
    f"أجب باختصار وبحد أقصى 500 كلمة:\n\n{user_message}"
)

    except Exception as e:
        print(e)
        await update.message.reply_text(
            "حدث خطأ، حاول مرة أخرى."
        )


# ==========================
# RUN BOT
# ==========================
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)

print("Bot Started...")

app.run_polling()
