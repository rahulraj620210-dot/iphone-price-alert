import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

URL = "https://www.flipkart.com/apple-iphone-16-pro-desert-titanium-128-gb/p/itm5a8453e89cbd4"

TARGET_PRICE = 89000

EMAIL = "bhaiyamax080@gmail.com"
PASSWORD = "abcd efgh ijkl mnop"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# -------- TEST EMAIL --------

msg = MIMEText(
"✅ System working!\n\n"
"Price tracker activate ho gaya hai.\n"
"Ab jab price ₹89000 ya usse kam hoga tab main turant email bhej dungi."
)

msg["Subject"] = "iPhone Price Tracker Activated"
msg["From"] = EMAIL
msg["To"] = EMAIL

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL, PASSWORD)
server.sendmail(EMAIL, EMAIL, msg.as_string())
server.quit()

print("Test email sent")

# -------- PRICE CHECK --------

response = requests.get(URL, headers=headers, timeout=20)

soup = BeautifulSoup(response.text, "html.parser")

price_tag = soup.find("div", {"class": "Nx9bqj CxhGGd"})

if price_tag:

    price = int(price_tag.text.replace("₹","").replace(",",""))
    print("Current price:", price)

    if price <= TARGET_PRICE:

        msg = MIMEText(
        f"🔥 Price Drop Alert!\n\n"
        f"Current Price: ₹{price}\n\n"
        f"Buy now:\n{URL}"
        )

        msg["Subject"] = "iPhone Price Drop Alert"
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, EMAIL, msg.as_string())
        server.quit()

        print("Price alert email sent")

else:
    print("Price not found")
