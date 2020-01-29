from data_processing import DataProcessing


def main():


    dp = DataProcessing()
    dp.authenticate("antoine")
    tracks = dp.get_playlist_tracks("spotify:playlist:7evicL9iF5Iaa0Unm22N30")
    tracks_2 = dp.get_track_features(tracks)

   # print(tracks)
   # print(len(tracks))



if __name__ == '__main__':
    main()
