# ============================================================
# Python Dates and Time
# datetime module — working with dates, times, and differences
# ============================================================

from datetime import datetime, date, time, timedelta
import calendar

print("=== DATETIME MODULE ===")

# --- Creating Date Objects ---
print("\n--- Creating date objects ---")

today = date.today()
print(f"Today's date:  {today}")
print(f"Year:  {today.year}")
print(f"Month: {today.month}")
print(f"Day:   {today.day}")

# Specific date
birthday = date(2000, 6, 15)
print(f"\nSpecific date: {birthday}")

# Current date and time
now = datetime.now()
print(f"\nNow (datetime): {now}")
print(f"  Year:   {now.year}")
print(f"  Month:  {now.month}")
print(f"  Day:    {now.day}")
print(f"  Hour:   {now.hour}")
print(f"  Minute: {now.minute}")
print(f"  Second: {now.second}")

# Creating specific datetime
meeting = datetime(2025, 12, 31, 18, 30, 0)
print(f"\nNew Year's Eve meeting: {meeting}")

# Creating time object
alarm = time(7, 30, 0)
print(f"Alarm time: {alarm}")


# --- Date Formatting ---
print("\n=== DATE FORMATTING ===")

now = datetime.now()

# strftime — format datetime as string
print("--- strftime() formatting ---")
print(now.strftime("%Y-%m-%d"))              # 2025-04-28
print(now.strftime("%d/%m/%Y"))              # 28/04/2025
print(now.strftime("%B %d, %Y"))             # April 28, 2025
print(now.strftime("%A, %B %d, %Y"))         # Monday, April 28, 2025
print(now.strftime("%I:%M %p"))              # 12-hour format with AM/PM
print(now.strftime("%H:%M:%S"))              # 24-hour format
print(now.strftime("%d %b %Y %H:%M"))        # 28 Apr 2025 14:35

# Format codes reference
print("\n--- Common format codes ---")
codes = {
    "%Y": "4-digit year",
    "%m": "Month as number (01-12)",
    "%d": "Day of month (01-31)",
    "%H": "Hour 24h (00-23)",
    "%M": "Minute (00-59)",
    "%S": "Second (00-59)",
    "%A": "Weekday full name",
    "%B": "Month full name",
    "%I": "Hour 12h (01-12)",
    "%p": "AM or PM",
}
for code, desc in codes.items():
    print(f"  {code}  →  {desc}")

# strptime — parse string to datetime
print("\n--- strptime() parsing ---")
date_str = "2025-06-15"
parsed = datetime.strptime(date_str, "%Y-%m-%d")
print(f"Parsed '{date_str}' → {parsed}")
print(f"Type: {type(parsed)}")

date_str2 = "28 April 2025 14:30"
parsed2 = datetime.strptime(date_str2, "%d %B %Y %H:%M")
print(f"Parsed '{date_str2}' → {parsed2}")


# --- Calculating Time Differences ---
print("\n=== TIME DIFFERENCES ===")

# timedelta — represents a duration
print("--- timedelta examples ---")
delta = timedelta(days=7)
one_week_later = today + delta
print(f"Today:         {today}")
print(f"One week later: {one_week_later}")

# Days ago / from now
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
next_month = today + timedelta(days=30)
print(f"Yesterday:     {yesterday}")
print(f"Tomorrow:      {tomorrow}")
print(f"30 days later: {next_month}")

# Difference between two dates
start = date(2025, 1, 1)
end = date.today()
diff = end - start
print(f"\nDays since Jan 1, 2025: {diff.days} days")

# Age calculator
print("\n--- Age calculator ---")
birth_date = date(2000, 6, 15)
today = date.today()
age = today.year - birth_date.year - (
    (today.month, today.day) < (birth_date.month, birth_date.day)
)
print(f"Born: {birth_date}")
print(f"Age:  {age} years old")

# Countdown
print("\n--- Countdown to New Year ---")
new_year = datetime(today.year + 1, 1, 1)
now = datetime.now()
countdown = new_year - now
print(f"Days until New Year: {countdown.days} days")

# timedelta with hours and minutes
print("\n--- timedelta with hours ---")
event_start = datetime(2025, 5, 1, 9, 0)
event_duration = timedelta(hours=2, minutes=30)
event_end = event_start + event_duration
print(f"Event start: {event_start.strftime('%H:%M')}")
print(f"Event end:   {event_end.strftime('%H:%M')}")

# Calendar info
print("\n=== CALENDAR INFO ===")
print(f"Is 2024 a leap year? {calendar.isleap(2024)}")
print(f"Is 2025 a leap year? {calendar.isleap(2025)}")
print(f"Days in Feb 2024: {calendar.monthrange(2024, 2)[1]}")
print(f"Days in Feb 2025: {calendar.monthrange(2025, 2)[1]}")
