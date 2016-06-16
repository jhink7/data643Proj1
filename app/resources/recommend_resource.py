from app import app
from flask import jsonify, request, abort
from config import BASE_URL
from app.rec_engine.recommendation_engine import RecommendationEngine

@app.route(BASE_URL + 'recommendations', methods=['GET'])
def get_all_recs():
    return jsonify({'numRecs': 12})

@app.route(BASE_URL + 'users/<int:user_id>/recommendations', methods=['GET'])
def get_recs_for_user(user_id):
    recEngine = RecommendationEngine()
    recs = recEngine.generate_recommendations(user_id)
    return jsonify({'numRecs': recs})