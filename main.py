import requests
import time
from datetime import datetime, timedelta
import csv
import psycopg2

# connect ot the database
try:
    # Establish a connection to the database
    connection = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",  # Host is set to localhost
        port="5432",       # Default PostgreSQL port
        database="temps"
    )
    cursor = connection.cursor()
    print("Connected to the database")


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
        if temperature >= 100:
            alert = 1
        else:
            alert = 0

        # add the temp and time to our database
        new_weather = (1, time_of_data, temperature, alert)
        insert_query = """ INSERT INTO fridge_temps (truck_id, time, temperature, alert) VALUES (%s, %s, %s, %s)"""
        cursor.execute(insert_query, new_weather)

        # Commit the changes to the database
        connection.commit()
        print("Record inserted successfully")

        return temperature


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
        # final product calls api every minute when over temp threshold; currently calling every 5 for demonstration purposes
        if temperature >= 100:
            delay = 5 * 60
            print("Alert! High Temperatures Detected")
            time.sleep(delay)

            for i in range(0, 2):
                temperature = write_weather()
                if temperature >= 100:
                    print("Alert! High Temperatures Detected")
                time.sleep(delay)

            # will lead to other functions to inform relevant parties of potential failures in final product
        else:
            delay = 15 * 60
            time.sleep(delay)

except(Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")




