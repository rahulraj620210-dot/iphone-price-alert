import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import datetime
import os
import re
import json

EMAIL = "bhaiyamax080@gmail.com"
PASSWORD = "ryymqhgwolkemngv"

products = [

{
"name": "iPhone 16 Pro Flipkart",
"url": "https://dl.flipkart.com/dl/apple-iphone-16-pro-desert-titanium-128-gb/p/itm5a8453e89cbd4",
"min": 69999,
"max": 85000
},

{
"name": "iPhone 16 Pro JioMart",
"url": "https://www.jiomart.com/p/electronics/apple-iphone-16-pro-128-gb-natural-titanium/609946235",
"min": 69999,
"max": 85000
},

{
"name": "Samsung Galaxy S24 FE Flipkart",
"url": "https://www.flipkart.com/samsung-galaxy-s24-fe-5g-graphite-128-gb/p/itme960199e26f23",
"max": 32000
},

{
"name": "Samsung Galaxy S24 FE Amazon",
"url": "https://www.amazon.in/Samsung-Galaxy-Smartphone-Graphite-Storage/dp/B0DHL7YT5S",
"max": 32000
},

{
"name": "Samsung Galaxy S24 Ultra Flipkart",
"url": "https://www.flipkart.com/samsung-galaxy-s24-ultra-5g-titanium-gray-256-gb/p/itm12ef5ea0212ed",
"min": 60000,
"max": 85000
},

{
"name": "Samsung Galaxy S24 Ultra Amazon",
"url": "https://www.amazon.in/Samsung-Galaxy-Smartphone-Titanium-Storage/dp/B0CS5XW6TN",
"min": 60000,
"max": 85000
}

]

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
"Accept-Language":"en-IN,en;q=0.9",
"Connection":"keep-alive"
}

def send_mail(subject,body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(EMAIL,PASSWORD)

    server.sendmail(EMAIL,EMAIL,msg.as_string())

    server.quit()


def extract_price(text):

    prices = re.findall(r"₹\s?[\d,]+", text)

    if prices:
        p = prices[0].replace("₹","").replace(",","")
        return int(p)

    return None


price_memory_file = "price_memory.json"

if os.path.exists(price_memory_file):

    with open(price_memory_file) as f:
        price_memory = json.load(f)

else:
    price_memory = {}


# -------- ACTIVATION MAIL --------

if not os.path.exists("activated.txt"):

    send_mail(

    "Price Tracker Activated",

"""Tracker start ho gaya hai

Har 5 minute price check hoga

Price range match hua to instant alert

Daily report 7 PM
"""
    )

    open("activated.txt","w").close()


report = ""

for product in products:

    try:

        r = requests.get(product["url"],headers=headers,timeout=20)

        soup = BeautifulSoup(r.text,"html.parser")

        price = extract_price(soup.get_text())

        if price:

            report += f"{product['name']} : ₹{price}\n"

            last_price = price_memory.get(product["name"])

            alert = False

            if "min" in product and "max" in product:

                if product["min"] <= price <= product["max"]:

                    if last_price is None or price < last_price:
                        alert = True

            elif "max" in product:

                if price <= product["max"]:

                    if last_price is None or price < last_price:
                        alert = True


            if alert:

                send_mail(

                "🔥 Smart Price Drop Alert",

f"""
{product['name']}

Price : ₹{price}

Buy Now
{product['url']}
"""
                )

            price_memory[product["name"]] = price

    except:

        pass


with open(price_memory_file,"w") as f:

    json.dump(price_memory,f)


# -------- DAILY REPORT --------

now = datetime.datetime.now()

if now.hour == 19 and now.minute < 5:

    send_mail(

    "📊 Daily Price Report",

report
    )
