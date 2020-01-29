from data_processing import DataProcessing


def main():
    """
    Driver
    """

    dp = DataProcessing()
    dp.authenticate('janna')

    pid_liked = 'spotify:playlist:1Ol1AQX5IDgBKjEqVflQ0y'
    pid_disliked = 'spotify:playlist:1skUtkQW7tB9v9nsOJbw84'

    training_df = dp.create_dataset(pid_liked, pid_disliked, 'training')

    print(training_df.to_string())



if __name__ == '__main__':
    main()
