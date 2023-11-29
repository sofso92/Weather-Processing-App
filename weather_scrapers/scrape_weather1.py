# Web Scraper :)

from html.parser import HTMLParser
import urllib.request
import pprint
from datetime import datetime, timedelta
import re

class WeatherScraper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tr_count = 0
        self.inside_tbody = False
        self.weather_data = {}  # This will store the final structured data
        self.current_date = None
        self.current_max_temp = None
        self.current_min_temp = None
        self.current_mean_temp = None
        self.current_year = None
        self.current_month = None
        self.end_of_data_flag = False

    def extract_date_from_url(self, url):
        # Regular expression pattern to find year, month, and day in the URL
        date_pattern = r"Year=(\d+)&Month=(\d+)&Day=(\d+)"
        match = re.search(date_pattern, url)
        if match:
            year, month, day = match.groups()
            return int(year), int(month), int(day)
        else:
            raise ValueError("URL does not contain a valid date format.")
    
    # def has_previous_month(self, html):
    #     # Check if the "nav-prev" id is present in the HTML
    #     if 'id="nav-prev"' in html:
    #         return True
    #     return False

    def start_scrape(self):
    
        # Start from today's date
        current_date = datetime.now()
        self.current_year = current_date.year
        self.current_month = current_date.month
        consecutive_missing_data_days = 0
        max_consecutive_missing_data_days = 400 
    
        
        while consecutive_missing_data_days < max_consecutive_missing_data_days:
            formatted_date = current_date.strftime('%Y-%m-%d')
            url = self.create_url(current_date)
            
            try:
                with urllib.request.urlopen(url) as response:
                    html = response.read().decode('utf-8')
                    self.feed(html)  # Feed HTML to the parser

                    # If temperature data was found for the current date, store it
                    if self.current_max_temp is not None or self.current_min_temp is not None or self.current_mean_temp is not None:
                        daily_temps = {
                            "Max": self.current_max_temp,
                            "Min": self.current_min_temp,
                            "Mean": self.current_mean_temp
                        }
                        self.weather_data[formatted_date] = daily_temps
                        print(f"Scraping data for {formatted_date}: {daily_temps}")
                        consecutive_missing_data_days = 0  # Reset the counter because data was found
                    else:
                        consecutive_missing_data_days += 1  # Increment the counter for missing data

                        # Reset the temperature data for the next date
                        self.current_max_temp = None
                        self.current_min_temp = None
                        self.current_mean_temp = None

            except urllib.error.HTTPError as e:
                print(f"HTTP Error encountered: {e.reason}")
                break
            
            # Go to the previous day
            current_date -= timedelta(days=1)

            if consecutive_missing_data_days >= max_consecutive_missing_data_days:
                print("End of data reached after multiple consecutive days with no data.")

    def create_url(self, date):
        # Update the current year and month before creating the URL
        self.current_year = date.year
        self.current_month = date.month
        # Dynamically create the URL based on the provided date
        return f'http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear={date.year}&EndYear={date.year}&Day={date.day}&Year={date.year}&Month={date.month}'


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
            # and "Sum" not in data and "Avg" not in data and "Xtrm" not in data and "Summary" not in data
            if "Legend" not in data:
                if data.strip():  # Only add non-empty data
                    self.td_data.append(data.strip())
                    # Identify Min, Max and Meant temp data by index position in td_data
                    # Max temperature position
                    if self.td_count == 2:  
                        self.current_max_temp = self.parse_temp(data.strip())
                    # Min temperature position
                    elif self.td_count == 3:  
                        self.current_min_temp = self.parse_temp(data.strip())
                    # Mean temperature position
                    elif self.td_count == 4:  
                        self.current_mean_temp = self.parse_temp(data.strip())
    
    def parse_temp(self, temp_str):
    # Check if the temperature string is a digit or 'M' for missing data
    # and handle it accordingly. If it's anything else (like '^'), return None
        if temp_str.isdigit():
            return float(temp_str)
        elif temp_str == 'M' or temp_str == '^':
            return None
        else:
            try:
                return float(temp_str)
            except ValueError:
                return None


    def handle_endtag(self, tag):
        if tag == 'tbody':
            self.inside_tbody = False
        elif tag == 'tr' and self.inside_tbody:
            # Ensure that you have collected date and temperature data
            if self.tr_count > 2 and len(self.td_data) >= 4:
                day = self.td_data[0]
                try:
                    # Convert day to a date object using the current month and year
                    date_obj = datetime(self.current_year, self.current_month, int(day))
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    # Create a dictionary for the day's temperatures
                    daily_temps = {
                        "Max": float(self.td_data[1]),
                        "Min": float(self.td_data[2]),
                        "Mean": float(self.td_data[3])
                    }
                    # Store the data in the weather_data dictionary
                    self.weather_data[formatted_date] = daily_temps
                except ValueError:
                    # This can happen if the conversion to an int or float fails
                    pass
                # Reset the td_data for the next row
                self.td_data = []


if __name__ == "__main__":
    myparser = WeatherScraper()
    myparser.start_scrape()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(myparser.weather_data)  # This will print the nested dictionary structure

# if __name__ == "__main__":
#     myparser = WeatherScraper()
#     pp = pprint.PrettyPrinter(indent=4)
#     with urllib.request.urlopen('http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5') as response:
#         html = response.read().decode('utf-8')
#     myparser.feed(html)
#     # pp.pprint(colours)
