import datetime

def check_birthdays(events):
    today = datetime.date.today().isoformat()[5:]
    messages = []
    for event in events:
        if event["type"] == "birthday" and event["date"][5:] == today:
            messages.append(f"🎉 Oggi è il compleanno di {event['name']}!")
    return messages