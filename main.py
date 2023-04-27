import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
Stock_APi_Key="96UVT2BWEADJX53O"
News_API="48e7638745a1452db4190b5fb249cc6d"
Acc_SID="AC4df8c91dcf66a0d494e136beb0d96ee1"
Auth_Token="d4e22b38848b064b17f3ddca848b0846"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
Stock_para={
    "function":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol":STOCK_NAME,
    "apikey":Stock_APi_Key
}

response=requests.get(STOCK_ENDPOINT,params=Stock_para)
data=response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in data.items()]
yesterday_data=data_list[0]
yest_clos_price=float(yesterday_data['4. close'])
print(yest_clos_price)

#TODO 2. - Get the day before yesterday's closing stock price
day_befyes=data_list[1]
day_befyes_clos=float(day_befyes['4. close'])
print(day_befyes_clos)
#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
Difference=round(abs(yest_clos_price-day_befyes_clos),2)
print(Difference)
#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_dif=(Difference/yest_clos_price)*100
print(percentage_dif)
#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if percentage_dif>1:
    print("Get News")
    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
if percentage_dif>1:
    News_para={
        "apiKey":News_API,
        "qInTitle": COMPANY_NAME

    }
    get_news=requests.get(NEWS_ENDPOINT,params=News_para)
    #print(get_news.json())
    articles=get_news.json()["articles"]
    #print(articles)


#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles=articles[:3]
    #print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles=[f"Headline: {article['title']}. \nBrief:{article['description']}" for article in three_articles]
    print(formatted_articles)
#TODO 9. - Send each article as a separate message via Twilio. 
    client=Client(Acc_SID,Auth_Token)
    for article in formatted_articles:
        message=client.messages.create(
            body=article,
            from_="+16206341231",
            to="+251945521489"
        )

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

