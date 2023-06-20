import requests
from bs4 import BeautifulSoup
import csv

csv_file_path = 'output.csv'

url = "https://www.gptm.nl/statistieken/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

calendarUrl = "https://gptm.nl/race_calendar/"
totalRacesResponse = requests.get(calendarUrl)
soupRacesResponse = BeautifulSoup(totalRacesResponse.text, "html.parser")

totalRaces = soupRacesResponse.find_all('span', class_='driver-number')
totalRaces = [span.text.strip() for span in totalRaces]
racesLength = int(len(totalRaces))

driver_names = soup.find_all('p', class_='driver-name')
points = soup.find_all('td', class_='points')
data_dict = {}

# Print the dictionary to a csv file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    for name, point in zip(driver_names, points):
        driver_name = name.text.strip().split()[-1]
        point_value = int(point.text.strip())
        averagePoints = int(point_value / racesLength)  # Format average points as an integer
        data_dict[driver_name] = averagePoints
        writer.writerow([driver_name, averagePoints])

print("CSV file has been created successfully.")