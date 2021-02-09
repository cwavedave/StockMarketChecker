import requests
import datetime as dt
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

ALPHA_API = os.environ.get('ALPHA_API')
NEWS_API = os.environ.get('NEWS_API')

params = {
    'function':'TIME_SERIES_DAILY',
    'symbol':STOCK,
    'apikey': ALPHA_API
}

response = requests.get('https://www.alphavantage.co/query',params=params)
response.raise_for_status()

stock_data = response.json()
time_series_daily = stock_data['Time Series (Daily)']

now = dt.datetime.now()
yesterday = now - dt.timedelta(1)

yesterday_str = yesterday.strftime('%Y-%m-%d')
now_str = now.strftime('%Y-%m-%d')

if now_str in time_series_daily:
    print("Today has started")
else:
    open = float(time_series_daily[yesterday_str]['1. open'])
    close = float(time_series_daily[yesterday_str]['4. close'])

    print("Yesterday Open")
    print(time_series_daily[yesterday_str]['1. open'])

    print("Yesterday Close")
    print(time_series_daily[yesterday_str]['4. close'])

    print("Diff")
    if close > open:
        increase = close - open
        diff = round((increase / open) * 100,2)
        if diff > 5:
            print(f"Stock UP by {diff}%")
            print("Get News")

    elif open > close:
        decrease = open - close
        diff = (decrease / open) * 100
        diff = round(diff * -1,2)
        if diff < -5:
            print(f"stock DOWN by {diff}%")
            print("Get News")
    else:
        diff = 0
    print(f"{diff}%")

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

