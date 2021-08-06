import httpimport
import logging
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from typing import Dict
from dotenv import load_dotenv
load_dotenv('.env')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

TOKEN = os.getenv("TOKEN")

logger = logging.getLogger(__name__)

TASK, DATE, TIME = range(3)


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def create(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(
        'Please enter the task'
    )

    return TASK


def task(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = update.message.text
    context.user_data['task'] = text
    logger.info("Task of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Please enter date'
    )

    return DATE


def date(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = update.message.text

    context.user_data['date'] = text
    logger.info("Task of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Please enter time'
    )

    return TIME


def time(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    text = update.message.text

    context.user_data['time'] = text
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    print(context.user_data)
    update.message.reply_text(
        f"Here's the reminder you created: {facts_to_str(context.user_data)}Until next time!",)

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def listout(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        f"List: {facts_to_str(context.user_data)}Until next time!",)


def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("list", listout))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create', create)],
        states={
            TASK: [MessageHandler(Filters.text & ~Filters.command, task)],
            DATE: [MessageHandler(Filters.text & ~Filters.command, date)],
            TIME: [MessageHandler(Filters.text & ~Filters.command, time)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
