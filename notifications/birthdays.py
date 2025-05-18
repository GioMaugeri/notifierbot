import datetime

def check_birthdays(events):
    tz = pytz.timezone("Europe/Rome")
    today = datetime.now(tz).strftime("%Y-%m-%d")
    print(f"🎂 Oggi in Italy è: {today}")
    messages = []
    for event in events:
        if event["type"] == "birthday" and event["date"][5:] == today:
            messages.append(f"🎉 Oggi è il compleanno di {event['name']}!")
    return messages