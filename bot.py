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
from database import db

# ============================
# API KEYS
# ============================

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

brain = RGBrain()

# ============================
# START COMMAND
# ============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram_id = update.effective_user.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name

    user = db.create_user(telegram_id, username, first_name)
    db.update_last_seen(telegram_id)

    if user["is_active"]:
        await update.message.reply_text(
            "👋 أهلاً بعودتك في RG AI\n\n"
            "اسألني أي سؤال وسأجيبك من دليل RG AI."
        )
        context.user_data["awaiting_code"] = False
        return

    context.user_data["awaiting_code"] = True

    await update.message.reply_text(
        "👋 أهلاً بك في RG AI\n\n"
        "أنا مساعدك في التأجير اليومي للشقق الخاصة.\n\n"
        "أرسل كود التفعيل الخاص بك للبدء 🔑"
    )

# ============================
# CHAT / ACTIVATION
# ============================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    telegram_id = update.effective_user.id
    user_message = update.message.text.strip()

    db.update_last_seen(telegram_id)

    user = db.get_user(telegram_id)

    if user is None:
        # user never pressed /start
        await update.message.reply_text(
            "من فضلك ابدأ بالأمر /start أولاً."
        )
        return

    # -------- Case 1: waiting for activation code --------
    if context.user_data.get("awaiting_code") or not user["is_active"]:

        result = db.verify_code(user_message)

        if not result["success"]:
            await update.message.reply_text(
                f"❌ {result['message']}\n\nحاول مرة أخرى، أو تواصل مع فهد إذا واجهت مشكلة."
            )
            return

        subscription_type = result["data"]["subscription_type"]

        db.use_code(user_message, telegram_id)
        db.activate_user(telegram_id, user_message, subscription_type)

        context.user_data["awaiting_code"] = False

        await update.message.reply_text(
            "✅ تم تفعيل اشتراكك بنجاح!\n\n"
            "اسألني الآن أي سؤال عن التأجير اليومي، "
            "وتذكر أن مدة الدعم المجاني تبدأ من أول سؤال ترسله (7 أيام)."
        )
        return

    # -------- Case 2: active user asking a question --------
    if not db.is_subscription_valid(telegram_id):
        await update.message.reply_text(
            "⏳ انتهت مدة الاستشارة المجانية الخاصة بك.\n\n"
            "للتجديد أو الحصول على استشارة خاصة، تواصل مع فهد مباشرة."
        )
        return

    try:

        result = brain.answer(user_message)

        if result["status"] == "FOUND":
            text = result["answer"]
        else:
            text = (
                "❌ لم أجد إجابة لهذا السؤال داخل دليل RG AI.\n\n"
                "إذا كنت تحتاج استشارة خاصة، تواصل مع فهد مباشرة."
            )

        db.save_consultation(telegram_id, user_message)

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
