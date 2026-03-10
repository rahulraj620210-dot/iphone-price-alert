import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

URL = "https://www.flipkart.com/apple-iphone-16-pro-desert-titanium-128-gb/p/itm5a8453e89cbd4"

TARGET_PRICE = 89000

EMAIL = "rahulraj620210@gmail.com"
PASSWORD = "RAHULRAJ@999"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(URL, headers=headers, timeout=20)

soup = BeautifulSoup(response.text, "html.parser")

price_tag = soup.find("div", {"class": "Nx9bqj CxhGGd"})

if price_tag:
    price = int(price_tag.text.replace("₹","").replace(",",""))
    print("Current price:", price)

    if price <= TARGET_PRICE:

        msg = MIMEText(f"Price dropped to ₹{price}\n{URL}")
        msg["Subject"] = "iPhone Price Alert"
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, EMAIL, msg.as_string())
        server.quit()

        print("Email sent")

    else:
        print("Price still high")

else:
    print("Price not found")
