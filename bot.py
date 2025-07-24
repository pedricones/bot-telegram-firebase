import requests
from telegram.ext import Updater, MessageHandler, Filters
from datetime import datetime

FIREBASE_URL = "https://sinais-double-default-rtdb.firebaseio.com"

# Mapeamento dos emojis para nomes de cores
mapa_cores = {
    "⚫️": "Preto",
    "🔴": "Vermelho",
    "🟢": "Verde",
    "⚪️": "Branco"
}

def enviar_para_firebase(dados):
    try:
        response = requests.post(FIREBASE_URL + "/sinais.json", json=dados)
        print("✅ Sinal enviado com sucesso:", response.status_code)
    except Exception as e:
        print("❌ Erro ao enviar sinal:", e)

def processar_mensagem(update, context):
    if not update.message or not update.message.text:
        return

    texto = update.message.text
    print("📩 Mensagem recebida:", texto)

    cor_principal = None
    gales = 0

    if "Faça a Entrada No:" in texto:
        linha = [l for l in texto.split("\n") if "Faça a Entrada No:" in l]
        if linha:
            for emoji, nome in mapa_cores.items():
                if emoji in linha[0]:
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
        dados = {
            "Horario": datetime.now().strftime("%H:%M"),
            "Entre Agora na Cor": cor_principal,
            "Gales": gales,
            "Jogo": "Double"
        }
        enviar_para_firebase(dados)
    else:
        print("⚠️ Nenhuma cor detectada. Ignorado.")

def main():
    updater = Updater("7772900897:AAGKUIL7U6EDZWth4Nqd2-RhvQGIBm0ud3Y", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, processar_mensagem))
    print("🤖 Bot rodando e monitorando mensagens...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
