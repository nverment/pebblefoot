from pebble_utils import (
    transfer_to_yt,
    fetch_tracklist,
    query_yt,
    cleanup_string,
    run_command,
    process_files,
    check_headers_file,
    create_yt_instance,
)
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Pebblefoot")
    parser.add_argument("-u", "--url", required=True, help="spotify playlist URL (format open.spotify.com/playlist/..)")
    parser.add_argument("-n", "--name", help="output playlist name.")
    parser.add_argument("-m", "--mode",choices=["d", "t"],help="mode:\n  d = download\n  t = transfer")
    
    return parser.parse_args()
    
def main():
    args = parse_args()

    check_headers_file()

    url = args.url
    name = cleanup_string(args.name)
    mode = args.mode
    yt = create_yt_instance()

    tracklist = fetch_tracklist(url)
    urllist = query_yt(yt, tracklist)
    
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
        transfer_to_yt(yt, urllist, name)

def main_gui(url, name, mode):

    yt = create_yt_instance()
    name = cleanup_string(name)
    tracklist = fetch_tracklist(url)
    urllist = query_yt(yt, tracklist)
    
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
        transfer_to_yt(yt, urllist, name)
            
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
    print("A tool to download or transfer your Spotify playlists. Fuck Spotify, long live piracy.\n")
    main()