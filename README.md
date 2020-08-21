# Features

[X] Project setup - Git
[X] Project setup - Bot
[ ] Deployment - VM
[X] Bot - about
[X] Deployment - MongoDB
[X] Bot - schedule a reminder daily (in the morning, in the afternoon, in the evening)
[ ] Bot - healthcheck, sent messages in the last hr
[ ] Privacy - encrypt messages using User ID + salt
[X] Scheduler - send reminders
[X] Bot - delete a reminder
[ ] Bot - scheudle a reminder (daily, every N days, every X,Y,Z)
[ ] Bot - repeat reminders, require "Ok", snooze for 30m
[X] Bot - set timezone per user
[ ] Bot - Randomize messages
[ ] Bot - Greet daily with a :hi: emoji
[ ] Bot - Weekly stat

# Setup

## Production

Install pipenv

    pip install --user pipenv

Install packages

    pipenv sync

## Development

Install hooks:

    pipenv run pre-commit install -t pre-commit
    pipenv run pre-commit install -t pre-push

## Deployment

Run ansible playbook:

    ansible-playbook ansible.yaml

It requires host `tcb` to be in your inventory. Put the secrets in `/etc/environment`.
