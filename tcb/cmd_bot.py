from shared import argparseSetup, logSetup, mongoSetup
from Bot import Bot

def main():
    parser = argparseSetup(
        description="Telegram bot to remind me to keep my meatbag in check"
    )
    parser.add("--botToken", env_var="BOT_TOKEN", type=str, help="Telegram bot token")
    args = parser.parse_args()

    logSetup(args)

    try:
        client = mongoSetup(args)
    except Exception:
        return

    Bot(args, client.get_default_database())


if __name__ == "__main__":
    main()