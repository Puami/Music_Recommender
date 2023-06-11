import telebot

from models import Music

TOKEN = 'token'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['return'])
def return_to_main_menu(message):
    start(message)


@bot.message_handler(commands=['start'])
def start(message):
    response = "Welcome to our song recommender bot!\n\nPlease select an option:\n\n" \
               "1. Search for musics\n" \
               "2. Our offer\n" \
               "3. About us\n"

    bot.reply_to(message, response)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    if text == '3':
        response = "About us:\n\nWe are a company that provides..."
    elif text == '2':
        response = "Our offer - Top 10 Songs:\n\n"
        top_musics = get_top_musics()
        for i, music in enumerate(top_musics, 1):
            response += f"{i}. {music}\n"
    elif text == '1':
        response = "Search By:\n\n" \
                   "1. Music\n" \
                   "2. Genre\n" \
                   "3. Singer\n"
        bot.reply_to(message, response)
        bot.register_next_step_handler(message, search_songs)
    else:
        response = "Invalid input !!!"
    bot.reply_to(message, response)


def search_songs(message):
    text = message.text
    if text == '1':
        response = "Enter the music name:\n"
        # bot.reply_to(message, response)
        bot.register_next_step_handler(message, search_by_music)
    elif text == '2':
        response = "Enter the music genre:\n"
        # bot.reply_to(message, response)
        bot.register_next_step_handler(message, search_by_genre)
    elif text == '3':
        response = "Enter the singer name:\n"
        # bot.reply_to(message, response)
        bot.register_next_step_handler(message, search_by_singer)
    else:
        response = "Invalid input !!!"
    bot.reply_to(message, response)


def search_by_music(message):
    name = message.text
    try:
        music_genre = Music.select(Music.category).where(Music.name.contains(name))[0]
        qs = Music.select().where(Music.category == music_genre.category).order_by(Music.rate.desc()).limit(
            5).distinct()
        response = f"The best musics like '{name}':\n"
        for i, song in enumerate(qs, 1):
            response += f"{i}. {song.name}\n"
    except:
        response = "No results found"

    bot.reply_to(message, response)


def search_by_genre(message):
    genre = message.text
    qs = Music.select().where(Music.category == genre).order_by(Music.rate.desc()).limit(5).distinct()
    if qs.exists():
        response = f"The best musics in the genre of '{genre}':\n"
        for i, song in enumerate(qs, 1):
            response += f"{i}. {song.name}\n"
    else:
        response = "No results found"

    bot.reply_to(message, response)


def search_by_singer(message):
    singer = message.text
    qs = Music.select().where(Music.singer.contains(singer)).order_by(Music.rate.desc()).limit(5).distinct()
    if qs.exists():
        response = f"The best musics sung by '{singer}':\n"
        for i, song in enumerate(qs, 1):
            response += f"{i}. {song.name}\n"
    else:
        response = "No results found"

    bot.reply_to(message, response)


def get_top_musics():
    top_musics = list()
    qs = Music.select().order_by(Music.rate.desc()).limit(10).distinct()
    for music in qs:
        top_musics.append(music.name)
    return top_musics
