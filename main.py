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
                                               client_secret=f"{client_secret}", redirect_uri="http://example.com"))

currentUser = sp.current_user()
print(currentUser['id'])

song_uri_list = []
for title in song_titles:
    result = sp.search(q=f"track:{title} year:{date.split("-")[0]}", type="track", limit=3)
    # pprint(result['tracks']["items"][0])
    try:
        uri = result['tracks']["items"][0]['uri']
        song_uri_list.append(uri)
    except IndexError:
        print(f"{title} Doesn't exist in Spotify. Skipped")

print(song_uri_list)
print(len(song_uri_list))
# for idx, track in enumerate(results['tracks']['items']):
#     # if year.split("-")[0] in track['release_date']:
#         print(f"{track['artists'][0]['name']} - {idx, track['name']} {track['release_date']}")
