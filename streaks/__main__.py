import logging
from sender import send
from Bot import Bot
from configargparse import ArgParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Streak

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
    parser = ArgParser(description="Telegram bot to help humans build better habits")

    parser.add(
        "command",
        help="Command to execute. Can be 'bot' or 'send'.",
    )
    parser.add(
        "--log_format",
        env_var="LOG_FORMAT",
        help="Log format. Can be SHORT or LONG",
        default="LONG",
    )
    parser.add(
        "--log_level",
        env_var="LOG_LEVEL",
        help=f'Log verbosity. Can be {", ".join(logLevels)}',
        default="INFO",
    )

    parser.add(
        "--db",
        env_var="DB",
        default="streak_bot.db",
        help="SQLite3 DB file name, default 'streak_bot.db'",
    )
    parser.add("--bot_token", env_var="BOT_TOKEN", type=str, help="Telegram bot token")

    args = parser.parse_args()
    print(f"Log level is {args.logLevel}")

    if args.command == "bot":
        command = Bot
    elif args.command == "send":
        command = send
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

    try:
        logging.info(f"Using DB: {args.db}")
        engine = create_engine(f"sqlite:///{args.db}")

        User.init(engine)
        Streak.init(engine)

        Session = sessionmaker(bind=engine)
        session = Session()
    except Exception as e:
        logging.error(e)
        logging.error("DB check failed, exiting")
        return

    command(args, session)


if __name__ == "__main__":
    main()
