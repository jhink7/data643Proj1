from app import app
from flask import jsonify, request, abort
from config import BASE_URL
from app.rec_engine.recommendation_engine import RecommendationEngine

@app.route(BASE_URL + 'users/<int:user_id>/recommendations', methods=['GET'])
def get_recs_for_user(user_id):
    recEngine = RecommendationEngine()
    user_exists, recs = recEngine.generate_recommendations(user_id)
    if not user_exists:
        abort(404)
    return jsonify({'top_picks': recs})