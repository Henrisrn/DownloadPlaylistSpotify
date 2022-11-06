import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import pytube
import time

CLIENT_ID = ''
CLIENT_SECRET = ""
PLAYLIST_LINK = "https://open.spotify.com/playlist/1HIustV9i4CVpvlDx1EcsD?si=e2d4c1704ac742dd"

CLIENT_CREDENTIALS_MANAGER = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
SP = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)
downloadtype = 1

def get_playlist_uri(playlist_link):
    return playlist_link.split("/")[-1].split("?")[0]


def call_playlist(creator, playlist_id):
    playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]

    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    #step2
    
    playlist = SP.user_playlist_tracks(creator, playlist_id)["items"]
    for track in playlist:
        # Create empty dict
        playlist_features = {}
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
        
        # Get audio features
        audio_features = SP.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            try:
                playlist_features[feature] = audio_features[feature]
            except:
                print("error")        
        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)

    #Step 3
        
    return playlist_df

dfplaylist = call_playlist('Tribal Trap','1HIustV9i4CVpvlDx1EcsD')
driver=webdriver.Chrome("C://Users//henri//Downloads//chromedriver_win32 (2)//chromedriver.exe")  
def normalise(string):
    res = ""
    for i in range(len(string)):
        if(string[i] == " " and string[i+1] != " " and string[i-1] != " "):
            res += '+'
        if(string[i] != " "):
            res += string[i]
    return res

uridespages = []
titreplaylist = []
for i in range(len(dfplaylist["track_name"])):
    titre = normalise(str(dfplaylist["track_name"][i])).replace(" ","+")+'+'+ normalise(str(dfplaylist["artist"][i])).replace(" ","+")
    print(titre)
    driver.get("https://www.youtube.com/results?search_query="+titre)
    time.sleep(3)
    try:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        link = soup.find_all('a',class_="yt-simple-endpoint style-scope ytd-video-renderer",href=True)
        uridespages.append(link[0]["href"])
        print(link[0]["href"])
    except:
        print("Probleme avec la lecture du titre : "+str(titre))
    
print(titreplaylist)
print(uridespages)
# where to save 
  
# link of the video to be downloaded 
for i in uridespages:
    try:
        link="https://www.youtube.com"+str(i)
        print(link)
        yt = pytube.YouTube(link)
        stream = yt.streams.get_audio_only()
        #stream = yt.streams.first()
        stream.download()
    except:
        print("Problem avec : "+str("https://www.youtube.com"+str(i)))
    time.sleep(2)

driver.close()

