# Web Scraper :)

from html.parser import HTMLParser
import urllib.request
import pprint


class WeatherScraper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tr_count = 0
        self.inside_tbody = False

    def handle_starttag(self, tag, attrs):
        if tag == 'tbody':
            self.inside_tbody = True
        elif tag == 'tr' and self.inside_tbody:
            self.tr_count += 1
            self.td_count = 0  # Reset td_count for a new row
            self.td_data = []  # Reset td_data for a new row

        if tag == 'td' and self.inside_tbody:
            self.td_count += 1

    def handle_data(self, data):
        if self.tr_count and self.inside_tbody:
            if "Legend" not in data:
                if data.strip():  # Only add non-empty data
                    self.td_data.append(data.strip())

    def handle_endtag(self, tag):
        if tag == 'tbody':
            self.inside_tbody = False
        elif tag == 'tr' and self.inside_tbody:
            if len(self.td_data):
                formatted_data = ', '.join(
                    ['"{}"'.format(d) for d in self.td_data[:4]])
                print("Data:", formatted_data)


if __name__ == "__main__":
    myparser = WeatherScraper()
    pp = pprint.PrettyPrinter(indent=4)
    with urllib.request.urlopen('http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5') as response:
        html = response.read().decode('utf-8')
    myparser.feed(html)
    # pp.pprint(colours)
