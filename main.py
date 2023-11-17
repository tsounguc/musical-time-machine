from pprint import pprint

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os

client_id = os.environ.get("client_id", "Message")
client_secret = os.environ.get("client_secret", "Message")

date = input("Which Year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, 'html.parser')

songs = soup.find_all(name="div", class_="o-chart-results-list-row-container")

song_titles = [song.find(name="h3").getText().strip() for song in songs]

print(song_titles)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=f"{client_id}",
                                               client_secret=f"{client_secret}", redirect_uri="http://example.com", scope="playlist-modify-public"))

current_user_id = sp.current_user()['id']
playlist = sp.user_playlist_create(user=current_user_id, name=f"{date} Billboard 100",)
print(playlist)
uri_list = []
for title in song_titles:
    result = sp.search(q=f"track:{title} year:{date.split("-")[0]}", type="track", limit=3)
    # pprint(result['tracks']["items"][0])
    try:
        uri = result['tracks']["items"][0]['uri']
        uri_list.append(uri)
    except IndexError:
        print(f"{title} Doesn't exist in Spotify. Skipped")

sp.playlist_add_items(playlist_id=playlist['id'], items=uri_list)
