import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("8283344299:AAHLeKmYviijZxV1EV4pi-I41QpjqtZE_xs")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Recibí /start")
    await update.message.reply_text("✅ Bot funcionando en Render")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    print("Bot iniciado correctamente...")
    app.run_polling(drop_pending_updates=False)