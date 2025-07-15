from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import os
from aiohttp import web

BOT_TOKEN = "7924756576:AAG_9USm4BJXhSQrx_qiHjbecpw-Jd6VBVs"

user_steps = {}

# Instructions steps
steps = [
    "1️⃣ افتح إعدادات الهاتف.",
    "2️⃣ ابحث داخل الإعدادات عن كلمة: \"dns\".",
    "3️⃣ إذا لم تجد، ابحث عن كلمة: \"نطاق\".",
    "4️⃣ اختر الخيار الثالث.",
    "5️⃣ اكتب فيه: family-filter-dns.cleanbrowsing.org",
    "6️⃣ احفظ الإعدادات.",
    "🧪 الآن لاختبار النجاح:\nافتح الرابط https://dnsleaktest.com/\nثم اضغط على زر الاختبار وتأكد أن النتائج تظهر dns-edge"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_steps[user_id] = 0
    keyboard = [["➡️ التالي"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "📱 لنبدأ الإعدادات خطوة بخطوة.\nاضغط على الزر :", reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.message.text == "➡️ التالي":
        step_index = user_steps.get(user_id, 0)
        if step_index < len(steps):
            # Show images only at step 7
            if step_index == 6:
                for img in ["images/1.png", "images/2.png"]:
                    if os.path.exists(img):
                        with open(img, "rb") as photo:
                            await update.message.reply_photo(photo=photo)
            # Send text
            await update.message.reply_text(steps[step_index])
            user_steps[user_id] += 1
        else:
            await update.message.reply_text("✅ انتهينا من جميع الخطوات. إذا أردت البدء من جديد أرسل /start")
    else:
        await update.message.reply_text("❓ اكتب '➡️ التالي' أو أرسل /start للبدء من جديد.")

# Build bot application
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handlers once
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Webhook handler
async def handle(request):
    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return web.Response(text="OK")

# Run aiohttp web server
async def main():
    aio_app = web.Application()
    aio_app.router.add_post("/", handle)
    runner = web.AppRunner(aio_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await app.initialize()
    await app.start()
    await app.bot.set_webhook("https://your-app.up.railway.app")  # Replace with your real Railway URL
    await site.start()
    print("🚀 Bot is live on Railway and webhook is set")
    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
