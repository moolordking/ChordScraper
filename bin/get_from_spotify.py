import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace these with your own Spotify API credentials
CLIENT_ID = '25faddab3f1f4bcfaac68712dcad7597'
CLIENT_SECRET = '05a98c1c7565401a8146259e95897b90'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri='http://localhost:8888/callback',
                                                   scope='user-library-read'))

def initialise():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri='http://localhost:8888/callback',
                                                   scope='user-library-read'))

def get_playlist_tracks(playlist_uri):
    results = sp.playlist_tracks(playlist_uri)
    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    return tracks

def clean_text(text):
    # Define a dictionary of character replacements for accents
    accent_replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
        'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u',
        'ä': 'a', 'ë': 'e', 'ï': 'i', 'ö': 'o', 'ü': 'u',
        'ç': 'c', 'ñ': 'n',
    }

    # Replace accented characters and uncommon symbols
    cleaned_text = ''.join(accent_replacements.get(char, char) for char in text)
    
    # Remove non-alphanumeric characters except for spaces and hyphens
    cleaned_text = ''.join(char if char.isalnum() or char.isspace() or char == '-' else ' ' for char in cleaned_text)

    # Replace consecutive spaces with a single space and strip leading/trailing spaces
    cleaned_text = ' '.join(cleaned_text.split())
    
    return cleaned_text

def extract_artists_and_songs(tracks):
    artist_song_list = []
    for track in tracks:
        artists = [clean_text(artist['name']) for artist in track['track']['artists']]
        song = clean_text(track['track']['name'])
        artist_song_list.append(f"{' & '.join(artists)} - {song}")

    return artist_song_list

def save_to_text_file(artist_song_list, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write('\n'.join(artist_song_list))

def locate_and_add_playlist(playlist_uri):
    initialise()

    tracks = get_playlist_tracks(playlist_uri)
    artist_song_list = extract_artists_and_songs(tracks)
    
    # Replace 'output.txt' with your desired output file name
    save_to_text_file(artist_song_list, 'SONGS.txt')  # Change 'output.txt' to 'SONGS.txt'
    
    print(f"Playlist information saved")
