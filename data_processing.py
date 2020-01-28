import pandas as pd
import spotipy
from spotipy import Spotify as sp


class DataProcessing:

    def __init__(self):
        self.training_dataset = None
        self.test_dataset = None


    def get_playlist_tracks(self, user, pid):
        if user == 'janna':
            cid = "3f24d8da29c44c2d80b2c2abe518b5d6"
            secret = "370a726a55654c68bd3d0a1036eb7049"

        ccm = spotipy.SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager=ccm)
        sp.trace = False

        results = sp.playlist_tracks(pid)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

      #  df = pd.DataFrame(tracks)

        #print(df.to_string())
        print(tracks)
        return tracks


    def get_track_features(self, tracklist):
        ids, audio_features, other_feats = [], [], (pd.DataFrame(columns=['popularity', 'explicit']))

        for i in range(len(tracklist)):
            other_feats.loc[i] = [tracklist[i]["track"]["popularity"]] + [tracklist[i]["track"]["explicit"]]
            ids.append(tracklist[i]["track"]["id"])

        audio_features = sp.audio_features(ids)
        final = pd.DataFrame(audio_features)
        final = pd.concat([final, other_feats], axis=1)

        print(final.to_string())
        return final

    def create_training_dataset(self, playlists_liked, playlists_disliked):
        """
        :param playlists_liked: dataframe of tracks liked
        :param playlists_disliked: dataframe of tracks disliked
        :return: concatenated df with 'liked' column
        """



    def generate_audio_analysis(self, songs):
        """
        *TO-DO*

        :param songs: list/df? of song IDs
        :return: dataframe with selected audio analysis features of tracks
        """



