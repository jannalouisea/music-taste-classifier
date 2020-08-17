import matplotlib
from data_processing import DataProcessing
from data_description import DataDescription
from sk_models import SKModel
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    """
    Driver
    """

    dp = DataProcessing()
    dd = DataDescription()

    dp.authenticate('antoine')

    pid_liked = 'spotify:playlist:1Ol1AQX5IDgBKjEqVflQ0y'
    pid_disliked = 'spotify:playlist:1skUtkQW7tB9v9nsOJbw84'

    pid_recommenders_library = 'spotify:playlist:1sShkL1XOhll7tPt2tUnif'

  #  dp.create_datasets(pid_liked, pid_disliked)
    dp.create_recommenders_datasets(pid_recommenders_library)


    #print(training_df.to_string())
  #  dd.visualize(training_df)
  #  dimen_reduced_training_df = dp.pca()

    """try:
        model_choice = int(input('Choose a model: \n'
                                 '0: Logistic Regression\n'
                                 '1: Random Forest\n'
                                 '2: LDA \n'
                                 '3: Naive Bayes \n'
                                 '4: KNN \n'
                                 '5: Decision Trees \n'
                                 '6: MLP Classifier \n'))
    except (ValueError, TypeError):
        model_choice = 0

    model = SKModel(model_choice, 5)            # 5 k-fold cross validation

    print("Starting cross validation...")
    acc = model.cross_validate(dp.training_X, dp.training_y)
    print("The accuracy is " + str(acc))

    predictions = model.generate_predictions(dp.training_X, dp.training_y, dp.test_X)
    model.evaluate(dp.test_y, predictions)
"""

"""
27/03/20

CV SCORES
- Logistic regression: 0.5974533600648904
- Random Forest: 0.6400927442187906
- LDA: 0.6134561080417434
- Naive Bayes: 0.5575688822230045
- KNN: 0.5238152240638428
- Decision Trees: 0.5791664498553741
- MLP Classifier: 0.4811602209944752


"""



if __name__ == '__main__':
    main()
