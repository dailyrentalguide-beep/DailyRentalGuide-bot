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

# ============================
# API KEYS
# ============================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# ============================
# START COMMAND
# ============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك في RG AI\n\n"
        "أنا مساعدك في التأجير اليومي للشقق الخاصة.\n"
        "اسألني أي سؤال وسأجيبك مباشرة."
    )

# ============================
# CHAT
# ============================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = model.generate_content(
            f"""
أنت خبير في:
- Airbnb
- التأجير اليومي
- إدارة الشقق
- التسويق
- التسعير
- زيادة الأرباح

أجب باللغة العربية.
اجعل الإجابة واضحة ومختصرة.

سؤال المستخدم:
{user_message}
"""
        )

        text = response.text

        for i in range(0, len(text), 4000):
            await update.message.reply_text(text[i:i+4000])

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

print("Bot Started...")

app.run_polling()
