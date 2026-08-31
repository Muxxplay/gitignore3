import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# .env faylidagi o'zgaruvchilarni yuklash
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! 💵 Valyuta kurslarini bilish uchun /kurs buyrug'ini yuboring."
    )

async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ochiq va bepul valyuta API'si
    url = "https://open.er-api.com/v6/latest/USD"
    
    try:
        response = requests.get(url).json()
        if response.get("result") == "success":
            uzs = response["rates"]["UZS"]
            eur_in_usd = response["rates"]["EUR"]
            eur_in_uzs = uzs / eur_in_usd

            text = (
                "💵 **Bugungi valyuta kursi:**\n\n"
                f"🇺🇸 1 USD = {uzs:,.2f} UZS\n"
                f"🇪🇺 1 EUR = {eur_in_uzs:,.2f} UZS"
            )
        else:
            text = "⚠️ Ma'lumotlarni olishda xatolik yuz berdi."
    except Exception:
        text = "❌ Serverga ulanib bo'lmadi."

    await update.message.reply_text(text)

if __name__ == "__main__":
    if not TOKEN:
        print("Xatolik: BOT_TOKEN topilmadi! .env faylini tekshiring.")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("kurs", rate))
    
    print("Valyuta boti ishga tushdi...")
    app.run_polling()