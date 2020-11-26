#!/usr/bin/env python3
#
# A library that allows to create an inline calendar keyboard.
# grcanosa https://github.com/grcanosa
#
"""
Base methods for calendar keyboard creation and processing.
"""


from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
import datetime
import calendar


def create_callback_data(action,year,month,day):
    """ Create the callback data associated to each button"""
    return ";".join([action,str(year),str(month),str(day)])


def create_callback_clock(action, hour, minute, m):
    """ Create the callback data associated to each button"""
    return ";".join([action,str(hour),str(minute),m])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_clock(hour=None, minute=None, m=None):
    # ↑ ↓
    keyboard = []
    now = datetime.datetime.now()
    if not hour:
        hour = now.hour
        if hour > 12:
            hour -= 12
    if not minute:
        minute = int(str(now.minute)[:-1] + "0")
        # minute = now.minute
    if not m:
        m = "am"
    data_ignore = create_callback_clock("IGNORE", hour, minute, m)

    row = []
    row.append(InlineKeyboardButton("↑", callback_data=create_callback_clock("PLUS-HOUR", hour, minute, m)))
    row.append(InlineKeyboardButton("↑", callback_data=create_callback_clock("PLUS-MINUTE", hour, minute, m)))
    row.append(InlineKeyboardButton("↑", callback_data=create_callback_clock("PLUS-M", hour, minute, m)))
    keyboard.append(row)

    row = []
    row.append(InlineKeyboardButton(str(hour), callback_data=data_ignore))
    row.append(InlineKeyboardButton(str(minute), callback_data=data_ignore))
    row.append(InlineKeyboardButton(m, callback_data=data_ignore))
    keyboard.append(row)

    row = []
    row.append(InlineKeyboardButton("↓", callback_data=create_callback_clock("MINUS-HOUR", hour, minute, m)))
    row.append(InlineKeyboardButton("↓", callback_data=create_callback_clock("MINUS-MINUTE", hour, minute, m)))
    row.append(InlineKeyboardButton("↓", callback_data=create_callback_clock("MINUS-M", hour, minute, m)))
    keyboard.append(row)

    row = []
    row.append(InlineKeyboardButton("OK", callback_data=create_callback_clock("OKAY", hour, minute, m)))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_clock_selection(bot, update):
    data = (False, None)
    query = update.callback_query
    (action, hour, minute, m) = separate_callback_data(query.data)
    hour, minute = int(hour), int(minute)

    if action == "IGNORE":
        bot.answer_callback_query(callback_query_id= query.id)

    elif action == "OKAY":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        data = True, [hour, minute, m]

    elif action == "PLUS-HOUR":
        if hour == 12:
            hour = 1
        else:
            hour += 1
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_clock(hour, minute, m))

    elif action == "MINUS-HOUR":
        if hour == 0:
            hour = 12
        else:
            hour -= 1
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_clock(hour, minute, m))

    elif action == "PLUS-MINUTE":
        if minute == 50:
            minute = 0
        else:
            minute += 10
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_clock(hour, minute, m))

    elif action == "MINUS-MINUTE":
        if minute == 0:
            minute = 50
        else:
            minute -= 10
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_clock(hour, minute, m))

    elif action == "PLUS-M":
        if m == "am":
            m = "pm"
        else:
            m = "am"
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_clock(hour, minute, m))

    elif action == "MINUS-M":
        if m == "am":
            m = "pm"
        else:
            m = "am"
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_clock(hour, minute, m))

    return data



def create_calendar(year=None,month=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    #First row - Month and Year
    row=[]
    row.append(InlineKeyboardButton(calendar.month_name[month]+" "+str(year),callback_data=data_ignore))
    keyboard.append(row)
    #Second row - Week Days
    row=[]
    for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
        row.append(InlineKeyboardButton(day,callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
            else:
                row.append(InlineKeyboardButton(str(day),callback_data=create_callback_data("DAY",year,month,day)))
        keyboard.append(row)
    #Last row - Buttons
    row=[]
    row.append(InlineKeyboardButton("<",callback_data=create_callback_data("PREV-MONTH",year,month,day)))
    row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
    row.append(InlineKeyboardButton(">",callback_data=create_callback_data("NEXT-MONTH",year,month,day)))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def process_calendar_selection(bot,update):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """
    ret_data = (False,None)
    query = update.callback_query
    (action,year,month,day) = separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        bot.answer_callback_query(callback_query_id= query.id)
    elif action == "DAY":
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = True, datetime.datetime(int(year),int(month),int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(pre.year),int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(ne.year),int(ne.month)))
    else:
        bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data
