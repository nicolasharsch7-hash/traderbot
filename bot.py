import random
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8283344299:AAHLeKmYviijZxV1EV4pi-I41QpjqtZE_xs"

# -------- DATOS EN MEMORIA --------
usuarios = {}

def get_user(user_id):
    if user_id not in usuarios:
        usuarios[user_id] = {
            "balance": round(random.uniform(1000, 5000), 2),
            "profit_total": 0
        }
    return usuarios[user_id]

# -------- COMANDOS --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    await update.message.reply_text(f"""
💎 *QuantumTrade Demo*

⚠️ Inversiones Automatizadas con IA

💰 Balance inicial: ${user["balance"]}

Usa:
/panel - ver dashboard
/trade - ejecutar trade
/grafico - ver mercado
""", parse_mode="Markdown")


async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    await update.message.reply_text(f"""
📊 *Dashboard*

💰 Balance: ${user["balance"]:,.2f}
📈 Ganancia total: ${user["profit_total"]:,.2f}

🤖 Estado: Activo
""", parse_mode="Markdown")


async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    profit = round(random.uniform(5, 500), 2)
    win = random.choice([True, False])

    if win:
        user["balance"] += profit
        user["profit_total"] += profit
    else:
        user["balance"] -= profit * 0.3

    await update.message.reply_text(f"""
📊 *Trade ejecutado*

Resultado: {"WIN ✅" if win else "LOSS ❌"}
💰 Resultado: ${profit}

🕒 {datetime.datetime.now().strftime("%H:%M:%S")}
""", parse_mode="Markdown")


async def grafico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
📈 *Gráfico en vivo*

https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT

(Visualización real del mercado)
""", parse_mode="Markdown")


# -------- MAIN --------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("panel", panel))
app.add_handler(CommandHandler("trade", trade))
app.add_handler(CommandHandler("grafico", grafico))

print("🚀 Bot funcionando...")
app.run_polling()