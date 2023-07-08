from telegram.ext import *
from telegram import *
from pygismeteo import Gismeteo

TOKEN = ""
gm = Gismeteo()

field = [[" "] * 3 for _ in range(3)]

def generate_buttons():
    keys = [
        [InlineKeyboardButton(field[i][j], callback_data=f"{i} {j}") for j in range(len(field[i]))] for i in
        range(len(field))
    ]
    return InlineKeyboardMarkup(keys)

async def start(update: Update, context):
    await update.message.reply_text("Game started", reply_markup=generate_buttons())


async def handle_callback(update: Update, context):
    i, j = map(int, update.callback_query.data.split())
    field[i][j] = 'x'
    await update.callback_query.answer()
    await update.callback_query.edit_message_reply_markup(generate_buttons())


async def handle_location(update: Update, context):
    weather = gm.current.by_coordinates(update.message.location.latitude, update.message.location.longitude)
    await update.message.reply_text(f"{weather.temperature.air.c} °C\n{weather.description.full}")


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.run_polling()


if __name__ == "__main__":
    main()
