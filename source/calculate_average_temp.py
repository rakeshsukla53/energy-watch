
import requests
import csv
import json
from time import gmtime, strftime
import datetime

API_KEY = 'e85ba5b4f3c4366380d0f7c6fe8df683'

def calculate_degree(city, country):
    ''' Calculate Heating Degree Days (HDD), Cooling Degree Days (CDD)'''
    url = 'http://api.openweathermap.org/data/2.5/forecast?q={},{}&units=imperial&appid={}'.format(city, country, API_KEY)
    # today's date in YY-MM-DD format
    datetime_now = strftime("%Y-%m-%d", gmtime())
    r = requests.get(url)
    # covert the response to json load
    data = json.loads(r.text)['list']
    # store the average of 3 hr period in a list
    result = []
    # iterate over all the whole data
    for line in data:
        if datetime_now in line["dt_txt"]:
            # ignoring result for the present day
            pass
        else:
            # capture result for the next five days
            temp_max = line['main']['temp_max']
            temp_min = line['main']['temp_min']
            # calculating the average of 3 hr period
            avg = float(temp_max + temp_min)/2
            result.append(avg)

    #ignoring the first value since that is not needed. It points to present day
    result.pop(0)
    return result

if __name__ == '__main__':
    # assumption is that you will enter correct city and country
    city = raw_input("Enter the name of the city")
    country = raw_input("Enter the name of the country")
    avg_values = calculate_degree(city, country)
    # divide the whole list in 5 equal parts which basically shows the average of 5 future days
    avg_temp_day = [avg_values[i:i + 8] for i in range(0, len(avg_values), 8)]
    # format of storing the file
    f = open('{}.txt'.format(city), 'wt')
    writer = csv.writer(f)
    # column header
    writer.writerow(('DAY', 'HDD', 'CDD', 'CITY', 'COUNTRY'))
    count = 1

    for line in avg_temp_day:
        # this is the overall average of the day
        overall_avg_day = reduce(lambda x, y: x + y, line) / float(len(line))
        energy_day = (datetime.date.today() + datetime.timedelta(days=count))
        date = "{}-{}-{}".format(energy_day.year, energy_day.month, energy_day.day)
        count += 1
        # logic for finding out the values of HDD and CDD
        if overall_avg_day > 65:
            HDD = 0
            CDD = overall_avg_day - 65
        else:
            CDD = 0
            HDD = 65 - overall_avg_day
        # writing the result to the file
        writer.writerow((date, HDD, CDD, city.upper(), country.upper()))
    f.close()

