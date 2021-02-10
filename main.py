import requests
import datetime as dt
import os
from newsapi import NewsApiClient

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_API = os.environ.get('ALPHA_API')
NEWS_API = os.environ.get('NEWS_API')

#NEWS
newsapi = NewsApiClient(api_key=NEWS_API)

#/v2/top-headlines
top_headlines = newsapi.get_top_headlines(q=COMPANY_NAME,
                                          sources='bbc-news,the-verge, cnn, financial-post, fox-news,google-news,crypto-coins-news, business-insider, cbs-news, fortune, hacker-news, msnbc, nbc-news, politicio, reddit-r-all, reuters, techcrunch, the-huffington-post, the-next-web,the-verge, the-wall-street-journal, time,wired',
                                          language='en',)

sources = newsapi.get_sources()
number_of_articles = len(top_headlines['articles'])

articles = top_headlines['articles']

news_today = []

for source in articles[:3]:
    news_today.append({'name':source['source']['name'],
                       'author':source['author'],
                       'title': source['title'],
                        'content':source['content']})

#STOCK

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
    print(news_today[0])
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
            print(f"{STOCK}: ⬆️️ {diff}%")
            print(f"Headline:{news_today[0]['title']}")
            print(f"Brief:{news_today[0]['content']}")

    elif open > close:
        decrease = open - close
        diff = (decrease / open) * 100
        diff = round(diff * -1,2)
        if diff < -5:
            print(f"stock DOWN by {diff}%")
            print(f"{STOCK}: ⬇️ {diff}%")
            print(f"Headline:{news_today[0]['title']}")
            print(f"Brief:{news_today[0]['content']}")

    else:
        diff = 0
        print(f"{diff}%")
        print("No Change")
