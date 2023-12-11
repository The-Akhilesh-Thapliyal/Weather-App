# Importing the necessary components and custom tkinter frame
from customtkinter import CTkFrame
from components import *

# Class for a small weather widget
class SmallWidget(CTkFrame):
    def __init__(self, parent, current_data, location, color, animation):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        # Setting up layout configurations
        self.rowconfigure(0, weight=6, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')

        # Creating and placing widgets within the frame
        SimplePanel(self, current_data, 0, 0, color, animation)
        DatePanel(self, location, 0, 1, color)

# Class for a wide weather widget
class WideWidget(CTkFrame):
    def __init__(self, parent, current_data, forecast_data, location, color, forecast_images, animation):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        # Setting up layout configurations
        self.rowconfigure(0, weight=6, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=2, uniform='a')

        # Creating and placing widgets within the frame
        SimplePanel(self, current_data, 0, 0, color, animation)
        DatePanel(self, location, 0, 1, color)
        HorizontalForecastPanel(self, forecast_data, 1, 0, 2, color['divider color'], forecast_images)

# Class for a tall weather widget
class TallWidget(CTkFrame):
    def __init__(self, parent, current_data, forecast_data, location, color, forecast_images, animation):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        # Setting up layout configurations
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure(0, weight=3, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')

        # Creating and placing widgets within the frame
        SimpleTallPanel(self, current_data, location, 0, 0, color, animation)
        HorizontalForecastPanel(self, forecast_data, 0, 1, 1, color['divider color'], forecast_images)

# Class for a maximum-sized weather widget
class MaxWidget(CTkFrame):
    def __init__(self, parent, current_data, forecast_data, location, color, forecast_images, animation):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        # Setting up layout configurations
        self.columnconfigure((0, 1), weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        # Creating and placing widgets within the frame
        SimpleTallPanel(self, current_data, location, 0, 0, color, animation)
        VerticalForecastPanel(self, forecast_data, 1, 0, color['divider color'], forecast_images)
