import requests
import time
from datetime import datetime, timedelta
import csv


def get_weather():
    # Define the API endpoint URL
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Phoenix,az,us&APPID=e690b6b8289cba128ff00c36f431373e&units=imperial'

    # Make a GET request to the API endpoint using requests.get()
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        weather = response.json()
        return weather
    else:
        print('Error:', response.status_code)
        return 0


def write_weather():
    new_weather = get_weather()

    # get the temperature and time to add to our log csv
    temperature = new_weather['main']['temp']
    time_of_data = datetime.now()
    if temperature >= 90:
        alert = 1
    else:
        alert = 0

    # add the temp and time to our log csv
    new_weather_csv = [1, time_of_data, temperature, alert]
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_weather_csv)

    return temperature

# initialize csv
weather_csv = ['truckid', 'time', 'temp', 'alert']

file_path = '/Users/nick/Documents/Willamette/Summer/Sales/poc/weather.csv'

# write data to CSV file
with open(file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(weather_csv)

csvfile.close()

# get a starting point:
starting_point = datetime.now()

# get the end time (24 hours from now, so we will have one days worth of observations)
ending_point = starting_point + timedelta(days=1)

# keep calling the api till the day has passed
while datetime.now() < ending_point:
    # get the weather
    temperature = write_weather()

    # if the temperature is over 90F, call the api every 5 minutes
    # else call it every 15 minutes
    #final product calls api every minute when over temp threshold; currently calling every 5 for demonstration purposes
    if temperature >= 90:
        delay = 5 * 60
        print("Alert! High Temperatures Detected")
        time.sleep(delay)

        for i in range(0,2):
            temperature = write_weather()
            if temperature >=90:
                print("Alert! High Temperatures Detected")
            time.sleep(delay)

        # will lead to other functions to inform relevant parties of potential failures in final product
    else:
        delay = 15 * 60
        time.sleep(delay)







