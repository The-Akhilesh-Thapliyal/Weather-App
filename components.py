# Importing necessary libraries and custom modules
import customtkinter as ctk
import datetime
import calendar
from image_widgets import *

# Panel class for a simple weather display
class SimplePanel(ctk.CTkFrame):
    def __init__(self, parent, weather, col, row, color, animation):
        super().__init__(master=parent, fg_color=color['main'], corner_radius=0)
        self.grid(column=col, row=row, sticky='nsew')

        # Setting layout configurations
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure((0, 1), weight=1, uniform='a')

        # Creating temperature and "feels like" labels
        temp_frame = ctk.CTkFrame(self, fg_color='transparent')
        ctk.CTkLabel(temp_frame, text=f"{weather['temp']}\N{DEGREE SIGN}",
                     font=ctk.CTkFont(family='Calibri', size=50), text_color=color['text']).pack()
        ctk.CTkLabel(temp_frame, text=f"feels like: {weather['feels_like']}\N{DEGREE SIGN}",
                     font=ctk.CTkFont(family='Calibri', size=16), text_color=color['text']).pack()
        temp_frame.grid(row=0, column=0)

        # Displaying an animated image
        AnimatedImage(self, animation, 0, 1, color['main'])

# Panel class for a vertically extended weather display
class SimpleTallPanel(ctk.CTkFrame):
    def __init__(self, parent, weather, location, col, row, color, animation):
        super().__init__(master=parent, fg_color=color['main'], corner_radius=0)
        self.grid(column=col, row=row, sticky='nsew')

        # Setting layout configurations
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure((0, 2, 4), weight=1, uniform='a')
        self.rowconfigure(1, weight=2, uniform='a')
        self.rowconfigure((3, 5), weight=6, uniform='a')

        # Retrieving date and time information
        day, weekday, suffix, month = get_time_info()

        # Creating temperature labels
        temp_frame = ctk.CTkFrame(self, fg_color='transparent')
        ctk.CTkLabel(temp_frame, text=f"{weather['temp']}\N{DEGREE SIGN}",
                     font=ctk.CTkFont(family='Calibri', size=50), text_color=color['text']).pack()
        ctk.CTkLabel(temp_frame, text=f"feels like: {weather['feels_like']}\N{DEGREE SIGN}",
                     font=ctk.CTkFont(family='Calibri', size=16), text_color=color['text']).pack()
        temp_frame.grid(row=5, column=0)

        # Creating frames for location and date information
        info_frame = ctk.CTkFrame(self, fg_color='transparent')
        info_frame.columnconfigure(0, weight=1, uniform='a')
        info_frame.rowconfigure((0, 1), weight=1, uniform='a')
        info_frame.grid(row=1, column=0)

        # Creating location information frame
        location_frame = ctk.CTkFrame(info_frame, fg_color='transparent')
        ctk.CTkLabel(location_frame, text=f"{location['city']}, ",
                     font=ctk.CTkFont(family='Calibri', size=20, weight='bold'),
                     text_color=color['text']).pack(side='left')
        ctk.CTkLabel(location_frame, text=f"{location['country']}",
                     font=ctk.CTkFont(family='Calibri', size=20),
                     text_color=color['text']).pack(side='left')
        location_frame.grid(column=0, row=0)

        # Creating date label
        ctk.CTkLabel(info_frame,
                     text=f"{weekday[:3]}, {day}{suffix} {calendar.month_name[month]}",
                     text_color=color['text'],
                     font=('Calibri', 18)).grid(column=0, row=1)

        # Displaying an animated image
        AnimatedImage(self, animation, 3, 0, color['main'])

