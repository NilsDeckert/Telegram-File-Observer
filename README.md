# Telegram-File-Observer
This Telegram bot periodically checks if the PDF of a given link has been updated. If so, the bot sends the updated file to
all of the bot's users who subscribed to the newsletter and logs the time and date of the update to a database. Users are also able to subscribe to a certain string and only receive a message if that string is contained in the PDF.

## Getting started
These instructions will get you a copy of the project up and running, ready to deploy on a live system.

## Prerequisites

* Python3

* MySQL database

* Telegram Bot (see: ["Bots: An introduction for developers"](https://core.telegram.org/bots#6-botfather))

---

## Installing

To install the necessary Python3 packages:
```
pip3 install -r requirements.txt
```

### Setup the MySQL tables:
```SQL
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` text COLLATE utf8_german2_ci NOT NULL,
  `username` text COLLATE utf8_german2_ci NOT NULL,
  `first_name` text COLLATE utf8_german2_ci NOT NULL,
  `last_name` text COLLATE utf8_german2_ci NOT NULL,
  `lang` text COLLATE utf8_german2_ci NOT NULL,
  `grade` text COLLATE utf8_german2_ci,
  `sub` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8 COLLATE=utf8_german2_ci
```
```SQL
CREATE TABLE `updates_time` (
  `date` date NOT NULL,
  `time` time NOT NULL,
  `day` text COLLATE utf8_german2_ci NOT NULL,
  `file_size_kb` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_german2_ci 
```
```SQL
CREATE TABLE `updates_date` (
  `date` date NOT NULL,
  `day` text COLLATE utf8_german2_ci NOT NULL,
  `updates` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_german2_ci
```
after that, fill the **config/mysql_pw.py** with your database's credentials:
```Python
import mysql.connector
from mysql.connector import errorcode
login = mysql.connector.connect(#MySQL login details
        host="HOST_ADDRESS", #eg localhost
        port="3306",
        user="MYSQL_USER",
        passwd="USERS_PASSWORD",
        database="DATABASE_NAME"
)

```

### Connect your Telegram Bot:
Now add your bot's token to the **config/telegram_pw.py**:
```Python
import telegram
from telegram.ext import Updater

bot = telegram.Bot(token="ENTER_YOUR_TOKEN_HERE")
updater = Updater(token="ENTER_YOUR_TOKEN_HERE", use_context=True)
```

## Customizing the bot:
See **config/setting.py** to adapt the bot to your wishes. You should add your own userid to:
```Python
# admin user id
admin_id = "000000000"
```
## Authors:

* **Nils Deckert** - *Initial work* - [NilsDeckert](https://github.com/NilsDeckert)
