from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import random

# =========================
# LÓGICA DE GANANCIA (SIMULADA)
# =========================
def simular_ganancia(monto):
    if monto < 100:
        porcentaje = random.uniform(0.5, 2)
    elif monto < 1000:
        porcentaje = random.uniform(1, 4)
    else:
        porcentaje = random.uniform(2, 7)

    ganancia = monto * (porcentaje / 100)
    return porcentaje, ganancia

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard")],
        [InlineKeyboardButton("💼 Invertir", callback_data="invertir")]
    ]

    await update.message.reply_text(
        "💼 *FinBot Pro (Demo)*\n\n"
        "📈 Plataforma de inversión inteligente\n\n"
        "⚠️ Simulación visual, sin dinero real\n\n"
        "Selecciona una opción:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# =========================
# DASHBOARD
# =========================
async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    barras = "▰" * random.randint(4, 10) + "▱" * random.randint(1, 6)

    await query.edit_message_text(
        f"📊 *Dashboard en vivo*\n\n"
        f"BTC: {barras}\n"
        f"ETH: ▰▰▰▰▱▱▱▱▱▱\n"
        f"SP500: ▰▰▰▰▰▰▱▱▱▱\n\n"
        f"📡 Estado: Mercado activo\n"
        f"(Datos simulados)",
        parse_mode="Markdown"
    )

# =========================
# PEDIR MONTO
# =========================
async def invertir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "💼 *Invertir fondos*\n\n"
        "Ingresa el monto en USD:\n\n"
        "Ejemplo: 500",
        parse_mode="Markdown"
    )

    context.user_data["esperando_monto"] = True

# =========================
# PROCESAR MONTO
# =========================
async def procesar_monto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("esperando_monto"):
        return

    try:
        monto = float(update.message.text)

        porcentaje, ganancia = simular_ganancia(monto)

        estado = random.choice([
            "📈 Mercado en alza",
            "📉 Corrección leve",
            "⚖️ Mercado estable"
        ])

        await update.message.reply_text(
            f"⏳ Analizando mercado...\n"
            f"▰▰▰▰▰▱▱▱▱▱\n\n"
        )

        await update.message.reply_text(
            f"💼 *Resultado de inversión*\n\n"
            f"💰 Monto: ${monto}\n"
            f"{estado}\n"
            f"📈 Rendimiento: +{porcentaje:.2f}%\n"
            f"💵 Ganancia estimada: ${ganancia:.2f}\n\n"
            f"⚠️ Simulación (no real)",
            parse_mode="Markdown"
        )

        context.user_data["esperando_monto"] = False

    except:
        await update.message.reply_text("❌ Ingresa un número válido.")

# =========================
# BOTONES
# =========================
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "dashboard":
        await dashboard(update, context)

    elif query.data == "invertir":
        await invertir(update, context)

# =========================
# MAIN
# =========================
app = ApplicationBuilder().token("8283344299:AAHLeKmYviijZxV1EV4pi-I41QpjqtZE_xs").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(botones))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_monto))

print("Bot corriendo...")
app.run_polling()