from sendMessages import sendMessages
from shared import argparseSetup, logSetup, mongoSetup


def main():
    parser = argparseSetup(description="Message sender application")
    args = parser.parse_args()

    logSetup(args)

    try:
        client = mongoSetup(args)
    except Exception:
        return

    sendMessages(args, client.get_default_database())


if __name__ == "__main__":
    main()
