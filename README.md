# Streaks

This repository contains code for Streaks - a small Telegram bot that helps humans build habits.

To learn more about Streaks, take a look at the [web page](https://streaks.iakov.me/).

The official Streaks bot is running under name [str34ks_bot](https://t.me/str34ks_bot), but you can roll your own instance.

## Install

Streaks is built using Python 3.8. Make sure it's installed on your system, and then clone the repo.

Install pipenv:

    pip install --user pipenv

Install packages:

    pipenv sync

Install hooks:

    pipenv run pre-commit install -t pre-commit
    pipenv run pre-commit install -t pre-push

Create a DB file:

    touch streak_bot.db

Make sure that the `streak_bot.db` file is writeable by the application.

## Configure

Streaks can be configured either via command line arugments or environment variables. Configuration options:

* `DB`, `--db` - path to SQLite3 DB file, defaults to `streak_bot.db`
* `BOT_TOKEN`, `--bot_token` - Telegram bot token, learn more [here](https://core.telegram.org/bots#6-botfather)
* `LOG_FORMAT`, `--log_format` - log format, defaults to `LONG`
* `LOG_LEVEL`, `--log_level` - log level, defaults to `INFO`

## Run

Streaks application has two main components - Bot and Sender.

Bot is the component that has to be always running to handle user interation through Telegram. Run it like this:

    pipenv run python streaks bot

This will create a new Bot that will listen to commands and handle button clicks. Bot is responsible for storing configuration in database.

Sender is the component that sends periodic messages to Streaks users - reminders, updates and summaries. Run it like this:

    pipenv run python streaks send

This will send the messages to users based on current time. It makes sense to run sender as a periodic job on your system.

Take a look at `systemd` folder for a example of Systemd unit and timer files used for Streaks deployment.

To learn more about deployment and installation, take a look at the `ansible/install.taml` playbook. It installs Git, Python and Pip, downloads latest Streaks from GitHub, and re-starts the services.

## Contributing

Streaks is in it's early days. If you have an idea or suggestion, feel free to open a new issue on GitHub. If you wish to help Streaks development, take a look at open issues.

You can reach out to Streaks author on [Telegram](https://t.me/iakovmarkov).

## License

Streaks is licensed under GNU GPL v3.0. You can find the full text of the license in `COPYING` file in this repo.