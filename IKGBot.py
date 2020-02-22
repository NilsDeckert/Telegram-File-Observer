#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from functools import wraps
import logging
import filecmp
import threading
import calendar
import datetime
import time
import cmp
import printPdf
from config import mysql_pw
from config import telegram_pw
from config import settings
import mysql.connector
from mysql.connector import errorcode

#Telegram Setup
bot = telegram_pw.bot
updater = telegram_pw.updater
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logging.info("Script started")

#DB setup
global mydb
global mycursor
mydb = mysql_pw.login
mycursor = mydb.cursor()

#File Observer Setup
file = settings.file

# checks if file was updated, if so sends it every user in the database who subscribed to the newsletter
def check():
    n = 0
    mydb = pw.login
    mycursor = mydb.cursor()
    if cmp.check_v():
        v_prm = 'v/v.pdf'
        v_prm_size = os.stat(v_prm).st_size // 1024                             # file size in kb
        logging.info('File was updated ({}kb)'.format(str(v_prm_size)))         # prints file size
        updates_time_date()                                                     # triggers function that creates database entry to log the update
        logging.info('Converting pdf to text...')
        printPdf.pdftotext()
        logging.info('Finished!')
        logging.info('Sending newsletter...')
        try:
            mycursor.execute("SELECT user_id, grade FROM users WHERE sub=1")    # lists all users who subscribed to newsletter
            records = mycursor.fetchall()
            for row in records:
                grade = str(row[1])
                u_id = str(row[0])
                if printPdf.grade_check(grade):                                 # checks if users grade is in the pdfs content. empty string -> user receives every update
                    try:
                        send_v(u_id, 'v/v.pdf')
                        logging.info('Sent newsletter to {} ({})'.format(u_id, grade))
                        n += 1
                    except:
                        logging.error("Error in grade_check")
            mycursor.close()
            logging.info("Finished sending newsletter")
            print("Sent newsletter to {} users".format(str(n)))
        except:
            logging.error("check() - Error sending newsletter")
            ErrorNot("Sending newsletter")
    else:
        if settings.no_update_message:
            logging.info("No updated file")
    threading.Timer(settings.update_interval, check).start()


# Creates database entry to log every update of the file
def updates_time_date():
    mydb = pw.login
    mycursor = mydb.cursor()
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_day = datetime.datetime.now().strftime('%A')
    v_prm = 'v/v.pdf'
    v_prm_size = os.stat(v_prm).st_size // 1024
    try:
        # creates database entry with the current date, time, day of the week and the file size of the updated file
        sql = "INSERT INTO updates_time (date, time, day, file_size_kb) VALUES (%s, %s, %s, %s)"
        val = (current_date, current_time, current_day, v_prm_size)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        mydb = pw.login
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM updates_date WHERE date='{}'".format(current_date))
        records = mycursor.fetchall()
        # if this is the first update today, a new entry with today's date and day of the week is created
        if records == []:
            sql = "INSERT INTO updates_date (date, day, updates) VALUES (%s, %s, %s)"
            val = (current_date, current_day, '1')
            mycursor.execute(sql,val)
            logging.info("New entry for {} in updates_date".format(current_date))
        # if the file has been updated earlier this day, the count goes up by 1 for every additional update
        else:
            for row in records:
                date_updates = row[2] + 1
                mycursor.execute("UPDATE updates_date SET updates = {} WHERE date = '{}'".format(date_updates, current_date))
                logging.info("Updated entry for {} in updates_date ({})".format(current_date, date_updates))
        mydb.commit()
        mycursor.close()
    except:
        logging.error('updates_time_date() - Error commiting to database')
        ErrorNot("updates_time_date() - Error commiting to database")


# Handles the start of a new conversation
def start(update, context):
    mydb = pw.login
    mycursor = mydb.cursor()

    # logs user info
    # Note: user id is the only string that's never empty, users can choose to only set an username or their first name
    u_id = str(update.message.from_user.id)                                     # user id
    u_username = str(update.message.from_user.username)                         # username
    u_first_name = str(update.message.from_user.first_name)                     # first name
    u_last_name = str(update.message.from_user.last_name)                       # last name
    u_lang = str(update.message.from_user.language_code)                        # language code

    logging.info("{}: /start".format(u_id))

    try:
        # checks if user has uses the bot before / if there's an entry for this user already
        mycursor.execute("SELECT * FROM users WHERE user_id='{}'".format(u_id))
        records = mycursor.fetchall()
        # if there's no entry for this user in the database
        # all user info is saved in it.
        if records == []:
            logging.info("New user")
            print("\n" + "New user!")
            print("---")
            print("id:          " + u_id)
            print("username:    " + u_username)
            print("first name:  " + u_first_name)
            print("last name:   " + u_last_name)
            print("lang:        " + u_lang)
            print("---")
            mycursor.close()
            try:
                mydb = pw.login
                mycursor = mydb.cursor()
                sql1 = "INSERT INTO users (user_id, username, first_name, last_name, lang, grade, sub) VALUES (%s, %s, %s, %s, %s, %s, 1)"
                val1 = (u_id, u_username, u_first_name, u_last_name, u_lang, '')
                mycursor.execute(sql1, val1)
                mydb.commit()
                mycursor.close()
            except:
                logging.error('Error commiting to database')
                ErrorNot("Commiting new user info to database")
            # Sends message to the bots admin containing the new user's information
            if settings.new_user_notification:
                bot.send_message(chat_id=settings.admin_id, text="New User:\n"
                + "id: {} \n".format(u_id)
                + "username: {} \n".format(u_username)
                + "first name: {} \n".format(u_first_name)
                + "last name: {} \n".format(u_last_name)
                + "lang: {}".format(u_lang))
        else:
            mycursor.close()

    except:
        logging.error('Error in start()')
        ErrorNot("Error in start()")
    context.bot.send_message(chat_id=update.effective_chat.id, text=settings.welcome_message,parse_mode=telegram.ParseMode.MARKDOWN)

