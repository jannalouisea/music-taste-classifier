import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.model_selection import train_test_split


class DataProcessing:

    def __init__(self):
        self.cid = None
        self.secret = None
        self.ccm = None
        self.spot = None


    def authenticate(self, user):
        """
        :param user: name of user to authenticate
        """
        if user == 'janna':
            self.cid = "3f24d8da29c44c2d80b2c2abe518b5d6"
            self.secret = "8ac7cc24ebb54768963eb0d0f1c4fb54"
        elif user == 'antoine':
            self.cid = "588db28e1d014217844cf33a69c42e69"
            self.secret = "f3ae15c85e1b47ccaecdeb0e33dfccaa"
        else:
            print("ERROR: invalid user.")

        self.ccm = SpotifyClientCredentials(client_id=self.cid, client_secret=self.secret)
        self.spot = spotipy.Spotify(client_credentials_manager=self.ccm)                            # Uses user info to authenticates requests
        self.spot.trace = False


    def get_playlist_tracks(self, pid):
        """
        :param pid: playlist ID (Spotify URI)
        :return: a list of track objects
        """
        results = self.spot.playlist_tracks(pid)
        tracks = results['items']
        while results['next']:
            results = self.spot.next(results)
            tracks.extend(results['items'])

        return tracks


    def get_track_features(self, tracklist):
        """
        :param tracklist: a list of track objects
        :return: a DataFrame of tracks and their respective audio features
        """

        other_feats = pd.DataFrame(columns=['song_popularity', 'explicit', 'genres', 'album_popularity', 'artist_popularity'])

        ids = []
        artists = []
        album = []

        for i in range(len(tracklist)):
            if tracklist[i]['track']['id'] != None:
                ids.append(tracklist[i]['track']['id'])
                artists = tracklist[i]['track']['artists']
                album = tracklist[i]['track']['album']

                genres = []
                alb_pop = []
                art_pop = []
                print(str(i))

                try:
                    art_uri = artists[0]['uri']
                    alb_uri = album['uri']
                        
                    artist = self.spot.artist(art_uri)
                    album = self.spot.album(alb_uri)
                                
                    genres.append(artist['genres'])
                    art_pop.append(artist['popularity'])
                    alb_pop.append(album['popularity'])

                    print("This artist's genres are " + str(genres))
                    print("The artist popularity is " + str(art_pop))
                    print("The album popularity is " + str(alb_pop))
                except:
                    pass

                other_feats.loc[i] = [tracklist[i]['track']['popularity']] + [tracklist[i]['track']['explicit']] + [genres] + [alb_pop] + [art_pop]

        if len(ids) < 100:
            audio_features = self.spot.audio_features(ids)
            final = pd.DataFrame(audio_features).drop(['type', 'id', 'track_href', 'analysis_url'], axis=1)
        else:
            i = len(ids)
            final = pd.DataFrame()

            while i > 100:
                audio_features = self.spot.audio_features(ids[(len(ids)-i):(len(ids)-i+100)])
                aud = pd.DataFrame(audio_features)
                final = final.append(aud)
                i = i - 100

            audio_features = self.spot.audio_features(ids[(len(ids)-i):(len(ids))])
            aud = pd.DataFrame(audio_features)
            final = final.append(aud)

        final.reset_index(inplace=True, drop=True)
        final = pd.concat([final, other_feats], axis=1)

        return final
    

    def create_recommenders_datasets(self, pid, name):
        """
        :param pid: pid of tracks from library of recommender
        :param name: string of file name
        """
        tracks = self.get_playlist_tracks(pid)
        df = self.get_track_features(tracks)
        df.to_csv(name)        # Export recommender's df of tracks as a .csv



    def create_datasets(self, pid_liked, pid_disliked, name):
        """
        :param pid_liked: pid of tracks liked
        :param pid_disliked: pid of tracks disliked
        :param name: string of file name
        """

        liked_tracks = self.get_playlist_tracks(pid_liked)
        liked_df = self.get_track_features(liked_tracks)
        liked_df['like'] = 1
        #print("The number of liked songs is " + str(len(liked_df)))

        disliked_tracks = self.get_playlist_tracks(pid_disliked)
        disliked_df = self.get_track_features(disliked_tracks)
        disliked_df['like'] = 0
        #print("The number of disliked songs is " + str(len(disliked_df)))

        final = liked_df.append(disliked_df)
        final.reset_index(inplace=True, drop=True)

        final.to_csv('./datasets/' + name)         # Export final df of tracks as a .csv
