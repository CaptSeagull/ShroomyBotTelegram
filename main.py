import logging

from uuid import uuid4
from telegram import (Bot, CallbackQuery,
                      InlineQueryResultArticle, InputTextMessageContent, ParseMode,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackQueryHandler
from telegram.utils.helpers import escape_markdown

import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logging.getLogger(__name__)
'''
bot = telegram.Bot(token=config.token)
print(bot.get_me())
'''


def log_function_call(func):
    logging.info("Initiated command: {}".format(func.__name__))


'''Enter all commands here'''


def start(bot: Bot, update: CallbackQuery):
    log_function_call(start)
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, talk to me!")


def ask_me(bot, update):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def ask_me2(bot, update):
    keyboard = [[InlineKeyboardButton("Option 4", callback_data='4'),
                 InlineKeyboardButton("Option 5", callback_data='5')],

                [InlineKeyboardButton("Option 6", callback_data='6')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def inline_bot(bot: Bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]
    bot.answer_inline_query(update.inline_query.id, results)


def error(bot: Bot, update, error):
    """Log Errors caused by Updates."""
    logging.warning('{}\'s Update {} caused error {}'.format(bot.first_name, update, error))


'''Main setup here'''


def setup():
    updater = Updater(token=config.token)
    dispatcher = updater.dispatcher

    '''Add commands to dispatcher here'''
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('ask', ask_me))
    dispatcher.add_handler(CommandHandler('ask2', ask_me2))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(InlineQueryHandler(inline_bot))
    updater.dispatcher.add_error_handler(error)

    return updater


if __name__ == '__main__':
    updater = setup()
    updater.start_polling()
    logging.info("{0} is running on {1}".format(config.name, config.version))
    updater.idle()
    logging.info("{0} is stopped".format(config.name))
