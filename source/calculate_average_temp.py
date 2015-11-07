
import requests
import csv
import json
from time import gmtime, strftime
import numpy as np
import datetime

API_KEY = 'e85ba5b4f3c4366380d0f7c6fe8df683'

def calculate_degree(city, country):
    ''' Calculate Heating Degree Days (HDD), Cooling Degree Days (CDD)'''
    url = 'http://api.openweathermap.org/data/2.5/forecast?q={},{}&units=imperial&appid={}'.format(city, country, API_KEY)
    # today's date in YY-MM-DD format
    datetime_now = strftime("%Y-%m-%d", gmtime())
    r = requests.get(url)
    data = json.loads(r.text)['list']
    result = []
    for line in data:
        if datetime_now in line["dt_txt"]:
            #ignoring result for the present day
            pass
        else:
            #capture result for the next five days
            temp_max = line['main']['temp_max']
            temp_min = line['main']['temp_min']
            #Calculating the average of 3 hr period
            avg = float(temp_max + temp_min)/2
            result.append(avg)

    #ignoring the first value since that is not needed. It points to present day
    result.pop(0)
    return result

if __name__ == '__main__':

    city = raw_input("Enter the name of the city")
    country = raw_input("Enter the name of the country")

    avg_values = calculate_degree(city, country)
    avg_temp_day = [avg_values[i:i + 8] for i in range(0, len(avg_values), 8)]
    print avg_temp_day
    f = open('{}.txt'.format(city), 'wt')
    writer = csv.writer(f)
    writer.writerow(('DAY', 'HDD', 'CDD', 'CITY', 'COUNTRY'))
    count = 1
    for line in avg_temp_day:
        overall_avg_day = np.mean(line)
        energy_day = (datetime.date.today() + datetime.timedelta(days=count))
        date = "{}-{}-{}".format(energy_day.year, energy_day.month, energy_day.day)
        count += 1
        if overall_avg_day > 65:
            HDD = 0
            CDD = 65 - overall_avg_day
        else:
            CDD = 0
            HDD = 65 - overall_avg_day

        writer.writerow((date, HDD, CDD, city.upper(), country.upper()))

    f.close()

