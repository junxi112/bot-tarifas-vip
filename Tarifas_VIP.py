from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, ConversationHandler, CallbackQueryHandler
)
import math

# 🔐 Token del bot
TOKEN = '8209882179:AAGopCA-7it_F75URLSKg9AaFGX7FlgQN0E'

# 🎯 Estados del flujo
PERSONAS, ACCESOS = range(2)

# 📊 Diccionario de precios (personas, accesos_por_persona): precio_total
precio_dict = {
    (1, 1): 45, (1, 2): 60, (1, 3): 80, (1, 4): 100, (1, 5): 120, (1, 6): 140, (1, 7): 160, (1, 8): 180, (1, 9): 200, (1, 10): 220,
    (2, 1): 45, (2, 2): 60, (2, 3): 80, (2, 4): 100, (2, 5): 120, (2, 6): 140, (2, 7): 160, (2, 8): 180, (2, 9): 200, (2, 10): 220,
    (3, 1): 90, (3, 2): 120, (3, 3): 160, (3, 4): 200, (3, 5): 240, (3, 6): 280, (3, 7): 320, (3, 8): 360, (3, 9): 400, (3, 10): 440,
    (4, 1): 90, (4, 2): 120, (4, 3): 160, (4, 4): 200, (4, 5): 240, (4, 6): 280, (4, 7): 320, (4, 8): 360, (4, 9): 400, (4, 10): 440,
    (5, 1): 135, (5, 2): 180, (5, 3): 240, (5, 4): 300, (5, 5): 360, (5, 6): 420, (5, 7): 480, (5, 8): 540, (5, 9): 600, (5, 10): 660,
    (6, 1): 135, (6, 2): 180, (6, 3): 240, (6, 4): 300, (6, 5): 360, (6, 6): 420, (6, 7): 480, (6, 8): 540, (6, 9): 600, (6, 10): 660,
    (7, 1): 180, (7, 2): 240, (7, 3): 320, (7, 4): 400, (7, 5): 480, (7, 6): 560, (7, 7): 640, (7, 8): 720, (7, 9): 800, (7, 10): 880,
    (8, 1): 180, (8, 2): 240, (8, 3): 320, (8, 4): 400, (8, 5): 480, (8, 6): 560, (8, 7): 640, (8, 8): 720, (8, 9): 800, (8, 10): 880,
    (9, 1): 225, (9, 2): 300, (9, 3): 400, (9, 4): 500, (9, 5): 600, (9, 6): 700, (9, 7): 800, (9, 8): 900, (9, 9): 1000, (9, 10): 1100,
    (10, 1): 225, (10, 2): 300, (10, 3): 400, (10, 4): 500, (10, 5): 600, (10, 6): 700, (10, 7): 800, (10, 8): 900, (10, 9): 1000, (10, 10): 1100
}

# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! Vamos a calcular el precio de tus accesos a salas VIP.\n\n"
        "👉 ¿Cuántas personas sois? (máx. 10)"
    )
    return PERSONAS

# 👥 Recoger número de personas
async def personas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        num = int(update.message.text)
        if num <= 0 or num > 10:
            raise ValueError
        context.user_data["personas"] = num
        await update.message.reply_text(
            "✅ Perfecto. ¿Cuántos accesos necesita cada persona?\n\n"
            "🔸 *Un acceso = entrada a una sala VIP distinta (ej. ida y vuelta = 2).*",
            parse_mode="Markdown"
        )
        return ACCESOS
    except:
        await update.message.reply_text("❗ Escribe un número válido de personas (entre 1 y 10).")
        return PERSONAS

# 🔁 Calcular precio
async def accesos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        accesos = int(update.message.text)
        personas = context.user_data["personas"]
        if accesos <= 0 or accesos > 10:
            raise ValueError

        clave = (personas, accesos)
        if clave not in precio_dict:
            await update.message.reply_text("❗ Esa combinación no está disponible.")
            return ConversationHandler.END

        precio_total = precio_dict[clave]
        precio_unitario = round(precio_total / (personas * accesos), 2)

        respuesta = (
            f"👥 *{personas} personas*\n"
            f"🔁 *{accesos} accesos por persona*\n\n"
            f"💰 Precio total: *{precio_total} €*\n"
            f"🧮 Precio por persona y acceso: *{precio_unitario} €*\n\n"
            f"🕒 Puedes usar los accesos durante *1 año*.\n"
            f"➡️ Cuantos más accesos compres, más barato te sale."
        )

        # 👉 Botón para contactar
        mensaje_prellenado = (
            f"Hola, estoy interesado en adquirir pases VIP para {personas} persona(s) "
            f"y {accesos} acceso(s) por persona."
        )
        url_contacto = f"https://t.me/junxi112?start={mensaje_prellenado.replace(' ', '%20')}"

        botones = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 Volver a calcular", callback_data="reiniciar")],
            [InlineKeyboardButton("💬 Adquirir pases VIP", url=url_contacto)]
        ])

        await update.message.reply_text(respuesta, parse_mode="Markdown", reply_markup=botones)
        return ConversationHandler.END
    except:
        await update.message.reply_text("❗ Escribe un número válido de accesos (entre 1 y 10).")
        return ACCESOS

# 🔁 Reiniciar con botón inline
async def volver_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("🔁 Vamos a volver a empezar.\n\n👉 ¿Cuántas personas sois?")
    return PERSONAS

# ❌ Cancelar
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cálculo cancelado. Escribe /start para volver a empezar.")
    return ConversationHandler.END

# 🧠 Montar bot
app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
        CallbackQueryHandler(volver_callback, pattern="^reiniciar$")
    ],
    states={
        PERSONAS: [MessageHandler(filters.TEXT & ~filters.COMMAND, personas)],
        ACCESOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, accesos)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(volver_callback, pattern="^reiniciar$"))

# ▶️ Ejecutar bot
app.run_polling()
