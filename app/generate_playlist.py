import pandas as pd
#import model

def predict_liked(df):
    print('hi')
    # instantiate model
    # run df through model 
    # return output (df)

def get_track_info(sp, data):
    tracks = []
    artists = []
    albums = []
    artist_pop = []
    album_pop = []
    genres = []


    for item in data['items']:
        tracks.append(item['track']['uri'])
        auri = item['track']['artists'][0]['uri']
        alburi = item['track']['album']['uri']
        artists.append(auri)
        albums.append(alburi)

        artist = sp.artist(auri)
        album = sp.album(alburi)

        genres.append(artist['genres'])
        artist_pop.append(artist['popularity'])
        album_pop.append(album['popularity'])
    
    while(data['next']):
        data = sp.next(data)
        
        for item in data['items']:     
            tracks.append(item['track']['uri'])
            auri = item['track']['artists'][0]['uri']
            alburi = item['track']['album']['uri']
            artists.append(auri)
            albums.append(alburi)

            artist = sp.artist(auri)
            album = sp.album(alburi)

            genres.append(artist['genres'])
            artist_pop.append(artist['popularity'])
            album_pop.append(album['popularity'])

    
    print("There are " + str(len(tracks)) + " tracks.")
    print("The artist genres are " + str(genres))
    print("The artist popularities are " + str(artist_pop))
    print("The album popularities are " + str(album_pop))

    return tracks



def get_track_object(sp, data):
    tracks = data['items']

    while(data['next']):
        data = sp.next(data)
        tracks.extend(data['items'])

    return tracks        

def get_track_uri(sp, data):
    tracks = []
    for item in data['items']:
        tracks.append(item['track']['uri'])
    
    while data['next']:
        data = sp.next(data)

        for item in data['items']:
            tracks.append(item['track']['uri'])
    
    return tracks


def get_playlist_tracks(sp):
    # Note --- only returns tracks from 50 most recent playlists
    playlists = []
    tracks = []

    results = sp.current_user_playlists()
    for plist in results['items']:
        playlists.append(plist['id'])

    while results['next']:
        results = sp.next(results)
    
        for pl in results['items']:
            playlists.extend(pl['id'])
    
    print('There are ' + str(len(playlists)) + ' playlists.')
    
    for pid in playlists:
        data = sp.playlist_tracks(pid)
        tracks.append(get_track_uri(sp, data))

    print('There are ' + str(len(tracks)) + ' tracks!')

    return tracks

def get_saved_tracks(sp):
    data = sp.current_user_saved_tracks()
    #tracks = get_track_uri(sp, data)
    tracks = get_track_info(sp, data)
    
    print('There are ' + str(len(tracks)) + ' tracks!')
    return tracks


def get_track_features(sp, tracklist):
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
                    
                artist = sp.artist(art_uri)
                album = sp.album(alb_uri)
                            
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
        audio_features = sp.audio_features(ids)
        final = pd.DataFrame(audio_features).drop(['type', 'id', 'track_href', 'analysis_url'], axis=1)
    else:
        i = len(ids)
        final = pd.DataFrame()

        while i > 100:
            audio_features = sp.audio_features(ids[(len(ids)-i):(len(ids)-i+100)])
            aud = pd.DataFrame(audio_features)
            final = final.append(aud)
            i = i - 100

        audio_features = sp.audio_features(ids[(len(ids)-i):(len(ids))])
        aud = pd.DataFrame(audio_features)
        final = final.append(aud)

    final.reset_index(inplace=True, drop=True)
    final = pd.concat([final, other_feats], axis=1)

    return final



def create_rec_dataset():
    print('hi')
    # include the cleaning 
    # return the df to pass to the model 

def gen_playlist(df, mood, genres, thresh):
    #try:
        #df = df.drop(columns=['Unnamed: 0'])
    #except:
        #pass

    final_df = pd.DataFrame()

    if not genres or 'surprise me' in genres:
        final_df = df

    else:
        for gen in genres:
            temp = df.loc[df[gen] == 1]
            try:
                final_df = final_df.append(temp[temp.isin(final_df) == False].dropna())
            except:
                final_df = temp.merge(final_df)

        final_df = final_df.reset_index(drop=True)

    if mood == 'cheery':
        final_df = final_df.loc[final_df['valence'] > 0.5]
    elif mood == 'melancholy':
        final_df = final_df.loc[final_df['valence'] < 0.5]
    elif mood == 'upbeat':
        final_df = final_df.loc[(final_df['energy'] > 0.6) & (final_df['danceability'] > 0.6)]

    # subset from those with rf_pred_liked higher than 0.7
    # sample from subset (so different every time)
    final_df = final_df.loc[(final_df['rf_pred_liked'] > float(thresh))]

    if len(final_df) >= 10:
        final_df = final_df.sample(n=10)

    return final_df