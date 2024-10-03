import json
import requests
from datetime import datetime, timedelta
import re
import customtkinter as ctk




def extract_events_by_date(title, day):
   # Create a regex pattern to match the date in the format "Month Day, Year"
   day_str = day.strftime('%B %d, %Y').replace(' 0', ' ')  # Convert the date to string format
   title = title.replace('\u202f', ' ')
   # Create a regex pattern to match the specified date
   date_pattern = rf'\b({day_str})\b'
   # Split the title by commas to get individual events
   split_events = re.split(r'(?<=[AP]M),\s*', title)



   matching_events = []


   for event in split_events:


       # Check if the event contains a date that matches the specified day
       if day_str in event:
           if '12:00:00 AM' in event and '11:59:59 PM' in event:
               # Label the event as "All Day"
               temp_list = event.split('from')
               event = temp_list[0] + 'All Day'
           matching_events.append(event.strip())  # Append the matching event to the list


   return matching_events




def calendar_events(filename):
   with open(filename, 'r') as f:
       events = json.load(f)


   today_events = []
   today = datetime.now().date()  # Get today's date
   title = events[0]["title"]
   event_dates = extract_events_by_date(title, today)  # Extract events for today


   if event_dates:  # If there are matching events
       today_events.extend(event_dates)  # Add to today_events list


   return today_events




def upcoming_events(filename):
   """Retrieve upcoming events for tomorrow."""
   with open(filename, 'r') as f:
       events = json.load(f)


   upcoming = []
   tomorrow = (datetime.now().date() + timedelta(days=1))  # Get tomorrow's date


   title = events[0]["title"]
   event_dates = extract_events_by_date(title, tomorrow)  # Extract events for tomorrow


   if event_dates:  # If there are matching events
       upcoming.extend(event_dates)  # Add to upcoming list


   return upcoming




def get_weather(api_key, city):
   '''Fetch weather data from OpenWeatherMap API.'''
   base_url = "http://api.openweathermap.org/data/2.5/weather?"
   complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
   response = requests.get(complete_url)


   if response.status_code == 200:
       data = response.json()
       temp = data["main"]["temp"]
       temp_min = data["main"]["temp_min"]
       temp_max = data["main"]["temp_max"]
       weather_description = data["weather"][0]["description"]
       rain_last_hour = data.get("rain", {}).get("1h", 0)  # Rain in the last hour (in mm)
       snow_last_hour = data.get("snow", {}).get("1h", 0)  # Snow in the last hour (in mm)
       return temp, temp_min, temp_max, weather_description, rain_last_hour, snow_last_hour
   else:
       return None, None, None, "Unable to retrieve weather data.", None, None




def contains_cloud_or_cloudy(text):
   return "cloud" in text or "cloudy" in text or "clouds" in text




def get_greeting():
   current_hour = datetime.now().hour
   if current_hour < 12:
       return "Good Morning!"
   elif 12 <= current_hour < 18:
       return "Good Afternoon!"
   else:
       return "Good Evening!"




# Function to display a popup with events and weather
def show_popup(events, upcoming_events, weather_info):
    # Create a CustomTkinter window
    popup = ctk.CTk()
    popup.geometry("600x400")  # Set a larger initial size
    popup.title("Today's Events and Weather")

    # Set a custom theme color
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme(
        "/Users/julianambrose/PycharmProjects/Git_Projects/MyApp.app/Contents/CustomTkinter/customtkinter/assets/themes/dark-blue.json"
    )

    # Set the background color of the popup
    popup.configure(bg="#00A1F1")

    # Greeting label
    greeting_label = ctk.CTkLabel(popup, text=get_greeting(), font=("Helvetica Neue", 18, "bold"), text_color="white")
    greeting_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

    # Weather information
    temp, temp_min, temp_max, weather, rain_hr, snow_hr = weather_info
    rain_emoji = ''
    if rain_hr >= 0 and rain_hr < 0.5:
        rain_emoji = '☀️' if not contains_cloud_or_cloudy(weather) else '☁️'
    elif rain_hr >= 0.5 and rain_hr < 4:
        rain_emoji = '🌧'
    elif snow_hr > 0:
        rain_emoji = '❄️'
    else:
        rain_emoji = '☀️'

    weather_message = f"Condition: {weather}  {rain_emoji}\n"
    temp_message = f"Current Temperature: {round(temp, 0)}°C\n"

    weather_label = ctk.CTkLabel(popup, text=weather_message, font=("Helvetica Neue", 18), text_color="white")
    temp_label = ctk.CTkLabel(popup, text=temp_message, font=("Helvetica Neue", 18), text_color="white")
    weather_label.grid(row=1, column=0, columnspan=2, pady=(20, 10))
    temp_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))

    # Create two frames for today's and tomorrow's events
    today_frame = ctk.CTkFrame(popup, fg_color="#3B3B3B")
    tomorrow_frame = ctk.CTkFrame(popup, fg_color="#3B3B3B")

    today_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
    tomorrow_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

    # Events label
    today_events_label = ctk.CTkLabel(today_frame, text="Today's Events:", font=("Helvetica Neue", 14), text_color="white")
    today_events_label.pack(pady=(10, 5))

    # Message for today's events
    today_message = "\n".join(events) if events else "No events today."
    today_events_text = ctk.CTkTextbox(today_frame, width=250, height=150, text_color="white", fg_color="#3B3B3B")
    today_events_text.insert("0.0", today_message)
    today_events_text.pack(pady=(0, 10))

    # Tomorrow events label
    tomorrow_events_label = ctk.CTkLabel(tomorrow_frame, text="Tomorrow's Events:", font=("Helvetica Neue", 14), text_color="white")
    tomorrow_events_label.pack(pady=(10, 5))

    # Message for tomorrow's events
    tomorrow_message = "\n".join(upcoming_events) if upcoming_events else "No upcoming events tomorrow."
    tomorrow_events_text = ctk.CTkTextbox(tomorrow_frame, width=250, height=150, text_color="white", fg_color="#3B3B3B")
    tomorrow_events_text.insert("0.0", tomorrow_message)
    tomorrow_events_text.pack(pady=(0, 10))

    # OK button
    ok_button = ctk.CTkButton(popup, text="OK", command=popup.destroy, text_color="black")
    ok_button.grid(row=4, column=0, columnspan=2, pady=(20, 10))

    # Configure grid weights for resizing
    popup.grid_columnconfigure(0, weight=1)
    popup.grid_columnconfigure(1, weight=1)
    popup.grid_rowconfigure(3, weight=1)

    popup.mainloop()





# Main function
if __name__ == "__main__":
   api_key = "517f2e063325d8338f1a44c61b885064"  # Replace with your OpenWeatherMap API key
   city = "Montréal, CA"  # Replace with your city


   # Get today's events from the JSON file
   events = calendar_events('/Users/julianambrose/PycharmProjects/Git_Projects/MyApp.app/Contents/MacOS/calendar_events.json')


   # Get the current weather
   weather_info = get_weather(api_key, city)


   # Get upcoming events
   upcoming = upcoming_events('/Users/julianambrose/PycharmProjects/Git_Projects/MyApp.app/Contents/MacOS/calendar_events.json')


   # Show the popup
   show_popup(events, upcoming, weather_info)



