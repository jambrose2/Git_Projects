import json
import subprocess

from osascript import osascript


def get_calendar_events():
    apple_script = '''
    tell application "Calendar"
        set eventList to {}
        set today to current date
        repeat with cal in calendars
            repeat with ev in (every event of cal whose start date is greater than today and start date is less than today + 7 * days)
                set end of eventList to (summary of ev & " from " & start date of ev as string & " to " & end date of ev as string)
            end repeat
        end repeat
        return eventList
    end tell
    '''

    process = subprocess.Popen(['osascript', '-e', apple_script], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    events = output.decode('utf-8').strip().split('\n')
    return events

if __name__ == "__main__":
    events = get_calendar_events()
    event_data = [{"title": event} for event in events]

    # Write events to a JSON file
    with open('calendar_events.json', 'w') as f:
        json.dump(event_data, f, indent=4)
    print("Events stored successfully.")
