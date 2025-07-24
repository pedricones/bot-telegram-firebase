
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from datetime import datetime

FIREBASE_URL = "https://sinais-double-default-rtdb.firebaseio.com/sinais.json"
BOT_TOKEN = "7772900897:AAGKUIL7U6EDZWth4Nqd2-RhvQGIBm0ud3Y"

mapa_cores = {
    "⚫️": "Preto",
    "🔴": "Vermelho",
    "🟢": "Verde",
    "⚪️": "Branco"
}

def enviar_para_firebase(cor, gales):
    dados = {
        "Horario": datetime.now().strftime("%H:%M"),
        "Entre Agora na Cor": cor,
        "Gales": gales,
        "Jogo": "Double"
    }
    try:
        response = requests.post(FIREBASE_URL, json=dados)
        print("✅ Enviado para Firebase:", response.status_code, response.text)
    except Exception as e:
        print("❌ Erro ao enviar para Firebase:", e)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        texto = update.message.text
        print("📥 Mensagem recebida:", texto)

        cor_principal = None
        gales = 0

        if "Faça a Entrada No:" in texto:
            for emoji, nome in mapa_cores.items():
                if emoji in texto:
                    cor_principal = nome
                    break

            if "SEM GALE" in texto:
                gales = 0
            else:
                import re
                match = re.search(r'(\d+)\s*tentativa', texto)
                if match:
                    gales = int(match.group(1))

            if cor_principal:
                enviar_para_firebase(cor_principal, gales)
            else:
                print("⚠️ Cor principal não detectada.")

    except Exception as e:
        print("❌ Erro no handle:", e)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle))
    print("🤖 Bot rodando e monitorando mensagens...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
