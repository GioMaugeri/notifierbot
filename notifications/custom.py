import datetime

def check_custom(events):
    today = datetime.date.today().isoformat()
    messages = []
    for event in events:
        if event["type"] == "reminder" and event["date"] == today:
            messages.append(f"📌 {event['text']}")
    return messages