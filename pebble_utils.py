import os
import sys
import time
import subprocess
from ytmusicapi import YTMusic
from spotapi import PublicPlaylist
from mutagen.easyid3 import EasyID3
from ytmusicapi.auth.browser import setup_browser

DEBUG=0

def handle_multi_line_input() -> str:
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    text = "\n".join(lines)
    return text


def check_headers_file():
    if not os.path.exists("headers.txt"):
        
        open("headers.txt", "x") # create headers.txt
        print("Paste your headers (enter a blank line to finish):")

        headers_text = handle_multi_line_input()
        if not headers_text:
            raise Exception("Entered empty string")
        
        with open("headers.txt", "a") as f:
            f.write(headers_text)

    with open('headers.txt', 'r') as f:
        if f.read() == "":
            sys.exit("Empty headers.txt file.\nExiting...")


def create_yt_instance():
    with open('headers.txt', 'r') as f:
        setup_browser('browser.json', f.read())
    yt = YTMusic('browser.json')
    return yt

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
    info = list(playlist.paginate_playlist()) # paginate_playlist yields a generator so we turn it into a list for ease
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

def transfer_to_yt(yt_instance, url_list, folder):
    existing=input("Enter existing playlist URL to add songs to it." \
    "\nor press ENTER (no URL) and a new playlist will be created in your profile automatically.\n"
    "URL:")
    
    if "https://music.youtube.com/playlist?list=" in existing:
        playlist_id = yt_instance.get_playlist(existing.split("=",1)[1])["id"]
        print(playlist_id)
    else:
        playlist_id = yt_instance.create_playlist(title=folder, description='', privacy_status='public')
    
    for url in url_list:
        video_id = url.split("v=")[1]
        yt_instance.add_playlist_items(playlist_id, [video_id])
        time.sleep(1)

        print(f"added '{yt_instance.get_song(video_id)["videoDetails"]["title"]}' to playlist")

def query_yt(yt_instance, tracklist):
    url_list=[]
    if DEBUG:
        print(f"Searching for tracks...")
    for track in tracklist:
        track = cleanup_string(track)
        res = yt_instance.search(track)[0]
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