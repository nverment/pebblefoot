from spotapi import Song, PublicPlaylist
from ytmusicapi import YTMusic
from mutagen.easyid3 import EasyID3 
import subprocess
import sys
import os 

id='https://open.spotify.com/playlist/1fytm1VDA2xutq7FEn6lSm'

PP=1
DEBUG=0

yt = YTMusic('browser.json')

# spotify URL to list of strings in format 'title track - artist'
def fetch_tracklist(url):
    tracklist=[]
    playlist= PublicPlaylist(url)

    if "open.spotify.com/playlist" in url:
        print(f"Spotify URL detected.")
        info = playlist.get_playlist_info()
        items = info["data"]["playlistV2"]["content"]["items"]
        print(f"\nGenerating tracklist...\n")
        for item in items:
            query = (f"{item["itemV2"]["data"]["name"]} - {item["itemV2"]["data"]["artists"]["items"][0]["profile"]["name"]}")
            print(f"{query}")
            tracklist.append(query)
    else:
       print("Wrong URL format - try again")
    return tracklist

def query_yt(tracklist, folder):
    if DEBUG:
        print(f"Searching for tracks...")
    for track in tracklist:
        res = yt.search(track)[0]
        video_id = res["videoId"]
        str_help = f"{res["title"]} - {res["artists"][0]["name"]}"
        output_name=f"{folder}/{str_help}"
        run_command(f"https://www.youtube.com/watch?v={video_id}", output_name)
        if DEBUG:
            print(f"\n\t{track}\n\t{str_help}\n")
    print("Tracks found.")
    if DEBUG:
        print(tracklist)

def run_command(url, out_name):
    if DEBUG:
        print(f"DEBUG: got to run command with {url}")
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
        # print(cmd)
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"[X] yt-dlp failed for {url} / {out_name}")
        #sys.exit(1)

def process_files(filepath):
    if not os.path.isdir(filepath):
        print("Not a directory. Exiting.")
        exit(1)
    for p in os.listdir(filepath):
        fil = f"{filepath}{p}"
        ddd = p.replace(".mp3", "").split(' - ', 1)
        print(ddd)
        tag_mp3(fil, ddd[0], ddd[1])

def tag_mp3(path, title, artist, album=None):
    print(f"{title} {artist}")
    audio = EasyID3(path)
    audio["title"] = title
    audio["artist"] = artist
    if album:
        audio["album"] = album
    audio.save()

    # tag_mp3(
    #     path="todolist/01 - Cycles.mp3",
    #     title="Cycles",
    #     artist="Lili Trifilio",
    # )

if __name__=="__main__":
    print("Pebblefoot : Fuck Spotify\n")
    if not len(sys.argv)==3:
        print(f"Usage: python pebblefoot.py [url] [playlist_name]")
        exit(1)
    url = sys.argv[1]
    folder=sys.argv[2]
    # trackl= fetch_tracklist(url)
    # query_yt(trackl, folder)
    process_files(f"{folder}/")

