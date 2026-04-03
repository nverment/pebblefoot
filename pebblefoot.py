from pebble_utils import transfer_to_yt
from pebble_utils import fetch_tracklist, query_yt, cleanup_string, run_command, process_files
from ytmusicapi import YTMusic
from ytmusicapi.auth.browser import setup_browser
import argparse
import argparse
from tabulate import tabulate

with open('headers.txt', 'r') as f:
    setup_browser('browser.json', f.read())

yt = YTMusic('browser.json')

def parse_args():
    parser = argparse.ArgumentParser(description="Pebblefoot")
    parser.add_argument("-u", "--url", required=True, help="spotify playlist URL (format open.spotify.com/playlist/..)")
    parser.add_argument("-n", "--name", help="output playlist name.")
    parser.add_argument("-m", "--mode",choices=["d", "t"],help="mode:\n  d = download\n  t = transfer")
    
    return parser.parse_args()
    
def main():
    args = parse_args()

    url = args.url
    name = cleanup_string(args.name)
    mode = args.mode

    tracklist = fetch_tracklist(url)
    urllist = query_yt(tracklist)
    
    if mode=="d":
        if not (len(tracklist) == len(urllist)):
            print("Mismatched sizes, quitting!")
            exit(1)
        print("Downloading...")
        for i in range(len(tracklist)):
            print(f"[{i+1:02d}] {tracklist[i]}")
            run_command(urllist[i], f"{name}/{tracklist[i]}")
            process_files(name)
    else:
        transfer_to_yt(urllist, name)
            
if __name__=="__main__":
    print(
        """
   ▄▄▄▄  ▗▞▀▚▖▗▖   ▗▖   █ ▗▞▀▚▖▗▞▀▀▘▄▄▄   ▄▄▄     ■  
   █   █ ▐▛▀▀▘▐▌   ▐▌   █ ▐▛▀▀▘▐▌  █   █ █   █ ▗▄▟▙▄▖
   █▄▄▄▀ ▝▚▄▄▖▐▛▀▚▖▐▛▀▚▖█ ▝▚▄▄▖▐▛▀▘▀▄▄▄▀ ▀▄▄▄▀   ▐▌  
   █          ▐▙▄▞▘▐▙▄▞▘█      ▐▌                ▐▌  
   ▀                                             ▐▌  
                                                     
    """                                                                   
    )
    main()

