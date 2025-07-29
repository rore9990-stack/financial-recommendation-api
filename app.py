import os
from flask import Flask, request, jsonify
import mysql.connector
import joblib

app = Flask(__name__)

# ... كود get_user_data ...

@app.route('/recommendation', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'user_id مطلوب'}), 400

    user, transactions = get_user_data(user_id)
    if not user or not transactions:
        return jsonify({'recommendation': 'لم يتم العثور على بيانات كافية'}), 404

    model = joblib.load('model.pkl')
    income = user['income']
    total_spent = sum(t['amount'] for t in transactions)
    category_counts = len(set(t['category'] for t in transactions))
    features = [[income, total_spent, category_counts]]
    recommendation = model.predict(features)[0]

    return jsonify({'recommendation': recommendation})

@app.route('/')
def home():
    return "Financial Recommendation API is running!"

if __name__ == '__main__':
    import joblib, mysql.connector
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
