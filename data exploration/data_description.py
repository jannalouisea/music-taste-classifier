import matplotlib.pyplot as plt
import seaborn as sns

class DataDescription:


    def __init__(self):
        self.df = None
        self.liked = None
        self.disliked = None


    def describe(self, df):
        self.df = df
        self.liked = df[df['like']==1]
        self.disliked = df[df['like']==0]


    def visualize(self, df):
        self.df = df
        self.liked = df[df['like']==1]
        self.disliked = df[df['like']==0]

        try:
            choice = int(input('Choose a visualization: \n'
                               '0: Individual boxplots and countplots \n'
                               '1: Pairplots \n'
                               '2: Correlation Heatmap \n'))
        except (ValueError, TypeError):
            choice = 0

        if choice == 0:
            self.feature_distributions()

        elif choice == 1:
            print("This is pairplot #1: \n")
            sns.pairplot(data=self.training_dataset[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'like']],
                         hue='like', height=1)
            plt.show()

            print('This is pairplot #2: \n')
            sns.pairplot(data=self.training_dataset[['liveness', 'valence', 'tempo', 'duration_ms', 'popularity', 'like']],
                         hue='like', height=1)
            plt.show()


        else:
            corr_liked = self.liked_df.corr()
            corr_disliked = self.disliked_df.corr()

            print("This is the correlation heatmap for liked songs: \n")
            sns.heatmap(corr_liked, xticklabels=corr_liked.columns, yticklabels=corr_liked.columns,
                        cmap=sns.diverging_palette(220, 10, as_cmap=True))
            plt.show()

            print("This is the correlation heatmap for disliked songs: \n")
            sns.heatmap(corr_disliked, xticklabels=corr_disliked.columns, yticklabels=corr_disliked.columns,
                        cmap=sns.diverging_palette(220, 10, as_cmap=True))
            plt.show()


    def feature_distributions(self):

        distrib_feats_liked = self.liked[['danceability', 'energy', 'loudness', 'speechiness',
                                               'acousticness', 'instrumentalness', 'liveness',
                                               'valence', 'tempo', 'duration_ms', 'popularity', 'like']]
        distrib_feats_disliked = self.disliked[['danceability', 'energy', 'loudness', 'speechiness',
                                               'acousticness', 'instrumentalness', 'liveness',
                                               'valence', 'tempo', 'duration_ms', 'popularity', 'like']]
        count_feats = self.df[['mode', 'time_signature', 'explicit', 'key', 'like']]

        fig, axes = plt.subplots(3, 4, figsize=(9, 9))
        fig.suptitle('Continuous variable distribution', fontsize=20)
        for i, feature in enumerate(distrib_feats_liked.columns):
            sns.distplot(distrib_feats_liked[feature],  color="green", hist=False, ax=axes[i // 4, i % 4])
            sns.distplot(distrib_feats_disliked[feature],  color="red", hist=False, ax=axes[i // 4, i % 4])

            x = feature
            axes[i//4, i % 4].set_xlabel(x, fontsize=10)
            axes[i//4, i % 4].set_ylabel('frequency', fontsize=10)

        plt.show()

        fig2, axes2 = plt.subplots(2, 3, figsize=(11, 9))
        fig2.suptitle('Categorical variable count', fontsize=20)
        for i, feature in enumerate(count_feats.columns):
            sns.countplot(x=feature, hue='like', data=count_feats, ax=axes2[i//3, i%3])

        plt.show()


