
"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Conversational Bot example, repeats stikers as echo.
and Send News of different languages from whole world.
"""

import logging
import time
from telegram import Update, ForceReply, Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher
from utlis import get_reply, fetch_news, topics_keyboard
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    #send a hi sticker
    with open("hi.tgs", "rb") as sticker:
        update.message.reply_sticker(sticker)
 
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=False),
    )
    update.message.reply_text("Just click - /news")
def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Here to help you\n\nJust click - /news & you will get suggestions😊\n\nLanguages📚 supported-\n  English, Hindi, Tamil, Malayalam, Bengali & foreign languages\n\nSome basic conversation🗣 is possible\n\nAnd for news these are some basic commands for bot-\nIndian news in hindi\nTech news in Malayalam\nBusiness news in Bengali\nNews around the world in hindi\n\nHope you like it\n\nJust type forward slash(/) for more task and GitHub link\n\n  -Harsh Mathur")


def news(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /news is issued."""
    with open("news.tgs", "rb") as sticker:
        update.message.reply_sticker(sticker)
    update.message.reply_text('Choose a category!', reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True) )

def creator(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /creator is issued."""
    with open("create.tgs", "rb") as sticker:
        update.message.reply_sticker(sticker)
    update.message.reply_text('Harsh Mathur\n-Lakshmi Narain College of Technology')

def backend(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /backend is issued."""
    with open("duck.tgs", "rb") as sticker:
        update.message.reply_sticker(sticker)
    update.message.reply_text('This bot uses following tech-tools : \n\n - Python telegram library is heart of this bot\n\n - Dialogflow API for conversation\n\n - More than one dozen python libraries to perform different tasks like finding news, creating echo sticker messages to processing different parameters of test case like language, country etc.\n\n - Heroku Cloud Platform is used to host this bot\n\nand many more.')

def github(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /githu is issued."""
    update.message.reply_text('😺😺😺\nhttps://github.com/HarshMathur86/Telegram-news-bot-using-dialogflow')

def reply_text(update: Update, _: CallbackContext) -> None:
    """Reply the message."""

    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if intent == "get_news":
        articles  = fetch_news(reply)
        if len(articles) == 0:
            update.message.reply_text("Sorry news server isn't responding. 🥺\n Try to tell different")
            return
        for article in articles:
            update.message.reply_text(article.get('link'))
    else:
        update.message.reply_text(reply)

    print(CallbackContext)

def echo_sticker(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_sticker(update.message.sticker)
    update.message.reply_text("Take this back 😆")
    print(CallbackContext, end='')
    print(" echo_message : ", end='')
    print(update.message.sticker, end='\n\n')

    
 

def main() -> None:

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("creator", creator))
    dispatcher.add_handler(CommandHandler("news", news))
    dispatcher.add_handler(CommandHandler("backend", backend))
    dispatcher.add_handler(CommandHandler("github", github))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_text))
    dispatcher.add_handler(MessageHandler(Filters.sticker & ~Filters.command, echo_sticker))
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()