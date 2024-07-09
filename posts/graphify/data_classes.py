class Artist:
    """
    Data class to store a Spotify artist's attributes.

    Attributes:
        name (str): The name of the artist.
        id (str): The artist's Spotify unique identifier.
        image_url (str): URL to the artist's Spotify image.
        spotify_popularity (int): Popularity score of the artist on Spotify (0 to 100).
        user_rank (int): Rank of the artist among the user's most listened to artists.
        related_artists (list): List of the artist's "Fans also like" artists (includes artists not featured on mobile "Fans also like").

    """

    def __init__(self, name, id, image_url, spotify_popularity, user_rank, related_artists=None):
        """
        Initializes an Artist instance with the given attributes. 

        Args:
            name (str): The name of the artist.
            id (str): The artist's Spotify unique identifier.
            image_url (str): URL to the artist's Spotify image.
            spotify_popularity (int): Popularity score of the artist on Spotify (0 to 100).
            user_rank (int): Rank of the artist among the user's most listened to artists.
            related_artists (list, optional): List of the artist's "Fans also like" artists. Defaults to an empty list if not provided.
        """
        self.name = name 
        self.id = id 
        self.image_url = image_url 
        self.spotify_popularity = spotify_popularity 
        self.user_rank = user_rank
        if related_artists is None:
            related_artists = []
        self.related_artists = related_artists 

    def add_related_artist(self, related_artist):
        self.related_artists.append(related_artist)
