import json
from utils import is_authorized
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from notifications.birthdays import check_birthdays
from notifications.custom import check_custom

CHAT_ID = -4871518173
TOKEN = "7909371368:AAGPCCw2qx9aybzUJbFHYjXZPPOb840c028"

async def load_events():
    with open("data/events.json") as f:
        return json.load(f)

async def notify(app):
    while True:
        events = await load_events()
        messages = []
        messages += check_birthdays(events)
        messages += check_custom(events)

        for msg in messages:
            await app.bot.send_message(chat_id=CHAT_ID, text=msg)

        await asyncio.sleep(86400)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("⛔ Non sei autorizzato a usare questo bot.")
        return

    await update.message.reply_text("✅ Bot attivo. Puoi aggiungere eventi con /aggiungi_evento.")

async def aggiungi_evento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("Non sei autorizzato ad usare questo comando")
        return

    try:
        tipo = context.args[0]
        nome_o_testo = context.args[1]
        data = context.args[2]

        with open("data/events.json", "r") as f:
            events = json.load(f)

        if tipo == "birthday":
            events.append({"type": "birthday", "name": nome_o_testo, "date": data})
        elif tipo == "custom":
            events.append ({"type": "custom", "text": nome_o_testo, "date": data})
        else:
            await update.message.reply_text("⚠️ Tipo non valido. Usa 'birthday' o 'reminder'.")
            return

        with open("data/events.json", "w") as f:
            json.dump(events, f, indent=2)

        await update.message.reply_text("✅ Evento aggiunto con successo!")
    except Exception as e:
        await update.message.reply_text("❌ Errore: usa il formato\n`/aggiungi_evento birthday Marco 2025-05-20`",
                                        parse_mode="Markdown")

async def lista_eventi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("Non sei autorizzato ad usare questo comando")
        return

    with open ("data/events.json") as f:
        events = json.load(f)

    if not events:
        await update.message.reply_text("📭 Nessun evento salvato.")
        return

    testo = "📅 Eventi salvati:\n"
    for e in events:
        if e["type"] == "birthday":
            testo += f"🎂 {e['name']} - {e['date']}\n"
        elif e["type"] == "reminder":
            testo += f"📌 {e['text']} - {e['date']}\n"

    await update.message.reply_text(testo)

async def main ():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aggiungi_evento", aggiungi_evento))
    app.add_handler(CommandHandler("lista_eventi", lista_eventi))
    asyncio.create_task(notify(app))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
