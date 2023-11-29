from html.parser import HTMLParser
import urllib.request
from datetime import datetime, date

# class that inherits from HTMLParser which is used to parse HTML documents
class WeatherScraper(HTMLParser):
    def __init__(self, year, month):
        super().__init__()
        self.inside_tbody = False # A flag to track if the parser is within a 'tbody' tag
        self.year = year # Year for the data to scrape
        self.month = month # Month for the data to scrape
        self.weather_data = {} # Dictionary to store the scraped data
        self.td_data = [] # List to store data from each 'td' tag
        self.inside_div = False # A flag to track if the parser is within a 'div' tag
        self.inside_input = False  # A flag to track if the parser is within an 'input' tag
        self.month_value = "" # Variable to store the month value extracted
        self.year_value = "" # Variable to store the year value extracted
        self.input_data = [] # List to store data from each 'input' tag

    # Method to handle the start of a tag
    def handle_starttag(self, tag, attrs):
        if tag == 'tbody':
            self.inside_tbody = True # Set the flag to True if inside 'tbody'
        elif tag == 'tr' and self.inside_tbody:
            self.td_data = [] # Reset the list if a new 'tr' tag is encountered within 'tbody'

        if tag == "main":
            self.inside_div = True # Set the flag to True if inside a 'main' tag

        if tag == "h1":
            self.inside_input = True # Set the flag to True if inside an 'h1' tag

     # Method to handle the end of a tag
    def handle_data(self, data):
        if self.inside_tbody and "Legend" not in data: # Check if inside 'tbody' and data is not "Legend"
            clean_data = data.strip() # Strip the data of whitespace
            if clean_data: # If data is not empty after stripping
                self.td_data.append(clean_data) # Append the clean data to the list

        if self.inside_div == True and self.inside_input == True: # Check if inside 'div' and 'input'
            self.input_data.append(data) # Append the data to the input_data list

     # Method to handle the end of a tag
    def handle_endtag(self, tag):
        if tag == 'tr' and self.inside_tbody and len(self.td_data) >= 4: # Check if at the end of 'tr' within 'tbody' with enough data
            if self.td_data[0].isdigit(): # If the first element is a digit (day of month)
                try:
                    day = int(self.td_data[0])  # Convert the first element to an integer
                    date = datetime(self.year, self.month, day).strftime('%Y-%m-%d') # Format the date string
                    daily_temps = { # Create a dictionary of the temperatures
                        'Max': self.parse_temp(self.td_data[1]), # Parse the 'Max' temperature
                        'Min': self.parse_temp(self.td_data[2]), # Parse the 'Min' temperature
                        'Mean': self.parse_temp(self.td_data[3]) # Parse the 'Mean' temperature
                    }
                    self.weather_data[date] = daily_temps
                except ValueError:
                    pass  # If there's an error in date formatting, ignore it
                self.td_data = [] # Reset the td_data list for the next row
        if tag == "main":
            self.inside_div = False # Reset the flag when leaving the 'main' tag

        if tag == "h1":
            self.inside_input = False  # Reset the flag when leaving the 'h1' tag

     # A method to parse the temperature string
    def parse_temp(self, temp_str):
        
        try:
            return float(temp_str) if temp_str != 'M' else None # Convert temperature to float or None if 'M'
        except ValueError:
            return None # Return None if conversion to float fails

    # A method to print out the weather data
    def get_weather_data(self):

        for key, value in self.weather_data.items():
            print(key, value) # Print the date and the corresponding temperature data

    # A method to get the oldest year from the parsed input data
    def get_oldest_year(self):
        self.year_value = self.input_data[0].split()[5] # Split the input data and get the year value
        return int(self.year_value) # Return the year as an integer
    
    # A method to get the oldest month from the parsed input data
    def get_oldest_month(self):
         # A match-case statement to assign the month value based on string matching
        """ if self.input_data[0].split()[4] == "October":
            self.month_value = 10 """
        match self.input_data[0].split()[4]:
            case "January":
                self.month_value = 1
                return self.month_value
            case "February":
                self.month_value = 2
                return self.month_value
            case "March":
                self.month_value = 3
                return self.month_value
            case "April":
                self.month_value = 4
                return self.month_value
            case "May":
                self.month_value = 5
                return self.month_value
            case "June":
                self.month_value = 6
                return self.month_value
            case "July":
                self.month_value = 7
                return self.month_value
            case "August":
                self.month_value = 8
                return self.month_value
            case "September":
                self.month_value = 9
                return self.month_value
            case "October":
                self.month_value = 10
                return self.month_value
            case "November":
                self.month_value = 11
                return self.month_value
            case "December":
                self.month_value = 12
                return self.month_value # Return the month value

# The main block that gets executed when the script is run directly
if __name__ == "__main__":
    today = date.today()
    current_year = today.year  
    current_month = today.month

     # Set initial year and month for scraping
    year = 1900
    month = 1

    # Create an instance of the WeatherScraper
    scrape = WeatherScraper(year, month)

    # Format the URL with the specified parameters
    url = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={year}&Day=1&Year={year}&Month={month}"

    # Open the URL and read the HTML content
    with urllib.request.urlopen(url) as response:
        html = response.read().decode("utf-8")
    scrape.feed(html) # Feed the HTML content to the parser

     # Get the oldest year and month from the scraper
    oldest_year = scrape.get_oldest_year()
    oldest_month = scrape.get_oldest_month()

    year_scrape = current_year # Start scraping from the current year
    month_scrape = current_month # Start scraping from the current month

     # Loop through the years and months and scrape data
    while year_scrape >= oldest_year:
        #year = year - 1

        if month_scrape == 0:
            month_scrape = 12
        else:
            month_scrape = current_month
        while month_scrape != 0:
            scraper = WeatherScraper(year_scrape, month_scrape)
             # Format the URL with the specified parameters
            url = f'http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear={year_scrape}&Day=1&Year={year_scrape}&Month={month_scrape}'
            # Open the URL and read the HTML content
            with urllib.request.urlopen(url) as response:
                html = response.read().decode('utf-8')
            scraper.feed(html) # Feed the HTML content to the parser
            scraper.get_weather_data() # Print the scraped data
            month_scrape = month_scrape - 1 # Decrement the month
        year_scrape = year_scrape - 1 # Decrement the year
    
    input("Press Enter to exit...") # Wait for user input to exit