import requests
import json
import os
from twilio.rest import Client

STOCK = "Meta"
COMPANY_NAME = "Meta"


# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": Alpha_Vantage_API,
    }

news_params = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API,
    "searchin": 'title',
}

## Collect the news articles for the stock in question
def get_news():
    news_request = requests.get(url=news_url, params=news_params)
    news_request.raise_for_status()
    articles = news_request.json()["articles"]
    three_articles = articles[:3]
    return three_articles

## Checking the stock price of the stock in question
def check_stock_change():
    r = requests.get(url=alphavantage_url, params=stock_params)
    r.raise_for_status()
    data = r.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[0]
    yyesterday_data = data_list[1]
    change = abs(float(yyesterday_data["4. close"]) - float(yesterday_data["4. close"])) / float(yyesterday_data["4. "
                                                                                                                 "close"])
    if change > 0.05:
        three_articles = get_news()
        formatted_articles = [f"Headline: {article['title']}. \nLink:{article['url']}" for article in three_articles]
        return formatted_articles


final_articles = check_stock_change()

## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.

client = Client(ACCOUNT_SID, AUTH_TOKEN)

if final_articles:
    for article in final_articles:
        message = client.messages \
                        .create(
                             body=article,
                             from_='+447723343826',
                             to='+447925119022'
                         )
        print(message.sid)


"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

