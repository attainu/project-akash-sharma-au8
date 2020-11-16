# Bitcoin-Price-Notification
As we all know, Crypto Currency price is a fickle thing. You never really know where it's going to be at the end of the day. So, instead of constantly checking various sites for the latest updates, this project will send price notifications for every time interval and also notify whenever price reach to a certain threshold value provided.

## Project Overview
1. This Project will send notification of bitcoin latest price for every time interval.
2. The notifications will be sent to telegram channel https://t.me/bitCoinNoT
3. The notifications will be sent to email.
4. Used IFTTT for sending notification.
5. Used Flake 8 For linting the program file.

## Download
```
Download the file from the following link :-
https://github.com/project-akash-sharma-au8.git

(click on the "code" button on your right where you can clone or download ZIP)
```
## Getting Started

External Module Installation
```
pip install argparse (To get the input from the user)
pip install requests (To send HTTPS POST nad GET request)
```

## Help 

```
optional arguments:
  -h, --help            show this help message and exit
  -t THRESHOLD, --threshold THRESHOLD
                        Enter Threshold price for emergency Notification
  -i INTERVAL, --interval INTERVAL
                        Enter Time Interval in seconds
  -c COINTYPE, --coinType COINTYPE
                        Enter type of CryptoCurrency
  -u CURRENCY, --currency CURRENCY
                        Enter type of Currency
  -d DESTINATION, --destination DESTINATION
                        Enter where you want to send notification: Telegram or Email
 ```
 If the user did not provide above optional arguments then by default python will consider the below parameters.
 
 ```
 threshold = 10000
 interval = 1 (second)
 coinType = 'Bitcoin'
 currency = 'USD'
 destination = 'Telegram'
 ```
 
## How to Run
 
Go to the root folder where you have downloaded the file using command line.

Now type the following command:-

python bitcoin-price-notifier.py -t 10000 -i 1 -c Bitcoin -u USD -d Telegram 

where 
"-t" command line variable for threshold price
"-i" command line variable for time interval b/w notifications
"-c" command line variable for CryptoCurrency
"-u" command line variable for currency
"-d" command line variable for destination

and you can use variable/arguments of your choice.

## Work Flow and Description 

The general process to run the code and it will make an API calll to coinmarket API(https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest) to get the updated price of crypto currency and then it will show updated price on telegram or email.

If user provides coin type of crypto currncy then it will fetch the price for that coin type such as bitcoin, ethereum , litecoin etc.

If user did not provide type of coin type then it will fetch price for bitcoin by default.

This program will fetch price from API after every time interval provided by user.

If user provides type of currency then the program will fetch the price in that currency type such as INR,AUD, CAD etc

If user did not provide type of currency then it will fetch price in "USD" currency by default.

Now, to send notifications at certain time interval and also to send notification when price reach to a certain value as threshold value provided by users, this program use the automation website IFTTT.

IFTT("if this, then that") is a web service that bridges the gap between different apps and devices.

For that we need to create three IFTTT applets:

1. Regular telegram notifications on the crypto currency price(To send updates to telegram).
2. Emergency telegram notifications on the crypto currency price( To send updates to telegram).
3. Regular email notifications on the crypto currency price(To send updates to email).

Applet will be triggered by our python app which will consume the data from the coinmarket API.

An IFTTT applet is composed of two parts: a trigger and an action.

Our python app will make an HTTP request to webhook URL which will trigger an action.

There are two options for notification:
1) Telegram
2) E-mail

User can choose any option if user did not give any notification type then by default notification send to telegram

