# Importing custom modules and libraries
import customtkinter as ctk
from settings import *
from main_widgets import *

# Importing necessary modules for URL requests, JSON handling, and image processing
import urllib.request
import json
from weather_data import get_weather
from PIL import Image
from os import walk

# Importing Windows-specific libraries (optional)
try:
    from ctypes import windll, byref, sizeof, c_int
except ImportError:
    pass


# Main application class
class App(ctk.CTk):
    def __init__(self, current_data, forecast_data, city, country):
        # Initializing application data
        self.current_data = current_data
        self.forecast_data = forecast_data
        self.location = {'city': city, 'country': country}
        self.color = WEATHER_DATA[current_data['weather']]

        # Importing forecast images and animation
        self.forecast_images = [Image.open(f"images/{info['weather']}.png") for info in self.forecast_data.values()]
        self.today_animation = self.import_folder(self.color['path'])

        # Initializing the main application window
        super().__init__(fg_color=self.color['main'])
        self.title_bar_color(self.color['title'])
        self.geometry('550x250')
        self.minsize(550, 250)
        self.title('')
        self.iconbitmap('empty.ico')

        # Starting with the SmallWidget
        self.widget = SmallWidget(self, self.current_data, self.location, self.color, self.today_animation)

        # State variables and event binding
        self.height_break = 600
        self.width_break = 1000
        self.full_height_bool = ctk.BooleanVar(value=False)
        self.full_width_bool = ctk.BooleanVar(value=False)
        self.bind('<Configure>', self.check_size)
        self.full_width_bool.trace('w', self.change_size)
        self.full_height_bool.trace('w', self.change_size)

        # Running the application event loop
        self.mainloop()

    # Importing image folder and sorting images
    def import_folder(self, path):
        for _, __, image_data in walk(path):
            sorted_data = sorted(image_data, key=lambda item: int(item.split('.')[0]))
            image_paths = [path + '/' + item for item in sorted_data]

        images = [Image.open(path) for path in image_paths]
        return images

    # Setting the title bar color (Windows-specific)
    def title_bar_color(self, color):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(color)), sizeof(c_int))
        except AttributeError:
            pass

    # Handling window size changes
    def check_size(self, event):
        if event.widget == self:
            # Width
            if self.full_width_bool.get():
                if event.width < self.width_break:
                    self.full_width_bool.set(False)
            else:
                if event.width > self.width_break:
                    self.full_width_bool.set(True)

            # Height
            if self.full_height_bool.get():
                if event.height < self.height_break:
                    self.full_height_bool.set(False)
            else:
                if event.height > self.height_break:
                    self.full_height_bool.set(True)

    # Changing widget based on size and dimensions
    def change_size(self, *args):
        self.widget.pack_forget()

        # Max widget
        if self.full_height_bool.get() and self.full_width_bool.get():
            self.widget = MaxWidget(self,
                                    current_data=self.current_data,
                                    forecast_data=self.forecast_data,
                                    location=self.location,
                                    color=self.color,
                                    forecast_images=self.forecast_images,
                                    animation=self.today_animation)

        # Tall widget
        if self.full_height_bool.get() and not self.full_width_bool.get():
            self.widget = TallWidget(self,
                                     current_data=self.current_data,
                                     forecast_data=self.forecast_data,
                                     location=self.location,
                                     color=self.color,
                                     forecast_images=self.forecast_images,
                                     animation=self.today_animation)

        # Wide widget
        if not self.full_height_bool.get() and self.full_width_bool.get():
            self.widget = WideWidget(self,
                                     current_data=self.current_data,
                                     forecast_data=self.forecast_data,
                                     location=self.location,
                                     color=self.color,
                                     forecast_images=self.forecast_images,
                                     animation=self.today_animation)

        # Min widget
        if not self.full_height_bool.get() and not self.full_width_bool.get():
            self.widget = SmallWidget(self, self.current_data, self.location, self.color, self.today_animation)


# Application entry point
if __name__ == '__main__':
    # Retrieving location information from an API
    with urllib.request.urlopen("https://ipapi.co/json/") as url:
        data = json.loads(url.read().decode())
        city = data['city']
        country = data['country_name']
        latitude = data['latitude']
        longitude = data['longitude']

    # Retrieving weather information
    current_data = get_weather(latitude, longitude, 'metric', 'today')
    forecast_data = get_weather(latitude, longitude, 'metric', 'forecast')

    # Initializing the application
    App(current_data=current_data, forecast_data=forecast_data, city=city, country=country)
