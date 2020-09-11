from data_processing import DataProcessing

def main():
    """
    Driver
    """

    dp = DataProcessing()
    dp.authenticate('antoine')

    # Playlists of songs liked and disliked by Antoine
    pid_liked = 'spotify:playlist:1Ol1AQX5IDgBKjEqVflQ0y'
    pid_disliked = 'spotify:playlist:1skUtkQW7tB9v9nsOJbw84'

    # Playlist of Janna's music 
    pid_recommenders_library = 'spotify:playlist:1sShkL1XOhll7tPt2tUnif'

    dp.create_datasets(pid_liked, pid_disliked, 'music_prefs.csv') 
    dp.create_recommenders_datasets(pid_recommenders_library, 'recommenders_df.csv') #change to final_rec_df.csv


if __name__ == '__main__':
    main()
