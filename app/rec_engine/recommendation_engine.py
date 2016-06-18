from math import*
import pandas as pd
import numpy as np

class RecommendationEngine:
    def __init__(self):
        self.name = 'recommendation engine'

    def generate_recommendations(self, user_id):
        similiarity = self.cosine_similarity([3, 45, 7, 2], [2, 54, 13, 15])
        similiarity = self.jaccard_similarity([0,1,2,5,6],[0,2,3,5,7,9])
        similiarity = self.jaccard_similarity(['title1', 'title2', 'title3'], ['title3'])
        users, movies, ratings = self.load_data()

        user_exists = False
        all_user_ids = users.id.values[:]

        # ensure user requested exists in database
        # if not, bubble this info to resource layer which will throw the appropriate http error
        if user_id in all_user_ids:
            user_exists = True

            # get list of users who we want to generate similarity scores for
            comp_user_ids =  np.array(filter(lambda x: x != user_id, all_user_ids))

            df_sim_scores = pd.DataFrame(columns=['id', 'jac'])

            for i in comp_user_ids:
                    user_movies_rated = set(ratings[ratings['user_id'] == user_id].movie_id)
                    comp_user_movies_rated = set(ratings[ratings['user_id'] == i].movie_id)
                    jac = self.jaccard_similarity(user_movies_rated, comp_user_movies_rated)
                    df_sim_scores.loc[len(df_sim_scores)] = [i, jac]

            df_sim_scores[['id']] = df_sim_scores[['id']].astype(int)
            print df_sim_scores
        return user_exists, similiarity

    def load_data(self):
        all_users = pd.read_csv('users.csv')
        all_movies = pd.read_csv('movies.csv')
        all_ratings = pd.read_csv('ratings.csv')
        return all_users, all_movies, all_ratings

    def square_rooted(self,x):
        return round(sqrt(sum([a * a for a in x])), 3)

    def cosine_similarity(self, r1, r2):
        num = sum(a * b for a, b in zip(r1, r2))
        denom = self.square_rooted(r1) * self.square_rooted(r2)
        return round(num / float(denom), 3)

    def jaccard_similarity(self, m1, m2):
        int_card = len(set.intersection(*[set(m1), set(m2)]))
        un_card = len(set.union(*[set(m1), set(m2)]))
        return round(int_card / float(un_card), 3)