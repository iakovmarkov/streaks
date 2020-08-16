# Features

[X] Project setup - Git
[X] Project setup - Bot
[ ] Deployment - VM, domain
[ ] Deployment - Systemd unit
[ ] Deployment - SSL
[X] Bot - about
[X] Deployment - MongoDB
[X] Bot - schedule a reminder daily (in the morning, in the afternoon, in the evening)
[ ] Bot - healthcheck, sent messages in the last hr
[ ] Privacy - encrypt messages using User ID + salt
[ ] Scheduler - send reminders
[ x Bot - delete a reminder
[ ] Bot - scheudle a reminder (daily, every N days, every X,Y,Z)
[ ] Bot - repeat reminders, require "Ok", snooze for 30m
[ ] Bot - set timezone per user
[ ] Bot - Randomize messages
[ ] Bot - Greet daily with a :hi: emoji
[ ] Bot - Weekly stat

# Sending notifications

Runs every hour
Get current hour in GMT 0
Repeat for morning, afternoon and evening Periods:
    Get Offset to 9:00 (i.e. current hour - Period)
    Select all users whose TZ is Offset from above
    Get their jobs
    Generate personalized [morning, afternoon, evening] messages
    Add Messages to Queue
After Queue filled
If Queue length is more than 10 * 60 * 60 - Error in Log!
Repeat until finished:
    Take 10 messages from Queue
    Send
    Sleep 1s
