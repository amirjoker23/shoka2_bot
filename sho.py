import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes

# متغیر محیطی توکن
TOKEN = "7666433350:AAEtnztPRm2s4olljqaOLiSl0Lyr08u9Y-o"

# مراحل گفتگو
(NAME, PHONE, NATIONAL_ID, MARITAL, ADDRESS, BIRTHDAY, JOB, POSTAL, BENEFICIARY_ID, BENEFICIARY_BIRTHDAY) = range(10)

# آیدی عددی ادمین
ADMIN_ID = 1571446410

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 به بیمه سرمایه‌گذاری شوکا خوش اومدین!\n\nبرای ثبت اطلاعات، لطفا سوالات بعدی رو پاسخ بدین."
    )
    await update.message.reply_text("👤 نام و نام خانوادگی شما؟")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['نام و نام خانوادگی'] = update.message.text
    await update.message.reply_text("📱 شماره تماس شما؟")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['شماره تماس'] = update.message.text
    await update.message.reply_text("🆔 کد ملی شما؟")
    return NATIONAL_ID

async def get_national_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['کد ملی'] = update.message.text
    keyboard = [['متاهل', 'مجرد']]
    await update.message.reply_text(
        "💍 وضعیت تاهل خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return MARITAL

async def get_marital(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['وضعیت تاهل'] = update.message.text
    await update.message.reply_text("🏠 آدرس محل سکونت شما؟")
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['آدرس'] = update.message.text
    await update.message.reply_text("📅 تاریخ تولد شما؟ (مثال: 1370/01/01)")
    return BIRTHDAY

async def get_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['تاریخ تولد'] = update.message.text
    await update.message.reply_text("💼 شغل شما چیست؟")
    return JOB

async def get_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['شغل'] = update.message.text
    await update.message.reply_text("🏷️ کد پستی شما؟")
    return POSTAL

async def get_postal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['کد پستی'] = update.message.text
    await update.message.reply_text("👥 کد ملی ذینفع در صورت فوت؟")
    return BENEFICIARY_ID

async def get_beneficiary_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['کد ملی ذینفع'] = update.message.text
    await update.message.reply_text("📅 تاریخ تولد ذینفع؟ (مثال: 1375/03/22)")
    return BENEFICIARY_BIRTHDAY

async def get_beneficiary_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['تاریخ تولد ذینفع'] = update.message.text

    keyboard = [['ماهانه', 'سالانه', 'یکجا']]
    await update.message.reply_text(
        "💳 کدام یک از طرح‌ها را انتخاب می‌کنید؟",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return PLAN_TYPE

    # ساخت خلاصه اطلاعات برای ادمین
    text = "📄 فرم جدید:\n\n"
    for key, value in context.user_data.items():
        text += f"{key}: {value}\n"

    await context.bot.send_message(chat_id=ADMIN_ID, text=text)

    await update.message.reply_text("✅ اطلاعات شما ثبت شد.\nبه زودی لینک پرداخت از طرف شرکت برای شما ارسال می‌شود.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            NATIONAL_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_national_id)],
            MARITAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_marital)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birthday)],
            JOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_job)],
            POSTAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_postal)],
            BENEFICIARY_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_beneficiary_id)],
            BENEFICIARY_BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_beneficiary_birthday)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