# if the bot runs into problems, it sends a message to the bots admin
def ErrorNot(source):
    bot.send_message(chat_id=settings.admin_id, text="Error: " + source)
    logging.info("Sent error Notification")

# Lets users subscribe to the newsletter
def subscribe(update,context):
    try:
        mydb = pw.login
        mycursor = mydb.cursor()
        u_id = str(update.message.from_user.id)
        #sql = "UPDATE users SET sub = 1 WHERE user_id = '{}'".format(u_id)
        mycursor.execute("UPDATE users SET sub = 1 WHERE user_id = '{}'".format(u_id))
        mydb.commit()
        mycursor.close()
        logging.info('{} subscribed to newsletter'.format(u_id))
        context.bot.send_message(chat_id=update.effective_chat.id,
        text=settings.subscribe_message,parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        logging.error('Failed subscribing to newsletter')

# Lets users unsubscribe from newsletter
def unsubscribe(update,context):
        try:
            mydb = pw.login
            mycursor = mydb.cursor()
            u_id = str(update.message.from_user.id)
            #sql = "UPDATE users SET sub = 1 WHERE user_id = '{}'".format(u_id)
            mycursor.execute("UPDATE users SET sub = 0 WHERE user_id = '{}'".format(u_id))
            mydb.commit()
            mycursor.close()
            logging.info('{} unsubscribed from newsletter'.format(u_id))
            context.bot.send_message(chat_id=update.effective_chat.id,
            text="settings.unsubscribe_message)
        except:
            logging.error('Failed unsubscribing from newsletter')

# let users set the string they want to be notified if its in the pdf
def grade(update,context):
    u_id = str(update.message.from_user.id)
    args = context.args
    mydb = pw.login
    mycursor = mydb.cursor()
    if len(args) == 0:
        mycursor.execute("SELECT * FROM users WHERE user_id='{}'".format(u_id))
        records = mycursor.fetchall()
        for row in records:
            # if no string has been set yet
            if row[6] == "":
                context.bot.send_message(chat_id=update.effective_chat.id, text="settings.grade_message_new,parse_mode=telegram.ParseMode.MARKDOWN)
            # sends users their current string
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=settings.grade_message_current + row[6]
                + settings.grade_message_current_reset,parse_mode=telegram.ParseMode.MARKDOWN)
        mycursor.close()
    elif len(args) == 1:
        # resets users string
        if args[0] == "reset":
            mycursor.execute("UPDATE users SET grade = '' WHERE user_id = '{}'".format(u_id))
            mydb.commit()
            logging.info('{}: Reset grade'.format(u_id))
            context.bot.send_message(chat_id=update.effective_chat.id, text=settings.grade_message_reset,parse_mode=telegram.ParseMode.MARKDOWN)
        # sets users string
        else:
            u_grade = args[0]
            mycursor.execute("UPDATE users SET grade = '{}' WHERE user_id = '{}'".format(u_grade, u_id))
            mydb.commit()
            logging.info('{}: Set grade to {}'.format(u_id, u_grade))
            context.bot.send_message(chat_id=update.effective_chat.id, text=settings.grade_message_new + u_grade
            + settings.grade_message_reset,parse_mode=telegram.ParseMode.MARKDOWN)
        mycursor.close()
    elif len(args) > 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text=settings.grade_message_too_many_arguments)

# sends the given file to the given userid
def send_v(u_id, v_file):
    bot.sendChatAction(chat_id=u_id, action="upload_document")
    bot.send_document(chat_id=u_id, document=open(v_file, 'rb'))

# Manually request file
def PDF(update, context):
    u_id = str(update.message.from_user.id)
    v_prm = 'v/v.pdf'
    logging.info("{}: /PDF".format(u_id))
    bot.send_document(chat_id=u_id, document=file)

# Resends user's message back to them if it's no command
def echo(update, context):
    u_id = str(update.message.from_user.id)
    m_text = update.message.text
    context.bot.send_message(chat_id=u_id, text=m_text)
    logging.info("{}: '{}'".format(u_id, m_text))

# lists all commands
def help(update,context):
    logging.info("{}: /help".format(update.message.from_user.id))
    context.bot.send_message(chat_id=update.effective_chat.id,text=settings.help_message,parse_mode=telegram.ParseMode.MARKDOWN)

#handler
start_handler = CommandHandler('start', start)
PDF_handler = CommandHandler('PDF', PDF)
sub_handler = CommandHandler('subscribe', subscribe)
unsub_handler = CommandHandler('unsubscribe', unsubscribe)
echo_handler = MessageHandler(Filters.text, echo)
help_handler = CommandHandler('help', help)
grade_handler = CommandHandler('grade', grade)

#dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(PDF_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(sub_handler)
dispatcher.add_handler(unsub_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(grade_handler)

print("\n" + "--- Bot up and running ---")
bot_username = str(bot.get_me().username)
bot_first_name = str(bot.get_me().first_name)
bot_id = str(bot.get_me().id)
print("username:    " + bot_username)
print("first_name:  " + bot_first_name)
print("id:          " + bot_id)
print("-----" + "\n")

check()
updater.start_polling()
