from spotapi import Song, PublicPlaylist
from ytmusicapi import YTMusic
from mutagen.easyid3 import EasyID3 
import subprocess
import sys
import os 

id='https://open.spotify.com/playlist/1fytm1VDA2xutq7FEn6lSm'

PP=1
DEBUG=1

yt = YTMusic('browser.json')

def cleanup_string(srg):
    cleaned = srg.replace(" - ", " ")
    cleaned = srg.replace(" | ", " ")
    if DEBUG and not (cleaned==srg):
        print(f"\t\t{srg}--> {cleaned}")
    return cleaned 

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
            # cleaning up original title (from spotify)
            title = cleanup_string(item["itemV2"]["data"]["name"])
            artist = cleanup_string(item["itemV2"]["data"]["artists"]["items"][0]["profile"]["name"])
            query = (f"{title} - {artist}")
            print(f"\t- {query}")
            tracklist.append(query)
    else:
       print("Wrong URL format - try again")
    # print(tracklist)
    # ans = input("Ok that all happened. Good to keep going? (Press any key)\n")
    return tracklist

def transfer_to_yt(url_list, folder):
    playlist_id = yt.create_playlist(title=folder, description='', privacy_status='public')

    for u in url_list:
        yt.add_playlist_items(playlist_id, u[0])
        print(f"Added song {u[1]}")

def query_yt(tracklist, folder):
    url_list=[]
    errlist=[]
    if DEBUG:
        print(f"Searching for tracks...")
        print(f"\nIMPORTANT NOTICE: The track is saved as the 'title' variable not the 'track found' one.")
    for track in tracklist:
        # print(f"\n --> searching for {track}")
        res = yt.search(track)[0]
        # print(res)
        if not res:
            errlist.append(track)
        video_id = res["videoId"]
        str_help = f"{res["title"]} - {res["artists"][0]["name"]}"
        # print(f" --> found {video_id}")
        output_name=f"{folder}/{track}"
        url_list.append([f"https://www.youtube.com/watch?v={video_id}", output_name]) 
        # run_command(f"https://www.youtube.com/watch?v={video_id}", output_name)
        if DEBUG:
            print(f"\n\tOriginal title:\t{track}\n\tTrack found:\t{str_help:<10}\n")
    print("\nTracks found.")
    # print(f"Files not found: ")
    # print(f"{[er for er in errlist]}")
    return url_list, folder

def handle_flow(url, folder):
    if (DEBUG):
        print("\n========== ENTERING DEBUG MODE ==========\n")
    trackl= fetch_tracklist(url)
    urllist = query_yt(trackl, folder)
    # flag=input("\nOptions:\n[1] Download playlist\n[2] Transfer playlist to YT Music\n")
    flag="1"
    # print(urllist)
    # ans = input("Ok that all happened. Good to keep going? (Press any key)\n")
    if flag=="1":
        for u in urllist[0]:
            temp = u[1].split('/', 1)[1]
            print(f"\nDownloading...\n\t--> {temp:<40}")
            run_command(u[0], u[1])
        # ans = input("Ok that all happened. Good to keep going? (Press any key)\n")
        process_files(folder)
    elif flag=="2":
        transfer_to_yt(urllist, folder)
    else:
        print("Input a number (1 or 2)")
    # transfer_to_yt(urllist)
    # process_files(f"{folder}/")

def run_command(url, out_name):
    # if DEBUG:
        # print(f"DEBUG: got to run command with {url}")
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
        #sys.exit(1)

def process_files(filepath):
    if not os.path.isdir(filepath):
        print("Not a directory. Exiting.")
        exit(1)
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

    # tag_mp3(
    #     path="todolist/01 - Cycles.mp3",
    #     title="Cycles",
    #     artist="Lili Trifilio",
    # )

if __name__=="__main__":
    print("========== Pebblefoot ==========\nA tool to download or transfer your Spotify playlists. Fuck Spotify, long live piracy.\n\nNOTICE: For now at least, Pebblefoot can only download playlists with up to 25 songs, because Spotify doesn't allow non-premium having peasants to have nice things. Split your playlist into smaller if needed.")
    if not len(sys.argv)==3:
        print(f"Usage: python pebblefoot.py [url] [playlist_name]")
        exit(1)
    url = sys.argv[1]
    folder=sys.argv[2]
    handle_flow(url, folder)
