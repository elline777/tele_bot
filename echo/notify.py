from logging import getLogger

from telegram import Bot

from apis.bittrex import BittrexClient, BittrexError
from echo.config import load_config

logger = getLogger(__name__)

NOTIFY_PAIR = 'USD-BTC'


def main():
    config = load_config()
    client = BittrexClient()

    try:
        current_price = client.get_last_price(pair=config.NOTIFY_PAIR)
        message = "{} = {}".format(config.NOTIFY_PAIR, current_price)
    except BittrexError:
        logger.error("BittrexError")
        current_price = None
        message = "Произошла ошибка"

    bot = Bot(
        token=config.TG_TOKEN,
        base_url=config.TG_API_URL
    )
    bot.send_message(
        chat_id=config.NOTIFY_USER_ID,
        text=message
    )


if __name__ == '__main__':
    main()