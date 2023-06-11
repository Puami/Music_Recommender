import telebot
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

client_id = 'client id'
client_secret = 'client secret'


auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

TOKEN = 'token'



bot = telebot.TeleBot(TOKEN)
button1 = KeyboardButton("1")
button2 = KeyboardButton("2")
button3 = KeyboardButton("3")
return_button = KeyboardButton('return')
@bot.message_handler(commands=['return'])
def return_to_main_menu(message):
    start(message)


@bot.message_handler(commands=['start'])
def start(message):
    response = "Welcome to our song recommender bot!\n\nPlease select an option:\n\n" \
               "1. Search for musics\n" \
               "2. Our offer\n" \
               "3. About us\n"
  
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Search for musics")
    button2 = KeyboardButton("Our offer")
    button3 = KeyboardButton("About us")
    return_button = KeyboardButton('return')
    keyboard.add(button1, button2, button3)
    keyboard.add(return_button)
    
    bot.reply_to(message, response, reply_markup=keyboard)

  


@bot.message_handler(commands=['return'])
def return_to_main_menu(message):
    start(message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    if text == 'About us':
       response = "About us:\n\nWe are a company that provides..."
       keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
       keyboard.add(return_button)
       
    elif text == 'Our offer':
        response = "Our offer\n\n"
        top_musics = get_top_songs()
        response += top_musics
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(return_button)
        
    elif text == 'Search for musics':
        response = "Choose an option:\n\n" \
                   "1. Music suggestion\n" \
                   "2. Genre\n" \
                   "3. Singer\n"
        button1.text = "Music suggestion"
        button2.text = "Genre"
        button3.text = "Singer"
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(button1, button2, button3)
        keyboard.add(return_button)
        bot.register_next_step_handler(message, search_songs)

    elif text == 'return':
        response = "Returning to the main menu..."
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(return_button)
        bot.reply_to(message, response, reply_markup=keyboard)
        start(message)
        return
    else:
        response = "Invalid input !!!"
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(return_button)

    
    bot.reply_to(message, response, reply_markup=keyboard)
        

def search_songs(message):
    text = message.text
    if text == "Music suggestion":
        response = "Enter the music name:\n"
        bot.reply_to(message, response)
        bot.register_next_step_handler(message, search_by_music)
    elif text == 'Genre':
        response = "Enter the music genre:\n"
        bot.reply_to(message, response)
        bot.register_next_step_handler(message, search_by_genre)
    elif text == 'Singer':
        response = "Enter the singer name:\n"
        bot.reply_to(message, response)
        bot.register_next_step_handler(message, search_by_singer)
    elif text == 'return':
        response = "Returning to the main menu..."
        bot.reply_to(message, response)
        start(message)
    else:
        response = "Invalid input !!!"
        bot.reply_to(message, response)


def search_by_music(message):
    music_name = message.text

    results = sp.search(q='track:' + music_name, type='track', limit=1)

    if results['tracks']['items']:
        track_id = results['tracks']['items'][0]['id']

        recommendations = sp.recommendations(seed_tracks=[track_id], limit=5)

        if recommendations['tracks']:
            response = f"Recommended songs similar to '{music_name}':\n\n"
            for i, track in enumerate(recommendations['tracks'], 1):
                artist = track['artists'][0]['name']
                song_name = track['name']
                spotify_url = track['external_urls']['spotify']
                response += f"{i}. {song_name} - {artist}\n"
                response += f"   Listen on Spotify: {spotify_url}\n"
        else:
            response = f"No similar songs found for '{music_name}'."
    else:
        response = f"No songs found for '{music_name}'."

    bot.reply_to(message, response)



def search_by_genre(message):
    genre = message.text

    results = sp.search(q='genre:' + genre, type='track', limit=5)

    if results['tracks']['items']:
        response = f"Top 5 songs in the {genre} genre:\n\n"
        for i, track in enumerate(results['tracks']['items'], 1):
            artist = track['artists'][0]['name']
            song_name = track['name']
            spotify_url = track['external_urls']['spotify']
            response += f"{i}. {song_name} - {artist}\n"
            response += f"   Listen on Spotify: {spotify_url}\n"
    else:
        response = f"No songs found for the {genre} genre."

    bot.reply_to(message, response)




def search_by_singer(message):
    singer_name = message.text

    results = sp.search(q='artist:' + singer_name, type='artist', limit=1)

    if results['artists']['items']:
        artist_id = results['artists']['items'][0]['id']

        tracks = sp.artist_top_tracks(artist_id=artist_id)

        if tracks['tracks']:
            response = "Top tracks by {}:\n\n".format(singer_name)
            for i, track in enumerate(tracks['tracks'], 1):
                track_name = track['name']
                album_name = track['album']['name']
                spotify_url = track['external_urls']['spotify']
                response += "{}. {} - {}\n".format(i, track_name, album_name)
                response += "   Listen on Spotify: {}\n".format(spotify_url)
        else:
            response = "No tracks found for {}.".format(singer_name)
    else:
        response = "Artist not found: {}.".format(singer_name)

    bot.reply_to(message, response)


def get_top_songs():
    response = "Top 5 Songs in month:\n\n"
    results = sp.playlist_tracks("3cEYpjA9oz9GiPac4AsH4n", limit=10)
    for i, item in enumerate(results['items'], 1):
        track = item['track']
        artist = track['artists'][0]['name']
        song_name = track['name']
        spotify_url = track['external_urls']['spotify']
        response += f"{i}. {song_name} - {artist}\n"
        response += f"   Listen on Spotify: {spotify_url}\n"
    return response



bot.polling()
