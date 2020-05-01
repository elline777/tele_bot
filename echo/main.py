from logging import getLogger
from subprocess import Popen
from subprocess import PIPE

from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from echo.config import load_config

config = load_config()

logger = getLogger(__name__)


def do_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Привет! Отправь мне что-нибудь",
    )


def do_help(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Это учебный бот\n\n"
             "Список доступных команд есть в меню\n\n"
             "Так же я отвечую на любое сообщение",
    )


def do_time(update: Update, context: CallbackContext):
    # process = Popen(["date"], stdout=PIPE)
    process = Popen("date /t", shell=True, stdout=PIPE)
    text, error = process.communicate()
    # Может произойти ошибка вызова процесса (код возврата не 0)
    if error:
        text = "Произошла ошибка, время неизвестно"
    else:
        # Декодировать ответ команды из процесса
        text = text.decode("utf-8")
    update.message.reply_text(text)


def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    reply_text = "Ваш Id = {}\n\n{}".format(chat_id, text)
    update.message.reply_text(
        text=reply_text
    )


def main():
    logger.info("Запускаем бота...")

    bot = Bot(
        token=config.TG_TOKEN,
        base_url=config.TG_API_URL
    )
    updater: Updater = Updater(
        bot=bot,
        use_context=True
    )

    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    logger.info(f'Bot info: {info}')

    # Навесить обработчики команд
    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_help)
    time_handler = CommandHandler("time", do_time)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(message_handler)

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()

    logger.info("Закончили...")


if __name__ == '__main__':
    main()
