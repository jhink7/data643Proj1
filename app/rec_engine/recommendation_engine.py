from math import*
import pandas as pd
import numpy as np

class RecommendationEngine:
    MAX_RECS = 3
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

            df_sim_scores = pd.DataFrame(columns=['id', 'jac', 'cos', 'comb'])

            user_movies_rated = ratings[ratings['user_id'] == user_id]
            for i in comp_user_ids:
                    comp_user_movies_rated = ratings[ratings['user_id'] == i]

                    jac = self.jaccard_similarity(set(user_movies_rated.movie_id), set(comp_user_movies_rated.movie_id))

                    both_seen_ids = set.intersection(*[set(user_movies_rated.movie_id), set(comp_user_movies_rated.movie_id)])

                    user_scores = []
                    comp_scores = []
                    for j in both_seen_ids:
                        user_score = np.average(
                            ratings[(ratings['movie_id'] == j) & (ratings['user_id'] == user_id)].rating.values)
                        comp_score = np.average(
                            ratings[(ratings['movie_id'] == j) & (ratings['user_id'] == i)].rating.values)
                        user_scores.append(user_score)
                        comp_scores.append(comp_score)

                    cos = self.cosine_similarity(user_scores, comp_scores)
                    df_sim_scores.loc[len(df_sim_scores)] = [i, jac, cos, (jac + cos)]

            df_sim_scores[['id']] = df_sim_scores[['id']].astype(int)
            df_sim_scores = df_sim_scores.sort_values(['comb'], ascending=[False])

            target_movie_ids = []
            for i in df_sim_scores.id.values:
                filt = ratings[(ratings['user_id'] == i)]
                g = filt.groupby('movie_id').agg({'rating':[np.size, np.mean]})
                atleast_3 = g['rating']['mean'] >= 3
                g = g[atleast_3].sort_values([('rating', 'mean')], ascending=False)

                cands = g.reset_index().movie_id.values

                for c in cands:
                    if not(c in user_movies_rated.movie_id.values) and not(c in target_movie_ids):
                        target_movie_ids.append(c)

            recs = []
            for t in target_movie_ids:
                title = movies[(movies['id'] == t)].title.values[0]
                recs.append(title)
        return user_exists, recs[:self.MAX_RECS]

    def load_data(self):
        all_users = pd.read_csv('data/users.csv')
        all_movies = pd.read_csv('data/movies.csv')
        all_ratings = pd.read_csv('data/ratings.csv')
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