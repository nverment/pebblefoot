import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print(f"{i + 1 + playlists['offset']:4d} {playlist['uri']} {playlist['name']}")
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
