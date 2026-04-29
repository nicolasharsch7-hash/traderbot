import random
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from db import *

TOKEN = "8283344299:AAHLeKmYviijZxV1EV4pi-I41QpjqtZE_xs"

def trade(user_id):
    profit = round(random.uniform(5, 3276), 2)
    win = random.choice([True, False])

    if win:
        update_balance(user_id, profit)
    else:
        update_balance(user_id, -profit * 0.3)

    return win, profit

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    get_user(user_id)

    await update.message.reply_text("💎 QuantumTrade Demo\nUsa /panel")

async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    await update.message.reply_text(f"""
💰 Balance: ${user[2]:,.2f}
📈 Profit total: ${user[3]:,.2f}

Panel web:
http://localhost:10000
""")

async def trade_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    win, profit = trade(user_id)

    await update.message.reply_text(f"""
📊 Trade ejecutado

Resultado: {"WIN ✅" if win else "LOSS ❌"}
💰 Profit: ${profit}
🕒 {datetime.datetime.now().strftime("%H:%M:%S")}
""")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("panel", panel))
app.add_handler(CommandHandler("trade", trade_cmd))

print("Bot corriendo...")
app.run_polling()
