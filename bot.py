from flask import Flask
from threading import Thread
import asyncio
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
    await update.message.reply_text(f'Olá! Eu sou o seu bot do Telegram! \nEstes são os comandos disponíveis no momento. \n - /start \n - /ajuda \n - /sobre')

# Função para exibir ajuda
async def ajuda(update: Update, context: CallbackContext):
    await update.message.reply_text('Aqui estão os comandos disponíveis:\n/start - Inicia o bot\n/ajuda - mostra este menu\n/sobre - sobre o bot')

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
async def start_bot():
    await app.run_polling()

#Função para iniciar o bot em task assíncrona
def run_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot()) # inicia o bot como uma tarefa assíncrona
    loop.run_forever() # Garante que o loop de evento continue rodando

#Inicia o bot e o servidor Flask em threads separadas
Thread(target=start_bot).start()

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8080)
