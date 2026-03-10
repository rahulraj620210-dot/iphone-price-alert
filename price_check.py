import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import datetime
import os

EMAIL = "bhaiyamax080@gmail.com"
PASSWORD = "mkfk vzky gcbg qulo"

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
"User-Agent":
"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
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

# -------- ACTIVATION MAIL (ONLY ONCE) --------

if not os.path.exists("activated.txt"):

    send_mail(

    "Price Tracker Activated",

"""✅ Tracker start ho gaya hai

Har 5 minute price check hoga

Aur har din 7 PM report milegi
"""
    )

    open("activated.txt","w").close()

# -------- PRICE CHECK --------

report = ""

for product in products:

    try:

        r = requests.get(product["url"],headers=headers)

        soup = BeautifulSoup(r.text,"html.parser")

        price_text = soup.get_text()

        price = None

        for word in price_text.split():

            if "₹" in word:

                price = int(word.replace("₹","").replace(",",""))

                break

        if price:

            report += f"{product['name']} : ₹{price}\n"

            if "min" in product and "max" in product:

                if product["min"] <= price <= product["max"]:

                    send_mail(

                    "🔥 Price Drop Alert",

f"""
{product['name']}

Price : ₹{price}

Buy Now
{product['url']}
"""
                    )

            elif "max" in product:

                if price <= product["max"]:

                    send_mail(

                    "🔥 Price Drop Alert",

f"""
{product['name']}

Price : ₹{price}

Buy Now
{product['url']}
"""
                    )

    except:

        pass

# -------- DAILY REPORT --------

now = datetime.datetime.now()

if now.hour == 19 and now.minute < 5:

    send_mail(

    "📊 Daily Price Report",

report
                )
