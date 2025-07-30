import os
from flask import Flask, request, jsonify
import mysql.connector
import joblib
import sys

MODEL_FILENAME = 'financial_model.pkl'  # اسم ملف النموذج الجديد

app = Flask(__name__)

def get_user_data(user_id):
    conn = mysql.connector.connect(
        host="fdb1027.biz.nf",
        user="4515138_maly",
        password="Ro0597980060-",
        database="4515138_maly"
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("SELECT category, amount FROM transactions WHERE user_id = %s", (user_id,))
    transactions = cursor.fetchall()

    cursor.close()
    conn.close()

    return user, transactions

def load_or_train_model():
    if not os.path.exists(MODEL_FILENAME):
        print(f"ملف النموذج '{MODEL_FILENAME}' غير موجود، جاري تدريب النموذج ...")
        import train_model  # تأكد أن train_model.py يحفظ النموذج باسم financial_model.pkl
        print("تم تدريب النموذج وحفظه.")
    model = joblib.load(MODEL_FILENAME)
    return model

model = load_or_train_model()

@app.route('/')
def home():
    return "Financial Recommendation API is running!"

@app.route('/recommendation', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'user_id مطلوب'}), 400

    user, transactions = get_user_data(user_id)
    if not user or not transactions:
        return jsonify({'recommendation': 'لم يتم العثور على بيانات كافية'}), 404

    income = user['income']
    total_spent = sum(t['amount'] for t in transactions)
    category_counts = len(set(t['category'] for t in transactions))
    features = [[income, total_spent, category_counts]]
    recommendation = model.predict(features)[0]

    return jsonify({'recommendation': recommendation})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
