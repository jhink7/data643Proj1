from math import*
import pandas as pd

class RecommendationEngine:
    def __init__(self):
        self.name = 'recommendation engine'

    def generate_recommendations(self, user_id):
        similiarity = self.cosine_similarity([3, 45, 7, 2], [2, 54, 13, 15])
        similiarity = self.jaccard_similarity([0,1,2,5,6],[0,2,3,5,7,9])
        similiarity = self.jaccard_similarity(['title1', 'title2', 'title3'], ['title3'])
        users, movies, ratings = self.load_data()

        #users = users.sort(['name'])
        return similiarity

    def load_data(self):
        all_users = pd.DataFrame.from_csv('users.csv')
        all_movies = pd.DataFrame.from_csv('movies.csv')
        all_ratings = pd.DataFrame.from_csv('ratings.csv')
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