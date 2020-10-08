from datetime import date
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


PAGE_LOADING_TIME = 2


def date_generator(from_date: date, to_date: date):
    current_date = from_date
    while current_date < to_date:
        yield current_date
        current_date += relativedelta(days=1)


def get_url(date: date):
    return f"https://www.wunderground.com/history/daily/ua/lviv/UKLL/date/{date}"


browser = webdriver.Firefox()


from_date = date(2020, 7, 16)  # parse(input('Enter start date in format yyyy-mm-dd: ')).date()
to_date = date(2020, 7, 17)  # parse(input('Enter end date in format yyyy-mm-dd: ')).date()
assert to_date <= date.today(), "We cannot jump to The Future yet :("

f = open(f'data/ua_lviv_UKLL_{from_date}_{to_date}.csv', 'w')
f.write(
    'day/month;Time;Temperature;Dew Point;Humidity;Wind;Wind Speed;Wind Gust;Pressure;Precip.;Precip Accum;Condition\n'
)
for day in date_generator(from_date, to_date):
    loading_time = PAGE_LOADING_TIME
    while True:
        try:
            browser.get(get_url(day))
            time.sleep(loading_time)
            bs = BeautifulSoup(browser.page_source, 'html.parser')
            table_container = bs.find('div', {'class': 'observation-table ng-star-inserted'})
            table = table_container.find('table')
        except Exception as e:
            print(e)
            loading_time += 1
        else:
            break
    table_body = table.find('tbody')
    day_month = day.strftime('%-d.%b')
    for table_row in table_body.find_all('tr'):
        csv_row = [day_month]
        for table_cell in table_row.find_all('td'):
            csv_row.append(table_cell.find('span').text)
        f.write(';'.join(csv_row))
        f.write('\n')

browser.close()
f.close()
