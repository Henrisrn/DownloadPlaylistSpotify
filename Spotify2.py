import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import pytube
import time

CLIENT_ID = 'ENTER CLIEN ID FROM SPOTIFY API'
CLIENT_SECRET = "ENTER CLIENT SECRET FROM SPOTIFY API"

#GO FOLLOW ME ON SPOTIFY
PLAYLIST_LINK = "https://open.spotify.com/playlist/6eo3ETxhrwTD1YY9GcMw79"

CLIENT_CREDENTIALS_MANAGER = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
SP = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)
downloadtype = input("Entre ce que tu veux télécharger comme musique (1 playlist, 2 album, 3 les top tubes de l'artiste")

def get_playlist_uri(playlist_link):
    return playlist_link.split("/")[-1].split("?")[0]


def get_tracks():
    tracks = []
    playlist_uri = get_playlist_uri(PLAYLIST_LINK)
    for track in SP.playlist_tracks(playlist_uri)["items"]:
        track_uri = track["track"]["uri"]
        track_name = track["track"]["name"]
        result = track_name, SP.audio_features(track_uri)
        tracks.append(result)

    return tracks

def get_traks_album():
    tracks = []
    album_uri = get_playlist_uri(PLAYLIST_LINK)
    for track in SP.album_tracks(album_uri)["items"]:
        track_uri = track["track"]["uri"]
        track_name = track["track"]["name"]
        result = track_name, SP.audio_features(track_uri)
        tracks.append(result)

    return tracks

def get_traks_artist():
    tracks = []
    uri = get_playlist_uri(PLAYLIST_LINK)
    for track in SP.artist_top_tracks(uri)["items"]:
        track_uri = track["track"]["uri"]
        track_name = track["track"]["name"]
        result = track_name, SP.audio_features(track_uri)
        tracks.append(result)

    return tracks


driver=webdriver.Chrome("C://Users//henri//Downloads//chromedriver_win32 (2)//chromedriver.exe")  
the_stuff = []
if(downloadtype == 1):
    the_stuff = get_tracks()
if(downloadtype == 2):
    the_stuff = get_traks_album()
if(downloadtype == 3):
    the_stuff = get_traks_artist()
uridespages = []
titreplaylist = []
for i in the_stuff:
    titreplaylist.append(i[0])
    titre = str(i[0]).replace(" ","+")
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