# Panel class for displaying location and date information
class DatePanel(ctk.CTkFrame):
    def __init__(self, parent, location, col, row, color):
        super().__init__(master=parent, fg_color=color['main'], corner_radius=0)
        self.grid(column=col, row=row, sticky='nsew')

        # Creating location information frame
        location_frame = ctk.CTkFrame(self, fg_color='transparent')
        ctk.CTkLabel(location_frame, text=f"{location['city']}, ",
                     font=ctk.CTkFont(family='Calibri', size=20, weight='bold'),
                     text_color=color['text']).pack(side='left')
        ctk.CTkLabel(location_frame, text=f"{location['country']}",
                     font=ctk.CTkFont(family='Calibri', size=20),
                     text_color=color['text']).pack(side='left')
        location_frame.pack(side='left', padx=10)

        # Creating date label
        day, weekday, suffix, month = get_time_info()
        ctk.CTkLabel(self,
                     text=f"{weekday[:3]}, {day}{suffix} {calendar.month_name[month]}",
                     font=ctk.CTkFont(family='Calibri', size=20),
                     text_color=color['text']).pack(side='right', padx=10)

# Panel class for horizontally displaying weather forecast information
class HorizontalForecastPanel(ctk.CTkFrame):
    def __init__(self, parent, forecast_data, col, row, rowspan, divider_color, forecast_images):
        super().__init__(master=parent, fg_color='#FFF')
        self.grid(column=col, row=row, rowspan=rowspan, sticky='nsew', padx=6, pady=6)

        # Creating forecast widgets
        for index, info in enumerate(forecast_data.items()):
            frame = ctk.CTkFrame(self, fg_color='transparent')

            # Retrieving date information
            year, month, day = info[0].split('-')
            weekday = list(calendar.day_name)[datetime.date(int(year), int(month), int(day)).weekday()][:3]

            # Setting layout configurations
            frame.columnconfigure(0, weight=1, uniform='a')
            frame.rowconfigure(0, weight=5, uniform='a')
            frame.rowconfigure(1, weight=2, uniform='a')
            frame.rowconfigure(2, weight=1, uniform='a')

            # Creating forecast widgets
            StaticImage(frame, forecast_images[index], 0, 0)
            ctk.CTkLabel(frame, text=f"{info[1]['temp']}\N{DEGREE SIGN}", text_color='#444',
                         font=('Calibri', 22)).grid(row=1, column=0, sticky='n')
            ctk.CTkLabel(frame, text=weekday, text_color='#444').grid(row=2, column=0)
            frame.pack(side='left', expand=True, fill='both', padx=5, pady=5)

            # Adding divider line
            if index < len(forecast_data) - 1:
                ctk.CTkFrame(self, fg_color=divider_color, width=2).pack(side='left', fill='both')

# Panel class for vertically displaying weather forecast information
class VerticalForecastPanel(ctk.CTkFrame):
    def __init__(self, parent, forecast_data, col, row, divider_color, forecast_images):
        super().__init__(master=parent, fg_color='#FFF')
        self.grid(column=col, row=row, sticky='nsew', padx=6, pady=6)

        # Creating forecast widgets
        for index, info in enumerate(forecast_data.items()):
            frame = ctk.CTkFrame(self, fg_color='transparent')

            # Retrieving date information
            year, month, day = info[0].split('-')
            weekday = list(calendar.day_name)[datetime.date(int(year), int(month), int(day)).weekday()]

            # Setting layout configurations
            frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
            frame.rowconfigure(0, weight=1, uniform='a')

            # Creating forecast widgets
            StaticImage(frame, forecast_images[index], 0, 3)
            ctk.CTkLabel(frame, text=weekday, text_color='#444').grid(row=0, column=0, sticky='e')
            ctk.CTkLabel(frame, text=f"{info[1]['temp']}\N{DEGREE SIGN}", text_color='#444',
                         font=('Calibri', 22)).grid(row=0, column=2, sticky='e', padx=10)
            frame.pack(expand=True, fill='both', padx=5, pady=5)

            # Adding divider line
            if index < len(forecast_data) - 1:
                ctk.CTkFrame(self, fg_color=divider_color, height=2).pack(fill='x')

# Helper function to get date and time information
def get_time_info():
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day
    weekday = list(calendar.day_name)[datetime.datetime.today().weekday()]

    # Determining the suffix for the day
    match day % 10:
        case 1: suffix = 'st'
        case 2: suffix = 'nd'
        case 3: suffix = 'rd'
        case _: suffix = 'th'

    return day, weekday, suffix, month
