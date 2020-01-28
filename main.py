from data_processing import DataProcessing


def main():


    dp = DataProcessing()
    tracks = dp.get_playlist_tracks("janna", "spotify:playlist:1Ol1AQX5IDgBKjEqVflQ0y")
    tracks_2 = dp.get_track_features(tracks)

   # print(tracks)
    print(len(tracks))



if __name__ == '__main__':
    main()
