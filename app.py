from flask import Flask, request, jsonify
import mysql.connector
import joblib

app = Flask(__name__)

def get_user_data(user_id):
        conn = mysql.connector.connect(
        host="fdb1027.biz.nf",
        user="4515138_maly",
        password="Ro0597980060-",
        database="4515138_maly"


    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT income FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("SELECT category, amount FROM transactions WHERE user_id = %s", (user_id,))
    transactions = cursor.fetchall()

    conn.close()

    return user, transactions

@app.route('/recommendation', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'user_id مطلوب'}), 400

    user, transactions = get_user_data(user_id)

    if not user or not transactions:
        return jsonify({'recommendation': 'لم يتم العثور على بيانات كافية'}), 404

    # مثال: استخدم موديل محفوظ مسبقاً
    model = joblib.load('model.pkl')

    # مثال: تحويل البيانات إلى صيغة مناسبة
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
    app.run(debug=True)
