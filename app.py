import spotipy
from spotipy.oauth2 import SpotifyOAuth
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import db
import time

cred = credentials.Certificate('key2.json')

app = firebase_admin.initialize_app(cred)
db = firestore.client()

client_id = '1e056cec71954c5dbbf1697f4d3e862c'
client_secret = '2fa8004246db46e897e8ab1101179b53'
redirect_uri = 'http://localhost:8888/callback'


scope = 'user-read-currently-playing,user-read-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def get_artist_info(artist_id):
    artist = sp.artist(artist_id)
    return artist

while True:
    current_track = ""
    if sp.current_playback():
        current_track = sp.current_playback()
    else:
        while True:
            if sp.current_playback():
                current_track = sp.current_playback()
                break
    name = current_track['item']['name']
    id = current_track['item']['id']
    artist_id = current_track['item']['artists'][0]['id']
    artist_info = get_artist_info(artist_id)
    genres = artist_info['genres']
    tot = ""
    for genre in genres:
        tot += genre
    doc = db.collection('gstavya').document('music').get()
    data = doc.to_dict()
    array = data.get('song', [])
    if name != array[len(array)-1]:
        db.collection('gstavya').document('music').update({"song": firestore.ArrayUnion([name])})
        db.collection('gstavya').document('music').update({"genre": firestore.ArrayUnion([tot])})
