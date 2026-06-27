import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from rgbrain import RGBrain


# ============================
# API KEYS
# ============================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

brain = RGBrain()


# ============================
# START COMMAND
# ============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 أهلاً بك في RG AI\n\n"
        "أنا مساعدك في التأجير اليومي للشقق الخاصة.\n"
        "اسألني أي سؤال وسأجيبك من دليل RG AI."
    )


# ============================
# CHAT
# ============================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    try:

        result = brain.answer(user_message)

        if result["status"] == "FOUND":

            text = result["answer"]

        else:

            text = (
                "❌ لم أجد إجابة لهذا السؤال داخل دليل RG AI.\n\n"
                "إذا كنت تحتاج استشارة خاصة، تواصل مع فهد مباشرة."
            )

        for i in range(0, len(text), 4000):
            await update.message.reply_text(text[i:i + 4000])

    except Exception as e:

        print(e)

        await update.message.reply_text(
            f"حدث خطأ:\n{e}"
        )


# ============================
# RUN BOT
# ============================

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
)

print("RG AI Started...")

app.run_polling()
