import requests
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import argparse
from datetime import datetime
import time

Telegram_applet = "coin_price_telegram"
Telegram_emergency_applet = "coin_emergency_price_telegram"

Email_applet = "coin_price_email"

ifttt_webhooks_url = 'https://maker.ifttt.com/trigger/{destination_type}/with/key/FxXkblst8aNIFLhr36jgi'


def get_crypto_price(coinType, currency):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': currency
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '32fe56dc-a110-4ca6-89cb-2482c2737a1b',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        data = data['data']
        new_obj = ''
        for x in data:
            if (x['name'].lower() == (coinType).lower()):
                new_obj = x
                break
        if (new_obj != ''):
            price = round(float(new_obj['quote'][currency]['price']), 2)
            date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

            return [date, price, currency]

        else:
            print("Invalid coinType entered")
            return None
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def push_ifttt_notification(destination, data):
    if(destination == 'telegram'):
        ifttt_destination_link = ifttt_webhooks_url.format(
            destination_type=Telegram_applet)

    elif(destination == 'telegram_emergency'):
        ifttt_destination_link = ifttt_webhooks_url.format(
            destination_type=Telegram_emergency_applet)

    elif(destination == 'email'):
        ifttt_destination_link = ifttt_webhooks_url.format(
            destination_type=Email_applet)
    else:
        print("Please enter valid destination type")
        return

    requests.post(ifttt_destination_link, json=data)
# function for fetch crypto data and send to telegram and email via post
# request


def send_data(threshold, interval, coinType, currency, destination):
    arr = []
    while True:
        date, price, currency = get_crypto_price(coinType, currency)
        print(date, currency, price)

        if price:
            if(price < float(threshold)):
                data = {'value1': coinType + " Emergency update",
                        'value2': price,
                        }
                print(data)

                # Triggering IFTTT
                push_ifttt_notification(destination.lower()+"_emergency", data)
                return

            crypto_updated_data = "{}: {} {}".format(date, currency, price)
            arr.append(crypto_updated_data)

            # send latest five prices in given time intervals

            if (len(arr) == 5):
                arr = "<br>".join(arr)

                data = {"value1": "Latest " + coinType + " Price Update",
                        "value2": arr
                        }
                push_ifttt_notification(destination.lower(), data)

                arr = []
                print("Check your " + destination)
                return

            time.sleep(interval)

        else:
            print("No Price data found")
            break


def main():

    parser = argparse.ArgumentParser()
    # command line variable for threshold price
    parser.add_argument("-t", "--threshold",
                        nargs=1,
                        default=[10000],
                        help='''Enter Threshold price for emergency
                        Notification''')
    # command line variable for time interval b/w notifications
    parser.add_argument("-i", "--interval",
                        type=int,
                        nargs=1,
                        default=[1],
                        help=" Enter Time Interval in seconds")
    # command line variable for CryptoCurrency
    parser.add_argument("-c", "--coinType",
                        nargs=1,
                        default=['Bitcoin'],
                        help="Enter type of CryptoCurrency")

    # command line variable for currency
    parser.add_argument("-u", "--currency",
                        nargs=1,
                        default=['USD'],
                        help="Enter type of Currency")

    # command line variable for destination
    parser.add_argument("-d", "--destination",
                        nargs=1,
                        default=['telegram'],
                        help='''Enter where you want to send notification:
                        Telegram or Email''')

    # Read arguments from command line
    new_args = parser.parse_args()

    interval = new_args.interval[0]
    threshold = new_args.threshold[0]
    coinType = new_args.coinType[0]
    currency = new_args.currency[0].upper()
    destination = new_args.destination[0]
    print('Running A Program with Interval of =', interval, "Seconds.",
          'threshold =', threshold,
          'coinType =', coinType,
          'currency =', currency,
          'destination =', destination)
# calling functions
    send_data(threshold, interval, coinType, currency, destination)


if __name__ == '__main__':
    main()
