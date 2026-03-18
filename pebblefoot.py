from spotapi import Song, PublicPlaylist
from ytmusicapi import YTMusic
import subprocess
import sys
import ytmusicapi

id='https://open.spotify.com/playlist/1fytm1VDA2xutq7FEn6lSm'

PP=1
DEBUG=1

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

def query_yt(tracklist):
    if DEBUG:
        print(f"Searching for tracks...")
    for track in tracklist:
        res = yt.search(track)[0]
        video_id = res["videoId"] 
        str_help = f"{res["title"]} - {res["artists"][0]["name"]}"
        if DEBUG:
            print(f"\n\t{track}\n\t{str_help}\n")

# def god_method(url):
#     tracklist = []
#
#     playlist = PublicPlaylist(url)
#     if "open.spotify.com/playlist" in url:
#         print(f"Spotify URL detected.")
#         fe = playlist.get_playlist_info()
#         fetched = fe["data"]["playlistV2"]["content"]["items"]
#         print(f"\nGenerating tracklist...\n")
#         for rr in fetched:
#             curr = (f"{rr["itemV2"]["data"]["name"]} - {rr["itemV2"]["data"]["artists"]["items"][0]["profile"]["name"]}")
#             print(f"{curr}")
#             tracklist.append(curr)
#     else:
#        print("wrong format") 
#
#     if PP:
#         for track in tracklist:
#             argg = yt.search(track)[0]
#             arg1 = argg["videoId"] 
#             arg2 = f"{argg["title"]} - {argg["artists"][0]["name"]}"
#             if DEBUG:
#                 print(f"Searching:\n\t{track}\n\t{arg2}")
#             # run_command(arg1, track)
#     else:
#         print(tracklist)
#
def run_command(url, out_name):
    if DEBUG:
        print(f"DEBUG: got to run command with {url}")
    cmd = [
        "yt-dlp",
        "--quiet", "--no-warnings",
        "-x",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", out_name,
        url,
    ]
    try:
        print(cmd)
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"[X] yt-dlp failed for {url} / {out_name}")
        #sys.exit(1)

if __name__=="__main__":
    print("Pebblefoot : Fuck Spotify\n")
    url = sys.argv[1]
    # god_method(url)
    trackl= fetch_tracklist(url)
    query_yt(trackl)

