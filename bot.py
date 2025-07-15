from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os

BOT_TOKEN = "7924756576:AAG_9USm4BJXhSQrx_qiHjbecpw-Jd6VBVs"

user_steps = {}

# خطوات التعليمات
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
    await update.message.reply_text("📱 لنبدأ الإعدادات خطوة بخطوة.\nاضغط على الزر :", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.message.text == "➡️ التالي":
        step_index = user_steps.get(user_id, 0)
        if step_index < len(steps):
            # عرض الصورة فقط في الخطوة رقم 7 (index 6)
            if step_index == 6:
                image_path = "images/1.png"
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as photo:
                        await update.message.reply_photo(photo=photo)
            if step_index == 6:
                image_path = "images/2.png"
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as photo:
                        await update.message.reply_photo(photo=photo)

            # إرسال النص
            await update.message.reply_text(steps[step_index])
            user_steps[user_id] += 1
        else:
            await update.message.reply_text("✅ انتهينا من جميع الخطوات. إذا أردت البدء من جديد أرسل /start")
    else:
        await update.message.reply_text("❓ اكتب '➡️ التالي' أو أرسل /start للبدء من جديد.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

import asyncio

async def main():
    await app.initialize()
    await app.start()
    await app.bot.set_webhook("https://your-railway-app.up.railway.app")  # replace with your actual URL
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())