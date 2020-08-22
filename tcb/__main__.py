import logging
from sendMessages import sendMessages
from Bot import Bot
from pymongo import MongoClient
from configargparse import ArgParser

logLevels = [
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
]

logFormats = {
    "LONG": "%(asctime)s - %(message)s",
    "SHORT": "%(message)s",
}

def main():
    parser = ArgParser(description="Telegram bot to remind me to keep my meatbag in check")

    parser.add(
        "command",
        help="Command to execute. Can be 'bot' or 'send'.",
    )
    parser.add(
        "--logFormat",
        env_var="LOG_FORMAT",
        help="Log format. Can be SHORT or LONG",
        default="LONG",
    )
    parser.add(
        "--logLevel",
        env_var="LOG_LEVEL",
        help=f'Log verbosity. Can be {", ".join(logLevels)}',
        default="INFO",
    )

    parser.add("--db", env_var="DB", help="MongoDB String")
    parser.add("--botToken", env_var="BOT_TOKEN", type=str, help="Telegram bot token")

    args = parser.parse_args()

    if (args.command == 'bot'):
        command = Bot
    elif (args.command == 'send'):
        command = sendMessages
    else:
        print(f"Command {args.command} is not valid.")
        print(parser.format_help())
        return

    logging.basicConfig(
        level=args.logLevel,
        format=logFormats[args.logFormat],
        datefmt="%d-%b-%y %H:%M:%S",
    )
    logging.root.setLevel(args.logLevel)
    print(f"Log level is {args.logLevel}")

    try:
        logging.info("Connecting to MongoDB...")
        client = MongoClient(args.db, serverSelectionTimeoutMS=3000)
        client.server_info()
    except Exception as e:
        logging.error(e)
        logging.error("Error connecting to MongoDB, exiting")
        return

    logging.info("Connected to MongoDB")

    command(args, client.get_default_database())


if __name__ == "__main__":
    main()
