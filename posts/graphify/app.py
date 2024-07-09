import spotipy 
from spotipy.oauth2 import SpotifyOAuth
from data_classes import Artist
from data_functions import collect_top_artists, collect_related_artists
import dotenv
import os 
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

# Load environment variables
dotenv.load_dotenv()

# Define environment variables
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_url = os.getenv("SPOTIFY_REDIRECT_URI")
scope = os.getenv("SPOTIFY_SCOPE")

# Authenticate your Spotify account
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, 
                                               client_secret=client_secret,
                                               redirect_uri=redirect_url,
                                               scope=scope))

# Define how many of your top artists and for what time period you want to query 
n_artists = 10
time_period = "short_term"

# Store artist information in a list (note that information is stored in Artist class)
top_ten_artists = collect_top_artists(sp, time_period, n_artists)
for artist in top_ten_artists:
    print(artist.name)

# Collect list of artists in each artist's "Fans also like"
collect_related_artists(sp, top_ten_artists)

# Initialize your network of artists
N = nx.Graph()

# Create a node for each of the top artists
for artist in top_ten_artists:
    N.add_node(artist.name, size=40, shape='circularImage', image=artist.image_url)

# Check if each top artist is in the other top artists' "Fans also like" 
# If edge already exists, adjust the weight; create edge if one does not exist 
for artist in top_ten_artists:
    for different_artist in top_ten_artists:
        if artist != different_artist:
            if artist.name in different_artist.related_artists:
                if N.has_edge(artist.name, different_artist.name):
                    N[artist.name][different_artist.name]['weight'] += 1
                else:
                    N.add_edge(artist.name, different_artist.name, weight=1, color="black")


centrality_values = nx.betweenness_centrality(N)
print(centrality_values)

net_test = Network(notebook=True, directed=False, height='95vh', width='100%')
net_test.from_nx(N)
new_test_path = 'graph.html'
net_test.show(new_test_path)
# IFrame("graph.html", width="100%", height="600px")


########## Resised code to execute with the json
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
from data_classes import Artist
from data_functions import collect_top_artists, collect_related_artists, test_collect_related_artists
import dotenv
import os 
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import json

# Function to save and load data
def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Load environment variables
dotenv.load_dotenv()

# Define environment variables
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_url = os.getenv("SPOTIFY_REDIRECT_URI")
scope = os.getenv("SPOTIFY_SCOPE")

# Authenticate your Spotify account
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, 
                                               client_secret=client_secret,
                                               redirect_uri=redirect_url,
                                               scope=scope))

# Define how many of your top artists and for what time period you want to query 
n_artists = 15
time_period = "medium_term"
data_filename = 'top_artists_data.json'

# Check if data file exists
if os.path.exists(data_filename):
    # Load data from the file
    top_artists_data = load_data(data_filename)
    top_ten_artists = [Artist(**artist) for artist in top_artists_data]
else:
    # Collect artist information
    top_ten_artists = collect_top_artists(sp, time_period, n_artists)
    
    # Convert Artist objects to dictionaries to save to file
    top_artists_data = [artist.__dict__ for artist in top_ten_artists]
    save_data(top_artists_data, data_filename)

# Collect list of artists in each artist's "Fans also like" if not already loaded
test_collect_related_artists(sp, top_ten_artists)

# Initialize your network of artists
N = nx.Graph()

# Create a node for each of the top artists
for artist in top_ten_artists:
    N.add_node(artist.name, size=40, shape='circularImage', image=artist.image_url)

# Check if each top artist is in the other top artists' "Fans also like" 
# If edge already exists, adjust the weight; create edge if one does not exist 
for artist in top_ten_artists:
    for different_artist in top_ten_artists:
        if artist != different_artist:
            if artist.name in different_artist.related_artists:
                if N.has_edge(artist.name, different_artist.name):
                    N[artist.name][different_artist.name]['weight'] += 1
                else:
                    N.add_edge(artist.name, different_artist.name, weight=1, color="black")

centrality_values = nx.betweenness_centrality(N)
print(centrality_values)

net_test = Network(notebook=True, directed=False, height='95vh', width='100%')
net_test.from_nx(N)
new_test_path = 'graph.html'
net_test.show(new_test_path)
