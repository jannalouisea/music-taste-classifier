import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class DataProcessing:

    def __init__(self):
        self.cid = None
        self.secret = None
        self.ccm = None
        self.spot = None


        self.training_dataset = None
        self.test_dataset = None



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
        ids = []
        other_feats = pd.DataFrame(columns=['popularity', 'explicit'])

        for i in range(len(tracklist)):
            ids.append(tracklist[i]['track']['id'])
            other_feats.loc[i] = [tracklist[i]['track']['popularity']] + [tracklist[i]['track']['explicit']]

        if len(ids) < 100:
            audio_features = self.spot.audio_features(ids)
            final = pd.DataFrame(audio_features).drop(['type', 'id', 'uri', 'track_href', 'analysis_url'], axis=1)

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
        final = final.drop(['type', 'id', 'uri', 'track_href', 'analysis_url'], axis=1)
        final = pd.concat([final, other_feats], axis=1)

        return final


    def create_training_dataset(self, pid_liked, pid_disliked):
        """
        :param pid_liked: pid of tracks liked
        :param pid_disliked: pid of tracks disliked
        :return: concatenated df with 'liked' column
        """

        liked_tracks = self.get_playlist_tracks(pid_liked)
        liked_df = self.get_track_features(liked_tracks)

     #   print("The number of liked songs is " + str(len(liked_df)))

        disliked_tracks = self.get_playlist_tracks(pid_disliked)
        disliked_df = self.get_track_features(disliked_tracks)

    #   print("The number of disliked songs is " + str(len(disliked_df)))

        for i in range(len(liked_df)):
            liked_df['like'] = 1

        for i in range(len(disliked_df)):
            disliked_df['like'] = 0

        self.training_df = liked_df.append(disliked_df)
        self.training_df.reset_index(inplace=True, drop=True)

#        print("The number of total songs is " + str(len(self.training_df)))

        return self.training_df











        # calls get playlist tracks + get track features
        # returns final dataframe of all songs liked and disliked



    def generate_audio_analysis(self, songs):
        """
        *TO-DO LATER*

        :param songs: list/df? of song IDs
        :return: dataframe with selected audio analysis features of tracks
        """



