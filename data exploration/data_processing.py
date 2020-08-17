import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split


class DataProcessing:

    def __init__(self):
        self.cid = None
        self.secret = None
        self.ccm = None
        self.spot = None

        self.df = None
        self.df_X = None
        self.df_y = None

        self.training_dataset = None
        self.training_X = None
        self.training_y = None

        self.test_dataset = None
        self.test_X = None
        self.test_y = None

        self.training_pca = None


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
        ids = []
        other_feats = pd.DataFrame(columns=['song_popularity', 'explicit', 'artists', 'genres', 'album_popularity', 'artist_popularity'])

        for i in range(len(tracklist)):
            if tracklist[i]['track']['id'] != None:
                ids.append(tracklist[i]['track']['id'])
                artists = tracklist[i]['track']['artists']
                album = tracklist[i]['track']['album']

                names = []
                genres = []
                alb_pop = []
                art_pop = []

                for artist in artists:
                    art_uri = artist['uri']
                    alb_uri = album['uri']

                    if art_uri != None and alb_uri != None:
                        print('The artist uri is ' + str(art_uri))
                        print('The album uri is ' + str(alb_uri))

                        try:
                            artist_obj = self.spot.artist(art_uri)
                            names.append(artist['name'])
                            genres.append(artist_obj['genres'])
                            art_pop.append(artist_obj['popularity'])
                        except:
                            print("No artist object available.")

                        try:
                            album_obj = self.spot.album(alb_uri)
                            alb_pop.append(album_obj['popularity'])
                        except:
                            print("No album object available.")

                other_feats.loc[i] = [tracklist[i]['track']['popularity']] + [tracklist[i]['track']['explicit']] + [names] + [genres] + [alb_pop] + [art_pop]

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

    def create_recommenders_datasets(self, pid):
        tracks = self.get_playlist_tracks(pid)
        df = self.get_track_features(tracks)

        df.to_csv('recs_library_2.csv')


    def create_datasets(self, pid_liked, pid_disliked):
        """
        :param pid_liked: pid of tracks liked
        :param pid_disliked: pid of tracks disliked
        """

        liked_tracks = self.get_playlist_tracks(pid_liked)
        liked_df = self.get_track_features(liked_tracks)
        liked_df['like'] = 1

     #   print("The number of liked songs is " + str(len(liked_df)))

        disliked_tracks = self.get_playlist_tracks(pid_disliked)
        disliked_df = self.get_track_features(disliked_tracks)
        disliked_df['like'] = 0

    #   print("The number of disliked songs is " + str(len(disliked_df)))

        final = liked_df.append(disliked_df)
        final.reset_index(inplace=True, drop=True)
     #   self.df = final
     #   self.df_X = final.loc[:, final.columns != 'like']
    #    self.df_y = final['like']

        #self.training_X, self.test_X, self.training_y, self.test_y = train_test_split(self.df.loc[:, self.df.columns!='like'],
      #                                                                                self.df.like,
       #                                                                               test_size=0.2)

        final.to_csv('music_prefs.csv')

        """print(self.training_X)
        print(self.training_y)
        print(self.test_X)
        print(self.test_y)"""



    def pca(self):
        """
        runs PCA on a given dataset

        :return:
        """
        training_X = self.training_X.values

        training_X = StandardScaler().fit_transform(training_X) # First must standardize the data bc PCA is affected by scale
                                                                #   --> Do this using sklearn's StandardScaler
                                                                #   --> Uses unit scale (mean = 0, variance = 1)
        pca = PCA(n_components=2)
        pca_components = pca.fit_transform(training_X)
        pca_df = pd.DataFrame(data=pca_components, columns=['pc1', 'pc2'])

        pca_df = pd.concat([pca_df, self.training_y], axis=1)
        self.training_pca = pca_df

        print("The resulting dimensionality-reduced df is the following: \n")
        print(pca_df.to_string())

        print("The amount of variance explained by each of the principal components is as follows: \n")
        print(pca.explained_variance_ratio_)

        print("To visualize: \n")
        plt.scatter(pca_df.iloc[:, 0], pca_df.iloc[:, 1],
                    c=pca_df.like, edgecolor='none', alpha=0.5)
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.colorbar();
        plt.show()

        plt.plot(np.cumsum(pca.explained_variance_ratio_))
        plt.xlabel('number of components')
        plt.ylabel('cumulative explained variance')
        plt.show()

        return pca_df




    def svd_dim_reduction(self, df):
        """
        runs SVD dim reduction on given dataset

        :param df: dataset on which to run SVD
        :return:
        """


    def regularize(self, df, type):
        """
        regularizes input dataset, given choice between l1 and l2

        :param df: dataset to regularize
        :param type: 'l1' or 'l2'
        :return:
        """







    def generate_audio_analysis(self, songs):
        """
        *TO-DO LATER*

        :param songs: list/df? of song IDs
        :return: dataframe with selected audio analysis features of tracks
        """


    def get_top_artists(self):
        """
        *TO-DO LATER*
        :return:
        """

        top_artists = self.spot.current_user_top_tracks(limit=10)
        print(top_artists)


