import logging
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


def argparseSetup(description):
    parser = ArgParser(description)

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

    return parser


def logSetup(args):
    logging.basicConfig(
        level=args.logLevel,
        format=logFormats[args.logFormat],
        datefmt="%d-%b-%y %H:%M:%S",
    )
    logging.root.setLevel(args.logLevel)
    print(f"Log level is {args.logLevel}")


def mongoSetup(args):
    try:
        logging.info("Connecting to MongoDB...")
        client = MongoClient(args.db, serverSelectionTimeoutMS=3000)
        client.server_info()
    except Exception as e:
        logging.error(e)
        logging.error("Error connecting to MongoDB, exiting")
        raise e

    logging.info("Connected to MongoDB")
    return client
