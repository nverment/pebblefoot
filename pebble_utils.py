from spotapi import PublicPlaylist
from ytmusicapi import YTMusic
from ytmusicapi.auth.browser import setup_browser
from mutagen.easyid3 import EasyID3 
import subprocess
import time
import sys
import os 

id='https://open.spotify.com/playlist/1fytm1VDA2xutq7FEn6lSm'

PP=1
DEBUG=0

with open('headers.txt', 'r') as f:
    setup_browser('browser.json', f.read())
yt = YTMusic('browser.json')

def cleanup_string(srg):
    cleaned = srg.replace(" - ", " ")
    cleaned = srg.replace(" | ", " ")
    if DEBUG and not (cleaned==srg):
        print(f"\t\t{srg}--> {cleaned}")
    return cleaned 

def fetch_tracklist(url):
    tracklist=[]
    playlist= PublicPlaylist(url)

    if "open.spotify.com/playlist" in url:
        print(f"Spotify URL detected.")
        info = playlist.get_playlist_info(343)
        items = info["data"]["playlistV2"]["content"]["items"]
        playlist_size = len(items)

        # the maximum .get_playlist_info() can handle at once is 343 songs
        if playlist_size >= 343:
           tracklist = handle_big_playlist(playlist)
           return tracklist

        print(f"\nTracklist Generated\n-------------------")
        i = 0
        for item in items:
            query = create_query(item)
            print(f"[{i+1:02d}] {query}")
            i += 1
            tracklist.append(query)
    else:
       sys.exit("Wrong URL format, try again.")
    return tracklist

def handle_big_playlist(playlist: str) -> list:
    tracklist=[]
    # paginate_playlist yields a generator so we turn it into a list for ease
    info = list(playlist.paginate_playlist())
    pages = []
    for page in info:
        pages.append(page["items"])

    print(f"\nTracklist Generated\n-------------------")
    i = 0
    for page in pages:
        for song in page:
            query = create_query(song)
            print(f"[{i+1:02d}] {query}")
            i += 1
            tracklist.append(query)

    return tracklist

def create_query(song: dict) -> str:
    title = cleanup_string(song["itemV2"]["data"]["name"])
    artist = cleanup_string(song["itemV2"]["data"]["artists"]["items"][0]["profile"]["name"])
    query = (f"{title} - {artist}")

    return query


def transfer_to_yt(url_list, folder):
    existing=input("NOTE: If the playlist already exists and you want to append songs to it, input its URL here. Else, press any key.\n")
    # existing="https://music.youtube.com/playlist?list=PLhBzAgL4DBIXPtuZkaeYJspigs_j_PZ0s"
    if "https://music.youtube.com/playlist?list=" in existing:
        playlist_id = yt.get_playlist(existing.split("=",1)[1])["id"]
        print(playlist_id)
    else:
        playlist_id = yt.create_playlist(title=folder, description='', privacy_status='public')

    for u in url_list[0]:
        if DEBUG:
            video_id = u[0].split("v=")[1]
        yt.add_playlist_items(playlist_id, [video_id])
        time.sleep(1)
        print(f"Added song: {u[1].split("/",1)[1]}")

def query_yt(tracklist):
    url_list=[]
    if DEBUG:
        print(f"Searching for tracks...")
    for track in tracklist:
        track = cleanup_string(track)
        res = yt.search(track)[0]
        # str_help if we need to print out the differences and id possible mismatched songs
        str_help = f"{res["title"]} - {res["artists"][0]["name"]}"
        url_list.append(f"https://www.youtube.com/watch?v={res["videoId"]}") 
    print("\nTracks found.")
    return url_list

def run_command(url, out_name):
    cmd = [
        "yt-dlp",
        "--quiet", "--no-warnings",
        "-x",
        "--extract-audio",
        "--audio-format", "mp3",
        "--embed-thumbnail",
        "-o", out_name,
        url,
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"[X] yt-dlp failed for {url} / {out_name}")

def process_files(filepath):
    for p in os.listdir(filepath):
        fil = f"{filepath}/{p}"
        ddd = p.replace(".mp3", "").split(' - ', 1)
        tag_mp3(fil, ddd[0], ddd[1])

def tag_mp3(path, title, artist, album=None):
    audio = EasyID3(path)
    audio["title"] = title
    audio["artist"] = artist
    if album:
        audio["album"] = album
    audio.save()

if __name__=="__main__":
    print("========== Pebblefoot ==========\nA tool to download or transfer your Spotify playlists. Fuck Spotify, long live piracy.\n\nNOTICE: For now at least, Pebblefoot can only download playlists with up to 25 songs, because Spotify doesn't allow non-premium having peasants to have nice things. Split your playlist into smaller if needed.")
    if not len(sys.argv)==3:
        print(f"Usage: python pebblefoot.py [url] [playlist_name]")
        exit(1)
    url = sys.argv[1]
    folder=sys.argv[2]
