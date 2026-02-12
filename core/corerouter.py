import datetime

def needs_live_data(query):
    keywords = [
        "сейчас", "сегодня", "на данный момент",
        "новости", "курс", "цена",
        "кто сейчас", "что происходит",
        "актуально", "последние"
    ]
    return any(word in query.lower() for word in keywords)