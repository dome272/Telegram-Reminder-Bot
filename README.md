# Telegram Reminder Bot
A Telegram Bot which serves as a reminder for your meetings, appointments, events etc.

```/start -> add a new reminder```

```/list -> lists all scheduled future reminders```

```/time -> change your timezone (standard on utc time)```

## Try the bot
You can use the bot under: http://t.me/Appointment_Reminder_Bot

## Requirements
* ```pip install python-telegram-bot```
* telegram api token - place it in [bot.py](https://github.com/dome272/Telegram-Reminder-Bot/blob/main/bot.py) on line 248

## Demo Video
<img src="/images/telegram_reminder.gif" width="197" height="426"/>

## How it works
The code uses the telegram.ext ConversationHandler to create a guided and flawless conversation flow. Moreover it uses different other telegram.ext classes
to "ask & get" the responses information from the user. Furthermore all of the data is being stored in [reminder.json](https://github.com/dome272/Telegram-Reminder-Bot/blob/main/reminder.json)
to create the data flow between the different states of the ConversationHandler and have the opportunity to access the reminder later on (e.g. for the ```/list``` command).
Disclaimer: This is my first bot for telegram, so there might be things that could have been implemented and routed easier than I did.

## Credits
https://github.com/unmonoqueteclea/calendar-telegram -> calendar implementation
https://github.com/python-telegram-bot/python-telegram-bot -> telegram API

## Contact
Instagram [@dome271](https://instagram.com/dome271) 
Email: d6582533@gmail.com
