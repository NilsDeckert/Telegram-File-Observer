# link to file to observe
file = 'nils-deckert.de/files/testpdf.pdf'

# welcome message that is sent to new users
welcome_message = "*Welcome to my bot!* \nFeel free to play around with it."

# subscribe message, send whenever a user subscribes to the newsletter
subscribe_message = "You will now be sent the pdf as soon as it has been updated."

# unsubscribe message, send whenever a user unsubcribes from the newsletter
unsubscribe_message = "You will no longer receive updates of the file. Use /pdf to manually request the current file."

# message for /grade with no set string yet
grade_message_new = "*No update string set yet.* \nType '/grade YourUpdateString' to set the string you want know if it is in the file."


# message for /grade reset
grade_message_reset = "*Reset your string succesfully* \nYou will now receive messages for every file update."

# message for /grade with a string set
grade_message_current = "Your current string is: "
grade_message_current_reset = "\nType '/grade reset' to reset it."

# message for /grade and a new grade
grade_message_update = "String set to: "

# message for /grade and multiple arguments
grade_message_too_many_arguments = "You can only set one string!"

# command decriptions (/help)
help_message = "*You can use the following commands:*\n"
+ "/PDF: Sends you the latest version of the file\n"
+ "/unsubscribe: Unsubscribes from the file newsletter\n"
+ "/subscribe: Subscribes to the file newsletter  (Activated by default)\n"
+ "/grade: Set the string you want to know if it is in the file\n"
+ "/link: Sends you the link to this bot, so you can share it"

# Interval in which the file will be checked for changes (*in seconds*)
update_interval = 900

# Print message when bot found no changes in file
no_update_message = False

# admin user id
admin_id = "000000000"

# receive message for new users
new_user_notification = True
