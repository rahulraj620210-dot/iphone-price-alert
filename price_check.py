import requests
from bs4 import BeautifulSoup
import smtplib

URL = "https://dl.flipkart.com/dl/apple-iphone-16-pro-desert-titanium-128-gb/p/itm5a8453e89cbd4"

TARGET_PRICE = 89000

headers = {
    "User-Agent": "Mozilla/5.0"
}

page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

price_text = soup.find("div", {"class": "_30jeq3"}).text
price = int(price_text.replace("₹","").replace(",",""))

print("Current price:", price)

if price <= TARGET_PRICE:

    sender_email = "rahulraj620210@gmail.com"
    password = "RAHULRAJ@999"

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()

    server.login(sender_email,password)

    message = f"""Subject:iPhone Price Alert

🔥 iPhone 16 Pro price dropped!

Current Price: ₹{price}

Buy Now:
{URL}
"""

    server.sendmail(sender_email,sender_email,message)

    server.quit()

    print("Alert sent!")