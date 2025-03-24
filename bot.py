import os
import csv
from datetime import datetime
from collections import defaultdict
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
NGROK_URL = os.getenv("NGROK_URL")

# Estados
CATEGORIA, METODO_PAGO, CANTIDAD_DESC = range(3)
CATEGORIAS = [["🍔 Comida", "🚗 Transporte"], ["🛍️ Compras", "🏠 Casa"]]
METODOS_PAGO = [["💵 Efectivo", "💳 Tarjeta"]]

# Helpers

def get_csv_filename(user_id):
    return f"gastos_{user_id}.csv"

def get_presupuesto_filename(user_id):
    return f"presupuesto_{user_id}.txt"

def guardar_en_csv(csv_file, fecha, cantidad, categoria, metodo, descripcion):
    archivo_existe = os.path.isfile(csv_file)
    with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not archivo_existe:
            writer.writerow(["Fecha", "Cantidad", "Categoría", "Método", "Descripción"])
        writer.writerow([fecha, cantidad, categoria, metodo, descripcion])

def cargar_presupuesto(user_id):
    file = get_presupuesto_filename(user_id)
    if os.path.isfile(file):
        with open(file, "r") as f:
            return float(f.read().strip())
    return None

def verificar_presupuesto(user_id, total_mes_actual):
    presupuesto = cargar_presupuesto(user_id)
    if presupuesto:
        porcentaje = total_mes_actual / presupuesto
        if porcentaje >= 1:
            return f"⚠️ Has superado tu presupuesto mensual de {presupuesto:.2f}€."
        elif porcentaje >= 0.8:
            return f"⚠️ Has alcanzado el 80% de tu presupuesto mensual ({presupuesto:.2f}€)."
    return None

# Comandos del bot

def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 ¡Hola! Usa /gasto para registrar un gasto, /resumen para ver tus gastos o /presupuesto para fijar un límite mensual.")

def gasto(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(CATEGORIAS, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("¿En qué categoría quieres registrar el gasto?", reply_markup=reply_markup)
    return CATEGORIA

def categoria_seleccionada(update: Update, context: CallbackContext):
    context.user_data["categoria"] = update.message.text
    reply_markup = ReplyKeyboardMarkup(METODOS_PAGO, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Selecciona el método de pago:", reply_markup=reply_markup)
    return METODO_PAGO

def metodo_pago_seleccionado(update: Update, context: CallbackContext):
    context.user_data["metodo"] = update.message.text
    update.message.reply_text("Introduce el gasto en formato: cantidad descripción\nEjemplo: 12 hamburguesa")
    return CANTIDAD_DESC

def guardar_gasto(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id
        csv_file = get_csv_filename(user_id)
        partes = update.message.text.split(" ", 1)
        cantidad = float(partes[0])
        descripcion = partes[1] if len(partes) > 1 else ""
        categoria = context.user_data["categoria"]
        metodo = context.user_data["metodo"]
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        guardar_en_csv(csv_file, fecha, cantidad, categoria, metodo, descripcion)
        update.message.reply_text(f"✅ Gasto registrado: {cantidad}€ en {categoria} - {descripcion} ({metodo})")

        total = calcular_total_mes_actual(user_id)
        aviso = verificar_presupuesto(user_id, total)
        if aviso:
            update.message.reply_text(aviso)
    except:
        update.message.reply_text("❌ Formato incorrecto. Usa: 12 hamburguesa")
    return ConversationHandler.END

def calcular_total_mes_actual(user_id):
    csv_file = get_csv_filename(user_id)
    if not os.path.isfile(csv_file): return 0
    now = datetime.now().strftime("%Y-%m")
    total = 0
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Fecha"].startswith(now):
                total += float(row["Cantidad"])
    return total

def cancelar(update: Update, context: CallbackContext):
    update.message.reply_text("❌ Operación cancelada.")
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("gasto", gasto)],
        states={
            CATEGORIA: [MessageHandler(Filters.text & ~Filters.command, categoria_seleccionada)],
            METODO_PAGO: [MessageHandler(Filters.text & ~Filters.command, metodo_pago_seleccionado)],
            CANTIDAD_DESC: [MessageHandler(Filters.text & ~Filters.command, guardar_gasto)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(conv_handler)

    PORT = int(os.environ.get("PORT", 8443))
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{NGROK_URL}/{TOKEN}"
    )
    updater.idle()

if __name__ == "__main__":
    main()
