# Uses API data to determine ISS location in relation to API nighttime data
# to notify you via email if the ISS is visible in your location, refreshes every minute while program is running.

import time
import requests
from datetime import datetime
import smtplib

EMAIL = "YOUR EMAIL HERE"
PASSWORD = "YOUR PASSWORD HERE"
EMAIL_SMTP = "YOUR EMAIL SERVER HERE"

MY_LAT = 33.770577  # YOUR LATTIDTUDE HERE
MY_LONG = -118.177094  # YOUR LONGITUTDE HERE

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


def iss_above():
    if (MY_LAT - 5) <= iss_latitude <= (MY_LAT + 5) and (MY_LONG - 5) <= iss_longitude <= (MY_LONG + 5):
        return True
    else:
        return False


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now().hour


while True:
    if iss_above() and sunset <= time_now <= sunrise:
        with smtplib.SMTP(EMAIL_SMTP) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL,
                                to_addrs=EMAIL,
                                msg="Subject: Go Outside\n\nLook up the ISS is above you!"
                                )
    else:
        print("ISS is not visible right now.")
    time.sleep(60)
