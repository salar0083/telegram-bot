from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import nest_asyncio

nest_asyncio.apply()

TOKEN = "8047634329:AAFAmXX51JEVk64Mgc-LH-SONgFu6-W6avA"

CHANNELS = ["@marilyn_monsonn","@marilyn_monsonn_en","@marilyn_monsonn_farsi"]   # ← اینو با یوزرنیم واقعی کانالت عوض کن
CONTENT = [
    "https://cdn.cgmagonline.com/wp-content/uploads/2022/02/elden-ring-pc-review-2-1280x720.jpg",
    "https://cdn.cgmagonline.com/wp-content/uploads/2022/02/game-reviews-elden-ring-pc-review-768x432.jpg"
]  # لینک فایل‌ها

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # دکمه‌های عضویت بدون نمایش یوزرنیم کانال
    keyboard = [
        [InlineKeyboardButton(f"عضویت در کانال {i+1}", url=f"https://t.me/{channel.lstrip('@')}")]
        for i, channel in enumerate(CHANNELS)
    ]
    keyboard.append([InlineKeyboardButton("بررسی عضویت و دریافت محتوا", callback_data="check")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "برای دریافت محتوای ویژه، لطفاً در کانال‌های زیر عضو شو و سپس دکمهٔ بررسی رو بزن:",
        reply_markup=reply_markup
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.callback_query.from_user
    passed = True
    messages_to_delete = []

    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user.id)
            if member.status not in ["member", "administrator", "creator"]:
                passed = False
                break
        except:
            passed = False
            break

    if passed:
        await update.callback_query.message.reply_text("✅ عضویت تأیید شد! اینم محتوای ویژه شما 👇")
        for item in CONTENT:
            if item.endswith(".jpg") or item.endswith(".png"):
                msg = await context.bot.send_photo(chat_id=user.id, photo=item)
                messages_to_delete.append(msg.message_id)
            elif item.endswith(".mp4"):
                msg = await context.bot.send_video(chat_id=user.id, video=item)
                messages_to_delete.append(msg.message_id)
            else:
                msg = await context.bot.send_message(chat_id=user.id, text=item)
                messages_to_delete.append(msg.message_id)

        await asyncio.sleep(60)  # ۲ دقیقه صبر
        for msg_id in messages_to_delete:
            try:
                await context.bot.delete_message(chat_id=user.id, message_id=msg_id)
            except:
                pass
    else:
        await update.callback_query.message.reply_text("❌ هنوز در همه کانال‌ها عضو نشدی! لطفاً عضو شو و دوباره امتحان کن.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check, pattern="check"))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
