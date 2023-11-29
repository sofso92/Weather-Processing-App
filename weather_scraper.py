from html.parser import HTMLParser
import urllib.request
from datetime import datetime, date

class WeatherScraper(HTMLParser):
    """
    WeatherScraper class inherits from HTMLParser and is used to scrape weather data
    from a specific URL for a given year and month.
    """
    def __init__(self, year, month):
        """
        Initializes the WeatherScraper object with the provided year and month.
        """
        super().__init__()
        self.inside_tbody = False
        self.year = year
        self.month = month
        self.weather_data = {} # Store scraped weather data
        self.td_data = [] # Store table data
        self.location_data = []  # Store the location information
        self.in_location_tag = False  # location tag bool

    def handle_starttag(self, tag, attrs):
        """
        Handles the start tags encountered while parsing the HTML content.
        """
        if tag == 'tbody':
            self.inside_tbody = True
        elif tag == 'tr' and self.inside_tbody:
            self.td_data = [] # Reset table data for each row

        if tag == 'p': # responsible for getting location
            self.in_location_tag = True

    def handle_data(self, data):
        """
        Handles the data encountered between HTML tags.
        """
        if self.inside_tbody and "Legend" not in data:
            clean_data = data.strip()
            if clean_data:
                self.td_data.append(clean_data)

        if self.in_location_tag: # responsible for getting location
            self.location_data.append(data.strip())

    def handle_endtag(self, tag):
        """
        Handles the end tags encountered while parsing the HTML content.
        """
        if tag == 'tr' and self.inside_tbody and len(self.td_data) >= 4:
            if self.td_data[0].isdigit():
                try:
                    # Extract date and temperature data
                    day = int(self.td_data[0])
                    date = datetime(self.year, self.month, day).strftime('%Y-%m-%d')
                    daily_temps = {
                        'Max': self.parse_temp(self.td_data[1]),
                        'Min': self.parse_temp(self.td_data[2]),
                        'Mean': self.parse_temp(self.td_data[3])
                    }
                    # Update weather_data dictionary with daily temperatures
                    self.weather_data.setdefault(date, {}).update(daily_temps)
                except ValueError as e:
                    print(e)
                    pass

        if tag == 'p' and self.in_location_tag: # responsible for extracting the location information from the parsed HTML
            self.in_location_tag = False  # Reset the flag when the location tag ends

    def parse_temp(self, temp_str):
        """
        Parses the temperature data.

        Returns:
        - float or None: Parsed temperature as a float or None if parsing fails.
        """
        try:
            return float(temp_str) if temp_str != 'M' else None
        except ValueError as e:
            print(e)
            return None
        
    def get_weather_data(self):
        """
        Prints the weather data sorted by date in descending order.
        """
        sorted_weather_data = sorted(self.weather_data.items(), key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'), reverse=True)
        for date, temp_data in sorted_weather_data:
            #print(f"Date: {date}, {temp_data}")
            location = ' '.join(self.location_data[:2]) if len(self.location_data) >= 2 else 'Location Not Found'
            print(f"Date: {date}, Location: {location}, Weather Data: {temp_data}")

if __name__ == "__main__":
    # Scraping weather data loop
    today = date.today()
    current_year = today.year  
    current_month = today.month

    oldest_year = 1840  # Replace with oldest year
    year_scrape = current_year

    while year_scrape >= oldest_year:
        month_scrape = current_month

        while month_scrape != 0:
            # The URL for weather data scraping
            url = f'http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={year_scrape}&Day=1&Year={year_scrape}&Month={month_scrape}'
            with urllib.request.urlopen(url) as response:
                html = response.read().decode('utf-8')
                
            # Initialize WeatherScraper instance and parse HTML content
            scraper = WeatherScraper(year_scrape, month_scrape)
            scraper.feed(html)

            # Print scraped weather data
            scraper.get_weather_data() 

            month_scrape -= 1 # Move to previous month
        year_scrape -= 1 # Move to previous year
    
    input("Press Enter to exit...")
