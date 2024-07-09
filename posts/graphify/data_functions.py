import spotipy
import json
from data_classes import Artist
import os

def collect_top_artists(key, time_period, n_artists):
    """
    Collects the user's top Spotify artists.

    Retrieves the user's top artists over a given time period from the Spotify Web API. It returns a list of 'Artist' objects.

    Args:
        key (spotipy.Spotify): Authenticated Spotify API client.
        time_period (str): The time range over which to retrieve top artists. 
                           Valid values are 'short_term' (1 month), 'medium_term' (6 months), and 'long_term' (all-time).
        n_artists (int): The number of top artists to retrieve.
                           
    Returns:
        A list of 'Artist' objects representing the user's top artists.
        
    Raises:
        spotipy.SpotifyException: If there is an error in the Spotify API request.
    """
    sp = key 
    top_artists = sp.current_user_top_artists(time_range=time_period, limit=n_artists)
    top_ten_artists = []
    for i in range(n_artists):
        top_ten_artists.append(Artist(top_artists['items'][i]['name'], 
                                      top_artists['items'][i]['id'], 
                                      top_artists['items'][i]['images'][0]['url'], 
                                      top_artists['items'][i]['popularity'], i + 1))
    return top_ten_artists

def collect_related_artists(key, top_ten_artists):
    """
    Collects Spotify's "Fans also like" artists for each of the user's top artists.

    This function updates each 'Artist' object with a list of the artist's related artists using the Spotify Web API. 

    Args:
        key (spotipy.Spotify): Authenticated Spotify API client.
        top_ten_artists (list of Artist): A list of 'Artist' objects to query.
    
    Raises: 
        spotipy.SpotifyException: If there is an error in the Spotify API request.
    """
    sp = key 
    for artist in top_ten_artists:
        related_artists = sp.artist_related_artists(artist.id)
        artist.related_artists = [musician['name'] for musician in related_artists['artists']]

def test_collect_related_artists(sp, top_ten_artists, filename='related_artists_data_30.json'):
    # Check if data file exists
    if os.path.exists(filename):
        # Load related artists data from the file
        with open(filename, 'r') as f:
            related_artists_data = json.load(f)
        
        # Assign the loaded related artists to each artist
        for artist, related_artists in zip(top_ten_artists, related_artists_data):
            artist.related_artists = related_artists
    else:
        # Collect related artists data from the API
        related_artists_data = []
        for artist in top_ten_artists:
            related_artists = sp.artist_related_artists(artist.id)
            artist.related_artists = [musician['name'] for musician in related_artists['artists']]
            related_artists_data.append(artist.related_artists)
        
        # Save related artists data to a file
        with open(filename, 'w') as f:
            json.dump(related_artists_data, f)