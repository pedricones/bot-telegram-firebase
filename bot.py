import requests
import re
from telegram.ext import Updater, MessageHandler, Filters
from datetime import datetime

# URL do seu Firebase
FIREBASE_URL = "https://sinais-double-default-rtdb.firebaseio.com"

# Emojis e mapeamento de cores
mapa_cores = {
    "⚫️": "Preto",
    "🔴": "Vermelho",
    "🟢": "Verde",
    "⚪️": "Branco"
}

# Envia os dados formatados para o Firebase
def enviar_para_firebase(dados):
    try:
        response = requests.post(FIREBASE_URL + "/sinais.json", json=dados)
        print("✅ Sinal enviado com sucesso:", dados)
    except Exception as e:
        print("❌ Erro ao enviar sinal:", e)

# Processa cada mensagem recebida
def processar_mensagem(update, context):
    mensagem = update.effective_message
    if not mensagem or not mensagem.text:
        print("⚠️ Ignorado: mensagem sem texto.")
        return

    texto = mensagem.text
    print("📩 Mensagem recebida:", texto)
    print("🧩 Conteúdo bruto:", vars(mensagem))  # DEBUG: estrutura completa da mensagem

    # Só processa se contiver a palavra-chave
    if "Faça a Entrada No:" not in texto:
        print("⚠️ Ignorado: não contém 'Faça a Entrada No:'.")
        return

    cor_principal = None
    gales = 0

    # Procura a linha com a entrada
    for linha in texto.split("\n"):
        if "Faça a Entrada No:" in linha:
            for emoji, cor in mapa_cores.items():
                if emoji in linha:
                    cor_principal = cor
                    break
            break

    # Detectar GALE
    if "SEM GALE" in texto.upper():
        gales = 0
    else:
        tentativa = re.search(r"(\d+)\s*tentativa", texto, re.IGNORECASE)
        if tentativa:
            gales = int(tentativa.group(1))

    if cor_principal:
        dados = {
            "Horario": datetime.now().strftime("%H:%M"),
            "Entre Agora na Cor": cor_principal,
            "Gales": gales,
            "Jogo": "Double"
        }
        enviar_para_firebase(dados)
    else:
        print("⚠️ Nenhuma cor identificada. Ignorado.")

# Função principal
def main():
    updater = Updater("7772900897:AAGKUIL7U6EDZWth4Nqd2-RhvQGIBm0ud3Y", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, processar_mensagem))
    print("🤖 Bot rodando e monitorando mensagens...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
