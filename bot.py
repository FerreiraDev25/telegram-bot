from flask import Flask
from threading import Thread
import asyncio
import time
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes


# Seu TOKEN doBotFather aqui!
TOKEN = '7756070091:AAG8TcrPW602VVPlAnHU_O5nuwn8OVZSk-c'

# Função que responde ao comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Eu sou o seu bot do Telegram!")

#Função que responde mensagens comuns
async def responder(update: Update, context: CallbackContext):
    mensagem = update.message.text
    await update.message.reply_text(
        'Olá! Eu sou o seu bot do Telegram! \n'
        'Estes são os comandos disponíveis no momento. \n' 
        '- /start \n'
        ' - /ajuda \n'
        ' - /sobre'
    )

# Função para exibir ajuda
async def ajuda(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Aqui estão os comandos disponíveis:\n'
        '/start - Inicia o bot\n'
        '/ajuda - mostra este menu\n'
        '/sobre - sobre o bot'
    )

# Função para exibir informações sobre o bot
async def sobre(update: Update, context: CallbackContext):
    await update.message.reply_text('Sou um bot criado em Python! \nMe ajude a crescer dando sugestões!')
    
# Criando o aplicativo bot
app = Application.builder().token(TOKEN).build()

#Adicionando comandos
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('ajuda', ajuda))
app.add_handler(CommandHandler('sobre', sobre))

#Adicionando respostas para mensagens comuns
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

#Função Flask para manter o render funcionando
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot está rodando!"

#Função para iniciar o bot no asyncio
def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app.run_polling())

#Função para manter o Flask ativo, realizando o "ping" periodicamente
def keep_flask_alive():
    while True:
        try:
            #Rodando o comando curl para manter o Flask ativo
            subprocess.run(["curl", "-s", "https://seu-bot-no-render.com/"], stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f'Erro ao fazer o ping: {e}')
        #Aguarda 10 minutos (600 segundos) antes de fazer o próximo ping
        time.sleep(600)

#Inicia o bot e o servidor Flask em threads separadas
if __name__ == "__main__":
    flask_thread = Thread(target=flask_app.run, kwargs={"host": "0.0.0.0", "port": 8080}, daemon=True)
    flask_thread.start()

    # Inicia o bot no thread principal com asyncio
    asyncio.run(start_bot())
    
    # Inicia a thread de ping para manter o serviço ativo
    Thread(target=keep_flask_alive, daemon=True).start()
