from menu import Menu
from weather_scraper import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations


class WeatherProcessor():
    def get_weather(self):
        scraper = WeatherScraper()

        db = DBOperations()
        # Conncet to the database.
        connection = db.open_connection("weather.sqlite")
        # Creates the cursor for the database.
        cursor = db.create_cursor(connection)
        # Create new table with data provided.
        TABLE_FORMAT = """create table samples
                            (id integer primary key autoincrement not null,
                            date text not null,
                            location text not null,
                            min_temp real not null,
                            max_temp real not null,
                            avg_temp real not null);"""
        db.create_table(connection, cursor, TABLE_FORMAT)
        # Insert SQL
        sql = """insert into samples (date,location,min_temp,max_temp,avg_temp)
                values (?,?,?,?,?)"""
        # db.insert_into(connection, cursor, sql, scraper.get_weather_data())
        print(scraper.get_weather_data())

    def update_weather(self):
        pass

    def generate_box_plot(self):
        year1 = input("Please enter a year... ")
        year2 = input("Please enter another year... ")
        scraper = WeatherScraper()
        data = scraper.get_weather_data(year1, year2)
        plot = PlotOperations()
        plot.create_boxplot(data)

    def generate_line_plot(self):
        year = input("Please enter a year... ")
        month = input("Please enter a month... ")
        scraper = WeatherScraper()
        data = scraper.get_weather_data(year, month)
        plot = PlotOperations()
        plot.create_lineplot(data)


weather_operations = WeatherProcessor()

main_menu = Menu(
    title="Welcome to weather processor! Please choose an operation:", prompt="→")
# sub_menu = Menu(title="Choose a photo to view:", prompt="→")

main_menu_options = []
main_menu_options.append(
    ("Get Weather", weather_operations.get_weather),
    ("Update Weather", weather_operations.update_weather),
    ("Generate Box Plot", weather_operations.generate_box_plot),
    ("Generate Line Plot", weather_operations.generate_line_plot))
main_menu_options.append(("Exit", Menu.CLOSE))
main_menu.set_options(main_menu_options)
main_menu.open()
