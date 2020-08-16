from configargparse import ArgParser
from Bot import Bot
from DB import DB
import logging


def main():
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

    print("Initializing TinyCareBot")
    parser = ArgParser(
        description="Telegram bot to remind me to keep my meatbag in check"
    )
    parser.add("--botToken", env_var="BOT_TOKEN", type=str, help="Telegram bot token")
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
    parser.add(
        "--db",
        env_var="DB",
        help='MongoDB String'
    )
    args = parser.parse_args()

    print(f"Log level is {args.logLevel}")

    logging.basicConfig(
        level=args.logLevel,
        format=logFormats[args.logFormat],
        datefmt="%d-%b-%y %H:%M:%S",
    )
    logging.root.setLevel(args.logLevel)

    myDb = DB(args)
    Bot(args, myDb)


if __name__ == "__main__":
    main()

